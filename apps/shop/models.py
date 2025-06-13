from django.db import models


class Category(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name_uz


class Product(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='products/')
    categories = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.name_uz


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_colors/')

    def __str__(self):
        return self.image.name


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    images = models.ManyToManyField(ProductImage, blank=True, related_name='colors')

    def __str__(self):
        return f"{self.product.name_uz} - {self.name}"

