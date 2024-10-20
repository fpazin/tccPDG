from django.shortcuts import render

# Create your views here.


def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'base.html')

def PDG_view(request):
    return render(request, 'PDG.html')