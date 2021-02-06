from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.

User = get_user_model()


# категории товаров
class Category(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    # отображение навания категории в админке в виде строки
    def __str__(self):
        return self.name


# товары
class Product(models.Model):

    id = models.AutoField(primary_key=True)
    category = models.ForeignKey('mainapp.Category', verbose_name='Категория',
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание товара', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                verbose_name='Цена')

    # отображение навания товара в админке в виде строки
    def __str__(self):
        return self.title


# товары в корзине
class CartProduct(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('mainapp.Customer', verbose_name='Покупатель',
                             on_delete=models.CASCADE)
    cart = models.ForeignKey('mainapp.Cart', verbose_name='Корзина',
                             on_delete=models.CASCADE,
                             related_name='related_products')
    product = models.ForeignKey('mainapp.Product', verbose_name='Товар',
                                on_delete=models.CASCADE)
    # количество товаров в корзине
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      verbose_name='Общая цена')

    def __str__(self):
        return f'Товар: {self.product.title} (для корзины)'


# корзина
class Cart(models.Model):
    # пользователь корзины
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('mainapp.Customer', verbose_name='Владелец',
                              on_delete=models.CASCADE)
    product = models.ManyToManyField('mainapp.CartProduct', blank=True,
                                     related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2,
                                      verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)


# пользователь / покупатель
class Customer(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=20, verbose_name='Номер телефона')

    def __str__(self):
        return f'Покупатель: {self.user.first_name} {self.user.last_name}'


# Характеристики товара
class Specification(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255,
                            verbose_name='Имя товара для характеристик')

    def __str__(self):
        return f'Характиеристики товара: {self.name}'
