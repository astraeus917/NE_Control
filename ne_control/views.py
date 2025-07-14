from django.shortcuts import render

def index(request):
    return render(request, 'ne_control/index.html')


