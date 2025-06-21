from django.db import models
from menu.models import MenuItem, Customization
from django.utils import timezone

class Table(models.Model):
    TABLE_STATUS_CHOICES = [
        ('A', 'Available'),
        ('O', 'Occupied'), ]

    table_number = models.CharField(max_length=10, unique=True)
    seat = models.PositiveSmallIntegerField()
    table_status = models.CharField(max_length=1, choices=TABLE_STATUS_CHOICES, default='A')

    def __str__(self):
        return f'{self.table_number}, {self.get_table_status_display()}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('R', 'Received'),
        ('P', 'Preparing'),
        ('C', 'Completed'),
    ]

    table_number = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True)
    # staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R')
    notes = models.TextField(blank=True, null=True)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def __str__(self):
        return f'Order #{self.id}, ({self.get_status_display()})'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customizations = models.ManyToManyField(Customization, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def get_price(self):
        base_price = self.menu_item.price
        if self.pk: #really important cuz as a new instance will pass this instead of going through not existing(uncreated custom)
            for customization in self.customizations.all():
                base_price = base_price + customization.price
        return base_price

    def get_total_price(self):
        return self.get_price() * self.quantity

    def save(self, *args, **kwargs):
        self.unit_price = self.get_price()
        self.line_total = self.get_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"
