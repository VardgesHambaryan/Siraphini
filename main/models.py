from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class UserProfile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email



class Category(models.Model):

    name = models.CharField(_("Category name") , max_length=50)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(models.Model):

    category = models.ForeignKey(Category , on_delete=models.PROTECT , related_name='subcat')
    name = models.CharField(_("Sub Category name") , max_length=50)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"



class Color(models.Model):

    name = models.CharField(_("Color name") , max_length=30)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

class Size(models.Model):

    name = models.CharField(_("Size name") , max_length=30)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

class Image(models.Model):

    img = models.ImageField(upload_to='media')

    def __str__(self) -> str:
        return self.img.id
    
    def img_preview(self):
        return mark_safe(f'<img src = "{self.img.url}" width = "60"/>')

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"



class Product(models.Model):
    """Product model represents a product in the store"""
    


    name = models.CharField(_("Name"), max_length=200)
    price = models.FloatField(_("Price"))
    discount = models.DecimalField(_('Dicount') , max_digits=4 , decimal_places=2) 
    sex = models.CharField(max_length=10 , choices=[
        ('M' , 'Male'),
        ('F' , 'Female'),
        ('U' , 'Undefined'),
    ])

    color = models.ManyToManyField(Color)
    size = models.ManyToManyField(Size)
    image = models.ManyToManyField(Image)


    # privilege = models.TextField('') # BUG


    mean_rate_star_data = models.FloatField(_('Mean Rating')) # TODO: calculate mean 

    in_stock = models.BooleanField(default=True) 

    vendor_code = models.UUIDField()
    description = models.TextField(_("Description"))

    care_guide = models.TextField(_("Care Guide"))

    subcategory = models.ManyToManyField(SubCategory)
    categories = models.ForeignKey(Category , on_delete=models.PROTECT , related_name='prodcat' , blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        # Calculate discounted price before saving
        discounted_price = self.price - (self.price * (self.discount / 100))
        self.discounted_price = round(discounted_price, 2)  # Round to 2 decimal places
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class Review(models.Model):

    product =  models.ForeignKey(Product, on_delete=models.CASCADE , related_name='prod_review')
    user = models.ForeignKey(CustomUser , on_delete=models.PROTECT)
    review = models.TextField(_('Review'))
    star = models.IntegerField(_('Rating Starts') , choices=[
        (1 , '1'),
        (2 , '2'),
        (3 , '3'),
        (4 , '4'),
        (5 , '5'),
    ])

    created_at = models.DateTimeField(auto_now_add=True, editable=False)


    def __str__(self) -> str:
        return f"{self.user.username} {self.star}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Review"
        verbose_name_plural = "Reviews"




























