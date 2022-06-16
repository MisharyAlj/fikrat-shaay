from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min, Sum, Count
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.core import serializers
from django.utils import timezone
from datetime import timedelta
from products.forms import createNewProductForm, createNewCategoryForm, productForm, categoryForm
from products.models import Category, Invoice, Invoice_Cart, Product
from Users.models import CustomUser
from products.filters import ProductFilter, InvoiceFilter
from Users.filters import UserFilter
from Users.forms import NewUserForm


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


"""
I'm trying to get the sum of the total field in the Invoice model.
    :param request: The request object passed to the view
    :return: A dictionary with the following keys:
"""


@login_required(login_url='login')
def Dashboard(request):
    last_5_invoices = Invoice.objects.all().order_by('-createdAt')[:6]
    date_from = timezone.now() - timedelta(days=1)
    sales_last_24 = Invoice.objects.filter(
        createdAt__gt=date_from).aggregate(
        num_of_sales=Count('invoiceId'),
        sales_total=Sum("total"),
        sales_total_avg=Avg('total'),
        max_sale_total=Max('total'),
        min_sale_total=Min('total'))
    total1 = sales_last_24.get('sales_total')
    context = {
        'title': _("Dashboard"),
        'last_5_invoices': last_5_invoices,
        'sales_last_24': sales_last_24,
    }
    return render(request, 'back_office/index.html', context)


"""
If the user is logged in, render the analytics page. If not, redirect to the login page.

    :param request: The request object is an HttpRequest object. It contains metadata about the request,
    such as the HTTP method ("GET" or "POST"), the user's IP address, the browser they're using, etc
    :return: a render object.
"""


@login_required(login_url='login')
def Analatics(request):
    if request.user.is_authenticated:
        print('User is Loogedin :}')
    else:
        redirect('login')
    context = {
        'title': _("analytics"),
    }
    return render(request, 'back_office/analytics.html', context)


"""
    If the user is authenticated and is a superuser, then print "Admin User :}", otherwise print "You
    are not admin user!!!".

    :param request: The request object is the first parameter to all Django views. It contains metadata
    about the request, such as the HTTP method ("GET" or "POST"), the client's IP address, the query
    parameters, and more
    :return: A list of users.
"""


@login_required(login_url='login')
def Users(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = CustomUser.objects.all().order_by('-date_joined')
        form = NewUserForm()

        filter = UserFilter(request.GET, queryset=users)
        users = filter.qs

    else:
        redirect('login')
    context = {
        'title': _("users"),
        'users': users,
        'form': form,
        'filter': filter,
    }
    return render(request, 'back_office/users.html', context)


"""
It's a view that allows the user to update the information of a user.

:param request: The request object
:param id: The id of the user you want to edit
:return: The user_detail view is being returned.
"""


@login_required(login_url='login')
def user_detail(request, id):
    user = CustomUser.objects.get(id=id)
    form = NewUserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, _(
            'The user was updated seccesfuly.'))
        if request.POST.get('_save'):
            return redirect('users')
        elif request.POST.get('_continue'):
            return redirect('user_detail', id)
    context = {
        'title': user.first_name,
        'user': user,
        'form': form,
    }
    return render(request, 'back_office/user-detail.html', context)


"""
If the request is a POST request, then the form is saved and the new category is returned as a JSON
object.
    
:param request: The request object
:return: The form is being returned.
"""


@login_required(login_url='login')
def Categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        categories = Category.objects.all()
        products = Product.objects.all().values()
        form = createNewCategoryForm
        # request should be ajax and method should be POST.
        if request.method == 'POST':
            # get the form data
            form = createNewCategoryForm(request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                # serialize in new CATEGORY object in json
                ser_instance = serializers.serialize('json', [instance, ])
                # send to client side.
                print(ser_instance)
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)
    else:
        print("You are not admin user!!!")
        return redirect('login')
    context = {
        'title': _("Categories"),
        'categories': categories,
        'products': products,
        'form': form,
    }
    return render(request, 'back_office/categories.html', context)


"""
It's a view that renders a form to edit a category and a form to create a new product.

:param request: The request object
:param slug: The slug of the category to be edited
:return: The category_detail view is being returned.
"""


@login_required(login_url='login')
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    form = categoryForm(request.POST or None, instance=category)
    new_product_form = createNewProductForm(
        request.POST or None, initial={'category': category, 'price': 0.0})
    if form.is_valid():
        form.save()
        messages.success(request, _(
            'The category was updated seccesfuly.'))
        if request.POST.get('_save'):
            return redirect('categories')
        elif request.POST.get('_continue'):
            return redirect('category_detail', slug)
    context = {
        'title': category.title,
        'category': category,
        'form': form,
        'new_product_form': new_product_form,
    }
    return render(request, 'back_office/category-detail.html', context)


"""
It gets the category with the slug that was passed in the URL, deletes it, and then redirects to the
categories page

:param request: The request object is the first parameter to every view. It contains information
about the current request, such as the method (GET or POST), the user (if they’re logged in), and
much more
:param slug: The slug of the category to be deleted
:return: The category is being deleted and a message is being sent to the user.
"""


def delete_category(request, slug):
    category = Category.objects.get(slug=slug)
    category.delete()
    messages.success(request, _(
        'The catecory was deleted seccesfuly.'))
    return redirect('categories')


"""
    If the request is ajax and the method is POST, then save the form data and return the serialized
    instance

    :param request: The request object
    :return: The form is being returned.
"""


@login_required(login_url='login')
def Products(request):
    products = Product.objects.all()
    form = createNewProductForm()
    filter = ProductFilter(request.GET, queryset=products)

    products = filter.qs

    print("user : ", request.user.nationality_id)
    # request should be ajax and method should be POST.
    if is_ajax(request=request) and request.method == "POST":
        # get the form data
        form = createNewProductForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save(commit=False)
            instance.createdBy = request.user
            instance.save()
            print(instance)
            # serialize in new product object in json
            ser_instance = serializers.serialize('json', [instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)
    print(products)
    context = {
        'title': _("Products"),
        'products': products,
        'form': form,
        'filter': filter,
    }
    return render(request, 'back_office/products.html', context)


"""
It takes a request, a slug, gets the product, creates a form, validates the form, saves the form,
and returns a redirect.

:param slug: The slug of the product to be edited
:return: The product_detail view is being returned.
"""


@login_required(login_url='login')
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    form = productForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, _(
            'The product was updated seccesfuly.'))
        if request.POST.get('_save'):
            return redirect('products')
        elif request.POST.get('_continue'):
            return redirect('product_detail', slug)
    context = {
        'title': product.title,
        'product': product,
        'form': form,
    }
    return render(request, 'back_office/product-detail.html', context)


"""
It deletes a product from the database

:param request: The request object is the first parameter to every view. It contains information
about the current request, such as the HTTP method, the URL, the headers, and the body
:param slug: The slug is a unique identifier for the product
:return: The product is being deleted and a message is being displayed.
"""


@login_required(login_url='login')
def delete_product(request, slug):
    product = Product.objects.get(slug=slug)
    product.delete()
    messages.success(request, _(
        'The product was deleted seccesfuly.'))
    return redirect('products')


"""
If the request is ajax and the method is POST, then return a JsonResponse with the instance deleted.

If not, return a JsonResponse with an error

:param request: The request object
:param id: The id of the product to be deleted
:return: a JsonResponse object.
"""


@login_required(login_url='login')
def Delete_Product(request, id):
    product = get_object_or_404(Product, id=id)
    # request should be ajax and method should be POST.
    if is_ajax(request=request) and request.method == "POST":
        print(product)
        return JsonResponse({"instance": 'Deleted seccesfuly'}, status=200)
    else:
        # some form errors occured.
        return JsonResponse({"error": 'Not found'}, status=404)


"""
It's a function that displays all invoices in the database.

:param request: The request object is the first parameter to all Django views. It contains metadata
about the request, such as the HTTP method, the URL, the headers, and the body of the request
:return: The invoice_cart is being returned as a list of objects.
"""


@login_required(login_url='login')
def Invoices(request):
    invoices = Invoice.objects.all()
    invoice_cart = Invoice_Cart.objects.select_related().all()
    filter = InvoiceFilter(request.GET, queryset=invoices)
    invoices = filter.qs

    context = {
        'title': _('invoices'),
        'invoices': invoices,
        'invoice_cart': invoice_cart,
        'filter': filter,
    }
    return render(request, 'back_office/invoices.html', context)


"""
It takes a request, gets all the categories from the database, and then renders the menu.html
template with the categories.

:param request: The request object is a standard Django object that contains metadata about the
current request
:return: The categories are being returned.
"""


def Menu(request):
    categories = Category.objects.all()
    context = {
        'title': _('Menu'),
        'categories': categories,
    }
    return render(request, 'main_site/menu.html', context)
