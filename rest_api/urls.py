from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from . import views


router = DefaultRouter()
router.get_api_root_view().cls.__name__ = 'Api Root'
router.register(r'categoties', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'carts', views.InvoiceCartViewSet, basename='cart')
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'users', views.UserViewSet, basename='user')
# login through the rest api.
router.register(r'auth', views.AuthViewSet, basename='auth')
urlpatterns = router.urls

urlpatterns += [
    path('analatics/', views.AnalaticsViewSet.as_view(), name='analatic'),
    # api-auth/login/ | and | api-auth/logout/
    path('api-auth/', include('rest_framework.urls')),
    # Documentations routes
    path('schema/', SpectacularAPIView.as_view(), name="schema"),
    path('docs/', SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    # path('password_reset/', include('django_rest_passwordreset.urls',
    #      namespace='password_reset')),
]
