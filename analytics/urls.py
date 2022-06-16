from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

# A list of url patterns.
urlpatterns = [
    path('chart/filter-options/', views.get_filter_options,
         name='chart-filter-options'),
    path('chart/sales/<int:year>/', views.get_sales_chart, name='chart-sales'),
    path('chart/spend-per-customer/<int:year>/',
         views.spend_per_customer_chart, name='chart-spend-per-customer'),
    path('chart/payment-success/<int:year>/',
         views.payment_success_chart, name='chart-payment-success'),
    path('chart/payment-method/<int:year>/',
         views.payment_method_chart, name='chart-payment-method'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
