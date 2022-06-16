from rest_framework import serializers
from Users.models import CustomUser
from . import models


# This class is a serializer for the CustomUser model. It will only return the id, first_name, and
# last_name fields.
class CreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
        ]


# The ProductSerializer class is a subclass of the ModelSerializer class. It has a Meta class that
# defines the model to be serialized, the fields to be serialized, and the fields that are read-only
class ProductSerializer(serializers.ModelSerializer):
    createdBy = CreatedBySerializer(read_only=True)

    class Meta:
        model = models.Product
        lookup_field = 'slug'
        fields = [
            'id', 'category', 'title', 'slug', 'summary',
            'price', 'createdAt', 'updatedAt', 'createdBy'
        ]
        extra_kwargs = {
            "category": {"required": True},
        }
        read_only_fields = ("slug",)


# The `CategorySerializer` class is a subclass of the `ModelSerializer` and it's used to serialize the `Category` model.
# It has a Meta class that
# defines the model that the serializer is going to be based on. It also defines the fields that are
# going to be serialized
class CategorySerializer(serializers.ModelSerializer):

    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = models.Category
        #lookup_field = 'slug'
        fields = [
            'id', 'title', 'slug', 'content', 'products'
        ]
        read_only_fields = ("slug",)


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            "id",
            "title",
            "price"
        ]


class InvoiceCartSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)

    class Meta:
        model = models.Invoice_Cart
        fields = [
            "product",
            "quantity"
        ]


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Invoice_Cart
        fields = '__all__'
        extra_kwargs = {'product': {'required': True}}


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_cart = InvoiceCartSerializer(read_only=True, many=True)
    createdBy = CreatedBySerializer(read_only=True)

    class Meta:
        model = models.Invoice
        depth = 1
        fields = [
            "uniqueId",
            "invoiceId",
            "invoice_cart",
            "total",
            "payment_type",
            "createdBy",
            "createdAt",
            "updatedAt",
            'slug'
        ]
        read_only_fields = ("createdBy", "invoiceId", "slug")
