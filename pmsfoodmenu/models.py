from django.db import models


# Category / Product
class Category(models.Model):
    name_az = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)

    def __str__(self):
        return self.name_az


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name_az = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    description_az = models.TextField()
    description_en = models.TextField()
    description_ru = models.TextField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    vegan = models.BooleanField(default=False)
    halal = models.BooleanField(default=False)
    time = models.IntegerField(help_text="Hazırlanma vaxtı (dəqiqə)")
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.name_az


# Table
class Table(models.Model):
    STATUS_CHOICES = [
        ("empty", "Boş"),
        ("reserved", "Rezerv"),
        ("ordered", "Sifariş"),
        ("waitingFood", "Yemək gözləyir"),
        ("waitingWaite", "Ofisiant gözləyir"),
    ]

    table_num = models.IntegerField(unique=True, help_text="Masanın nömrəsi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="empty")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Table {self.table_num} - {self.get_status_display()}"


# Basket
class Basket(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="baskets")
    note = models.TextField(blank=True, null=True)
    service_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_time = models.IntegerField(default=0, help_text="Ümumi hazırlanma vaxtı (dəqiqə)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Səbət {self.id} ({self.table.table_num}) - {self.total_cost} AZN"


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    # Calculation fields (product-dan çəkilir)
    name_az = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    description_az = models.TextField()
    description_en = models.TextField()
    description_ru = models.TextField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    time = models.IntegerField(help_text="Hazırlanma vaxtı (dəqiqə)")

    def save(self, *args, **kwargs):
        if self.product:
            self.name_az = self.product.name_az
            self.name_en = self.product.name_en
            self.name_ru = self.product.name_ru
            self.description_az = self.product.description_az
            self.description_en = self.product.description_en
            self.description_ru = self.product.description_ru
            self.cost = self.product.cost
            self.time = self.product.time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name_az} x {self.count}"