from rest_framework import serializers
from .models import (
  SaleModel,
  SaleDetailModel,
  CustomerModel,
)

class CustomerSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomerModel
    fields = '__all__'

class SaleDetailSerializer(serializers.ModelSerializer):    
  class Meta:
    model = SaleDetailModel
    fields = '__all__'
    extra_kwargs = {
      'sale': {
        'required': False,
      }
    } 

class SaleSerializer(serializers.ModelSerializer):
  code = serializers.CharField(read_only=True)
  status = serializers.CharField(read_only=True)
  customer = CustomerSerializer(many=False)           # por defecto
  details = SaleDetailSerializer(many=True)

  class Meta:
    model = SaleModel
    fields = '__all__'

  # Validaciones previas
  def validate(self, attrs):
    # comprobar stock de productos
    details = attrs.get('details')
    
    for detail in details:
      product = detail.get('product')
      if product.stock < detail.get('quantity'):
        raise serializers.ValidationError(
          f'No hay suficiente stock de {product.name}'
        )
    return attrs

  # Crear venta
  def create(self, validated_data):
    customer = validated_data.pop('customer')
    details = validated_data.pop('details')

    # customer_instance, _ = CustomerModel.objects.get_or_create(
    #   email = customer.get('email'),
    #   defaults = customer
    # )
    # manejando ya existencia del customer  
    print('pasanddo')
    try:
      customer = CustomerModel.objects.get(email=customer.get('email'))
      print(customer)
    except CustomerModel.DoesNotExist:
      print('ocurrio error en el customer')
      customer = CustomerModel.objects.create(**customer)

    sale = SaleModel.objects.create(**validated_data, customer=customer)

    for detail in details:
      # restar el stock de cada producto
      product = detail.get('product')
      quantity = detail.get('quantity')
      if product.stock < quantity:
        raise serializers.ValidationError(
          f'No hay suficiente stock de {product.name}'
        )
      product.stock -= quantity
      product.save()
      SaleDetailModel.objects.create(sale=sale, **detail)

    return sale
