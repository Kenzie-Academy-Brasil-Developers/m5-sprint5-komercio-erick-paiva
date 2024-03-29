from django.db import models


class Product(models.Model):
    description = models.CharField(
        max_length=255,
    )
    price = models.FloatField()
    quantity = models.FloatField()
    is_active = models.BooleanField(default=True)
    seller = models.ForeignKey(to="users.User", on_delete=models.CASCADE)
