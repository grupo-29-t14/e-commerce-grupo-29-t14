from rest_framework.views import APIView, Response
from .serializers import OrderSerializer, ProductsOrdersSerializer, ListOrderSerializer, UpdateOrderSerializer
from cart.models import Cart
from cart.models import CartProducts
from users.models import User
from products.models import Product
from orders.models import ProductsOrders, Order
from .permissions import UpdateOrderPermisson, DeleteOrderPermisson
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404


class OrderView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id

        cart = get_object_or_404(Cart, buyer_id=user_id)

        cart_products = CartProducts.objects.filter(cart_id=cart)
        get_object_or_404(CartProducts, cart_id=cart)

        cart_products_list = list(cart_products.values())

        user_orders = cart_products_list

        for order in user_orders:
            product_id = order["product_id"]
            price = order["price"]
            quantity = order["quantity"]

            total_price = price * quantity

            product = Product.objects.get(pk=product_id)

            if product.stock < quantity:
                return Response({"detail": "The order cannot be fulfilled. quantity greater than stock"}, 409)

            seller_id = product.seller_id

            data = {
                "price_total": total_price
            }

            serializer = OrderSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            serializer.save(user_id=user_id, seller_id=seller_id)

            order_id = serializer.data["id"]

            data_product_orders = {
                "quantity": quantity,
                "price": price
            }

            serializer_product_orders = ProductsOrdersSerializer(data=data_product_orders)
            serializer_product_orders.is_valid(raise_exception=True)

            serializer_product_orders.save(product_id=product_id, order_id=order_id)

            new_stock = (product.stock) - int(quantity)

            validated_data = {"stock": f"{new_stock}"}

            for key, value in validated_data.items():
                setattr(product, key, value)
                product.save()

            return Response(serializer.data, 201)


class RetriveOrderView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ProductsOrders.objects.all()
    serializer_class = ProductsOrdersSerializer


class ListOrderView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = ListOrderSerializer

    def get_queryset(self):
        kwargs = self.kwargs
        get_object_or_404(Order, user_id=kwargs["pk"])
        return Order.objects.filter(user_id=kwargs["pk"])


class DestroyOrderView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, DeleteOrderPermisson]

    queryset = Order.objects.all()
    serializer_class = ListOrderSerializer


class UpdateOrderView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, UpdateOrderPermisson]

    queryset = Order.objects.all()
    serializer_class = UpdateOrderSerializer

    def perform_update(self, serializer):
        order = Order.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=order.user_id)
        new_status = self.request.data

        # send_mail(
        #     subject='Atualização em seu pedido',
        #     message=f'O status do seu pedido foi atualizado para {new_status}',
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[user.email],
        #     fail_silently=False
        # )
        serializer.save()
