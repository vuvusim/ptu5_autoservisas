from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date

class CarModel(models.Model):
    YEARS_CHOISES = ((metai, str(metai)) for metai in reversed(range(1899, date.today().year+1)))

    make = models.CharField(_("make"), max_length=255)
    model = models.CharField(_("model"), max_length=255)
    year = models.IntegerField(_("year"), choices=YEARS_CHOISES)
    engine = models.CharField(_("engine"), max_length=50)

    def __str__(self) -> str:
        return f'{self.make} - {self.model}, {self.year}'

    class Meta:
        verbose_name = 'car model'
        verbose_name_plural = 'car models'


class Car(models.Model):
    car_model = models.ForeignKey(
        CarModel, 
        verbose_name=_("car model"), 
        on_delete=models.CASCADE, 
        related_name='cars'
    )
    plate = models.CharField(_("license plate"), max_length=50)
    vin = models.CharField(_("VIN number"), max_length=50)
    client = models.CharField(_("client name"), max_length=50)

    class Meta:
        verbose_name = 'car'
        verbose_name_plural = 'cars'

    def __str__(self) -> str:
        return f'{self.car_model.make} - {self.car_model.model}, {self.plate}, {self.client}'


class Service(models.Model):
    name = models.CharField(_("service name"), max_length=255)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    car = models.ForeignKey(
        Car, 
        verbose_name=_("car"), 
        on_delete=models.CASCADE, 
        related_name='order'
    )
    total = models.DecimalField(_("total amount"), max_digits=18, decimal_places=2, default=0)
    date = models.DateField(_("date"), auto_now_add=True)

    
    def get_total(self):
        total = 0
        for line in self.order_lines.all():
            total += line.total
        return total

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.total = self.get_total()
        super().save(self, *args, **kwargs)

    def __str__(self) -> str:
        return f'{self.date}: {self.total}'

class OrderLine(models.Model):
    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"), 
        on_delete=models.CASCADE, 
        related_name='order'
    )
    service = models.ForeignKey(
        Service, 
        verbose_name=_("service name"), 
        on_delete=models.CASCADE, 
        related_name='serice'
    )
    quantity = models.IntegerField(_("quantity"), default=1)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self) -> str:
        return f'{self.service.name}: {self.quantity} x {self.price}'
