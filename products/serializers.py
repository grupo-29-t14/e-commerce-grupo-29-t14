from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Product
        fields = ('id', 'seller', 'name', 'category', 'stock', 'price')

    def validate(self, data):
    
        if not data:
            raise serializers.ValidationError("Nenhum dado enviado ou os dados enviados são inválidos. Revisar a requisição.")
       
        return data


