from django import forms
from .models import Category, Product


class productForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'ar_title', 'summary', 'price']


class createNewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'ar_title', 'summary', 'price']


# It creates a new category.
class categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'ar_title', 'content']


class createNewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'ar_title', 'content']
