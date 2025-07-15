from django.shortcuts import render

def index(request):
    return render(request, 'ne_control/index.html')

def list(request):
    return render(request, 'ne_control/list.html')

def show(request):
    return render(request, 'ne_control/show.html')

