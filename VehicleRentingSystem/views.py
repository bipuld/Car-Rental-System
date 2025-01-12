#Created by Yash
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseServerError



def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)



def trigger_500_error(request):
  
    raise Exception("This is a test 500 error.")