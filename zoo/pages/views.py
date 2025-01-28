from django.shortcuts import render

# Create your views here.

def Homepage(request):
    return render(request, 'index.html')

def About(request):
    return render(request, 'about.html')

def Conservation(request):
    return render(request, 'conservation.html')

def Animals(request):
    return render(request, 'animals.html')

def Visit(request):
    return render(request, 'visit.html')

def Events(request):
    return render(request, 'events.html')