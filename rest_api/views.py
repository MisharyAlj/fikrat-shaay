
from rest_framework import viewsets, generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, Max, Min, Sum, Count
from django.contrib.auth import logout, login
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db.models.functions import TruncMonth, TruncDay, Trim, ExtractYear
from Users.models import CustomUser
from Users.serializers import UserSerializer, UserLoginSerializer, PasswordChangeSerializer, EmptySerializer
from products.models import Invoice_Cart, Category, Product, Invoice
from products.serializers import ProductSerializer, CategorySerializer, CartSerializer, InvoiceSerializer
from .permissions import IsSuperuser, IsSuperuserOrReadOnly
from .utils import get_and_authenticate_user


# **CategoryViewSet** is a class that inherits from **ModelViewSet**, and it returns a list of all
# **Categories** in the system
class CategoryViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all **Categories** in the system.
    """
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperuserOrReadOnly]
    queryset = Category.objects.all()
    lookup_field = 'slug'


# This class is a viewset that returns a list of all products in the system
class ProductViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all **Products** in the system.
    """
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsSuperuserOrReadOnly]
    queryset = Product.objects.all()
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(createdBy=self.request.user)


# This class is a viewset that allows the user to view, create, update, and delete Invoice_Cart
# objects
class InvoiceCartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Invoice_Cart.objects.all()


# Returns a list of all **Invoices** in the system
class InvoiceViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all **Invoices** in the system.
    """
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.prefetch_related(
        'invoice_cart')  # Reverse Relationship
    lookup_field = 'slug'

    def get_queryset(self):
        employee = self.request.user
        if employee is not None:
            if employee.is_superuser:
                return Invoice.objects.all().order_by('-createdAt')
            return Invoice.objects.filter(createdBy=employee)
        return None

    def perform_create(self, serializer):
        serializer.save(createdBy=self.request.user)


# This view should return a list of all the users for the superuser or the user currently
# authenticated
class UserViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all **Users** in the system.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the users
        for the superuser or the user currwntly authinticated.
        """
        user = self.request.user
        if user and user.is_superuser:
            return CustomUser.objects.all().order_by('-date_joined')
        return CustomUser.objects.filter(email=user)

    def options(self, request, *args, **kwargs):
        """
        Don't include the view description in OPTIONS responses.
        """
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        data.pop('description')
        return Response(data=data, status=status.HTTP_200_OK)


##### Testing this code #####
# A viewset that returns a list of analytics.
class AnalaticsViewSet(generics.GenericAPIView):
    permission_classes = [IsSuperuser, ]
    queryset = CustomUser.objects.all()
    serializer_class = EmptySerializer

    def get(self, request, *args, **kwargs):
        # Number of all products
        products = Product.objects.count()

        # List (number of invoices, total, total avg, max/min invoice total) of all invoices
        invoices_total = Invoice.objects.aggregate(
            num_of_sales=Count('invoiceId'),
            sales_total=Sum("total"),
            sales_total_avg=Avg('total'),
            max_sale_total=Max('total'),
            min_sale_total=Min('total'))

        # List of sales (number of invoices, total) by day
        sales_by_day = Invoice.objects.annotate(
            day=TruncDay('createdAt')).values('day').annotate(
                num_of_sales=Count('invoiceId'),
                sales_total=Sum('total'))

        # List of sales (number of invoices, total) by month
        sales_by_month = Invoice.objects.annotate(
            month=TruncMonth('createdAt')).values('month').annotate(
                num_of_sales=Count('invoiceId'),
                sales_total=Sum('total'))

        # List of sales (number of invoices, total) by year
        sales_by_year = Invoice.objects.annotate(
            year=ExtractYear('createdAt')).values('year').annotate(
                num_of_sales=Count('invoiceId'),
                sales_total=Sum('total'))

        # List of sales (number of invoices, total) by employee
        sales_by_employee = Invoice.objects.annotate(
            employee_id=Trim('createdBy')).values('employee_id').annotate(
                num_of_sales=Count('invoiceId'),
                sales_total=Sum('total'))

        # Number of activ users
        active_users = CustomUser.objects.filter(
            is_active='True').count()

        # Number of employees
        employees = CustomUser.objects.filter(
            is_staff='True').count()

        return Response({
            'products': products,
            'invoices': invoices_total,
            'sales_by_day': sales_by_day,
            'sales_by_month': sales_by_month,
            'sales_by_year': sales_by_year,
            'sales_by_employee': sales_by_employee,
            'active_users': active_users,
            'employees': employees,
        }, status=status.HTTP_200_OK)


# sing in and sing out through the api.
# It's a viewset that allows you to login, logout, and change your password
class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
        'password_change': PasswordChangeSerializer
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        data = UserSerializer(user).data
        return Response({'id': user.id,
                         'email': user.email,
                         'national_id': user.nationality_id,
                         'first_name': user.first_name,
                         'lirst_name': user.last_name,
                         'is_active': user.is_active,
                         'is_superuser': user.is_superuser,
                         'token': token.key}, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False, permission_classes=[permissions.IsAuthenticated, ])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        data = {'success': _('Sucessfully logged out')}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[permissions.IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        data = {'success': _('Password was changed sucessfully.')}
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
