from django.shortcuts import render

# Create your views here.


def PDG_view(request):
    return render(request, 'PDG.html')