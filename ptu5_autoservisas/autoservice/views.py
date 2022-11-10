from django.shortcuts import render
from django.http import HttpResponse
from . models import CarModel, Car, Service, Order, OrderLine

def index(request):
    # return HttpResponse('Sveiki Atvyke!')
    carmodel_count = CarModel.objects.count()
    car_count = Car.objects.count()
    service_count = Service.objects.count()
    order_count = Order.objects.count()
    orderline_count = OrderLine.objects.count()

    context = {
        'carmodel_count': carmodel_count, 
        'car_count': car_count, 
        'service_count': service_count, 
        'order_count': order_count, 
        'orderline_count': orderline_count
    }

    return render(request, 'autoservice/index.html', context)

