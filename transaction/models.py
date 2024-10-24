from django.db import models
from warehouse.models import ProductModel


# Modelo para los clientes
class CustomerModel(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  address = models.CharField(max_length=200)
  document_number = models.CharField(max_length=100)
  email = models.EmailField(unique=True)

  class Meta:
    verbose_name = 'Cliente'
    verbose_name_plural = 'Clientes'
    db_table = 'customers'


# Modelo para las ventas
class SaleModel(models.Model):
  id = models.AutoField(primary_key=True)
  code = models.CharField(max_length=100)
  total = models.FloatField()
  STATUS_CHOICES = (
    ('PENDING', 'Pendiente'),
    ('COMPLETED', 'Completado'),
    ('CANCELLED', 'Cancelado'),
    ('DELETED', 'Eliminado'),
  )
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  customer = models.ForeignKey(
    CustomerModel, 
    on_delete=models.CASCADE,
    related_name='sales',
    db_column='customer_id'
  )

  class Meta:
    verbose_name = 'Venta'
    verbose_name_plural = 'Ventas'
    db_table = 'sales'


# Modelo para los productos vendidos
class SaleDetailModel(models.Model):
  id = models.AutoField(primary_key=True)
  quantity = models.IntegerField()
  price = models.FloatField()
  subtotal = models.FloatField()
  sale = models.ForeignKey(
    SaleModel, 
    on_delete=models.CASCADE,
    related_name='details',
    db_column='sale_id'
  )
  product = models.ForeignKey(
    ProductModel, 
    on_delete=models.CASCADE,
    related_name='product_details',
    db_column='product_id'
  )

  class Meta:
    verbose_name = 'Detalle de venta'
    verbose_name_plural = 'Detalles de venta'
    db_table = 'sale_details'





