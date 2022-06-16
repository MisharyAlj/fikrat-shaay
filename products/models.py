from django.utils.text import slugify
from django.db import models
from datetime import date
import uuid
from django.utils.translation import gettext_lazy as _
from Users.models import CustomUser


class Category(models.Model):
    title = models.CharField(_('Title'), max_length=75,
                             null=False, db_index=True)
    ar_title = models.CharField(_('Arabic title'), max_length=75,
                                null=False, db_index=True, default='arabic title')
    slug = models.SlugField(unique=True, null=True, blank=True)
    content = models.CharField(
        _('Content'), max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(
        Category, verbose_name=_('Category'), related_name='products', on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=75, null=False)
    ar_title = models.CharField(
        _('Arabic title'), max_length=75, null=False, default='ar')
    summary = models.CharField(
        _('Summary'), max_length=255, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=5)
    createdBy = models.ForeignKey(
        CustomUser, verbose_name=_('Created by'), related_name='product_created_by', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-createdAt',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Invoice(models.Model):
    PAYMENT_TYPE = (
        ('Cash', _('Cash')),
        ('Debit Card', _('Debit Card'))
    )

    uniqueId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    invoiceId = models.CharField(_('invoice ID'), blank=True, max_length=8)
    total = models.DecimalField(_('total'), decimal_places=2, max_digits=6)
    payment_type = models.CharField(_('payment type'),
                                    max_length=75, choices=PAYMENT_TYPE, default='Credit')
    createdBy = models.ForeignKey(
        CustomUser, related_name='invoice_created_by', on_delete=models.CASCADE)

    # Utilites
    slug = models.SlugField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoiceId

    def save(self, *args, **kwargs):
        if not self.invoiceId:
            today = date.today()
            today_str = today.strftime('%y%m%d')
            next_invoice_number = '01'
            last_invoice = Invoice.objects.all().filter(
                invoiceId__startswith=today_str).order_by('invoiceId').last()
            if last_invoice:
                last_invoice_number = int(last_invoice.invoiceId[6:])
                next_invoice_number = '{0:02d}'.format(last_invoice_number + 1)
            self.invoiceId = today_str + next_invoice_number
        if not self.slug:
            self.slug = slugify(self.invoiceId)
        super(Invoice, self).save(*args, **kwargs)


class Invoice_Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='invoice_cart')
    quantity = models.PositiveSmallIntegerField(_('quantity'), )

    class Meta:
        verbose_name_plural = 'Invoices Carts'

    def __str__(self):
        return "%s -- %s - quantity:  %s" % (self.product.title, self.invoice.invoiceId, self.quantity)
