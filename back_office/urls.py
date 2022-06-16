from django.urls import path, include
from . import views

# A list of url patterns.
urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('analytics/', views.Analatics, name='analytics'),
    path('users/', views.Users, name='users'),
    path('users/<int:id>/', views.user_detail, name='user_detail'),
    path('categories/', views.Categories, name='categories'),
    path('delete_category/<slug:slug>/',
         views.delete_category, name='delete_category'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('products/', views.Products, name='products'),
    path(r'products/<slug:slug>', views.product_detail, name='product_detail'),
    path(r'delete_product/<slug:slug>',
         views.delete_product, name='delete_product'),
    path(r'products/<int:id>/', views.Delete_Product, name='product_delete'),
    path(r'invoices/', views.Invoices, name='invoices'),
    path('analytics/', include('analytics.urls')),
]
