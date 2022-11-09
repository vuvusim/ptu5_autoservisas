from django.contrib import admin
from . import models


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service', 'quantity', 'price', 'total', 'order')
    ordering = ('order', 'id')
    list_filter = ('order', )


class CarAdmin(admin.ModelAdmin):
    list_display = ('car_model', 'plate', 'vin', 'client')
    list_filter = ('client', 'car_model')
    search_fields = ('plate', 'vin')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class OrderLineInLine(admin.TabularInline):
    model = models.OrderLine
    extra = 0
    can_delete = False


class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date')
    inlines = (OrderLineInLine, )
    readonly_fields = ('date', )

    fieldsets = (
        ('General', {'fields': ('car', )}), 
        ('Date', {'fields': ('date', )})
    )


admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)