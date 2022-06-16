from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Avg, Sum, F
from django.http import JsonResponse
from django.shortcuts import render
from products.models import Category, Invoice, Invoice_Cart, Product
from .utils.charts import colorPrimary, colorSuccess, colorDanger, get_year_dict, months, generate_color_palette


"""
It gets all the years from the Invoice model and returns them as a JSON response

:param request: The request object
:return: A list of years.
"""


def get_filter_options(request):
    grouped_purchases = Invoice.objects.annotate(year=ExtractYear(
        'createdAt')).values('year').order_by('-year').distinct()
    options = [purchase['year'] for purchase in grouped_purchases]

    return JsonResponse({
        'options': options,
    })


"""
It takes a year as a parameter, gets all the invoices from that year, groups them by month, sums the
prices of the products in each invoice, and returns a JSON response with the data for the chart

:param request: The request object
:param year: The year for which you want to get the sales chart
:return: A JsonResponse object.
"""


def get_sales_chart(request, year):
    purchases = Invoice.objects.filter(createdAt__year=year)
    grouped_purchases = purchases.annotate(price=F('invoice_cart__product__price')).annotate(month=ExtractMonth('createdAt'))\
        .values('month').annotate(average=Sum('invoice_cart__product__price')).values('month', 'average').order_by('month')

    sales_dict = get_year_dict()

    for group in grouped_purchases:
        sales_dict[months[group['month']-1]] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Sales in {year}',
        'data': {
            'labels': list(sales_dict.keys()),
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(sales_dict.values()),
            }]
        },
    })


"""
It takes a year as a parameter, gets all the purchases made in that year, groups them by month, and
then returns the average price of each month as a JSON response

:param request: The request object
:param year: The year to filter the data by
:return: A JSON response.
"""


def spend_per_customer_chart(request, year):
    purchases = Invoice.objects.filter(createdAt__year=year)
    grouped_purchases = purchases.annotate(price=F('invoice_cart__product__price')).annotate(month=ExtractMonth('createdAt'))\
        .values('month').annotate(average=Avg('invoice_cart__product__price')).values('month', 'average').order_by('month')

    spend_per_customer_dict = get_year_dict()

    for group in grouped_purchases:
        spend_per_customer_dict[months[group['month']-1]
                                ] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Spend per customer in {year}',
        'data': {
            'labels': list(spend_per_customer_dict.keys()),
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(spend_per_customer_dict.values()),
            }]
        },
    })


"""
It returns a JSON response containing a chart's title and data

:param request: The request object
:param year: The year to filter the purchases by
:return: A JsonResponse object.
"""


def payment_success_chart(request, year):
    purchases = Invoice.objects.filter(createdAt__year=year)

    return JsonResponse({
        'title': f'Payment success rate in {year}',
        'data': {
            'labels': ['Successful', 'Unsuccessful'],
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': [colorSuccess, colorDanger],
                'borderColor': [colorSuccess, colorDanger],
                'data': [
                    purchases.filter(successful=True).count(),
                    purchases.filter(successful=False).count(),
                ],
            }]
        },
    })


"""
It takes a year as a parameter, then it filters the Invoice model by that year, then it groups the
filtered Invoice model by payment type, then it sums the total of each group, then it orders the
groups by payment type, then it creates a dictionary with the payment types as keys and the total as
values, then it returns a JsonResponse with the data

:param request: The request object
:param year: The year for which the chart is to be generated
:return: A JsonResponse object.
"""


def payment_method_chart(request, year):
    purchases = Invoice.objects.filter(createdAt__year=year)
    grouped_purchases = purchases.values('payment_type').annotate(total=Sum('total'))\
        .values('payment_type', 'total').order_by('payment_type')

    payment_method_dict = dict()

    for payment_method in Invoice.PAYMENT_TYPE:
        payment_method_dict[payment_method[1]] = 0

    for group in grouped_purchases:
        payment_method_dict[dict(Invoice.PAYMENT_TYPE)[
            group['payment_type']]] = group['total']

    return JsonResponse({
        'title': f'Payment method rate in {year}',
        'data': {
            'labels': list(payment_method_dict.keys()),
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': generate_color_palette(len(payment_method_dict)),
                'data': list(payment_method_dict.values()),
                'borderWidth': 0,
                'hoverOffset': 4,
                'spacing': '5',
                'cutoutPercentage': 70,
            }]
        },
    })
