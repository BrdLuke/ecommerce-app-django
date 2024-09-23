from django.db import models
from django.core.validators import RegexValidator

CATEGORY_CHOICES = (
    ('t-shirt','T-SHIRT'),
    ('jeans', 'JEANS'),
    ('hoodie','HOODIE'),
    ('shoes','SHOES'),
    ('man-necklaces','MAN-NECKLACES'),
)

class User(models.Model):
    last_name       = models.CharField(max_length=20)
    first_name      = models.CharField(max_length=20)
    email           = models.EmailField(unique=True)
    username        = models.CharField(max_length=50, unique=True)
    password        = models.CharField(max_length=128)

class Product(models.Model):
    product_name        = models.CharField(max_length=100, blank=True)
    product_category    = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=None)
    product_price       = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    product_image       = models.ImageField(upload_to='images/products')
    product_description = models.TextField(max_length=2000, blank=True)
    cart                = models.BooleanField(default= False)
    product_quantity    = models.PositiveIntegerField(blank=True, null=True, default=1)

    def __str__(self):
        return f"{self.product_category} - {self.product_name} - {self.cart}"
    
class Payment(models.Model):
    email               = models.EmailField(unique=False)
    phone_regex         = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    tel                 = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date                = models.DateField(blank=True)
    cvc                 = models.CharField(max_length=50, blank=True)
    name_card           = models.CharField(max_length=50, blank=True)
    continents          = models.CharField(max_length=50, blank=True)
    zip                 = models.CharField(max_length=50, blank=True)
    #product             = models.CharField(max_length=100, blank=True)  #TODO: check the file 'views.py' --> **def checkout(request):**
    
    def __str__(self):
        return f"{self.email}"