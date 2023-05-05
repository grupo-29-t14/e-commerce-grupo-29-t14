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
        
        
        if self.instance is None:  
            already_exists = Product.objects.filter(
                seller=self.context['request'].user,
                name=data['name'],
                category=data['category']
            ).exists()

            if already_exists:
                raise serializers.ValidationError("O produto já existe.")
       
        return data



