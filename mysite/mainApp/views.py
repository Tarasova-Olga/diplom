from django.shortcuts import render

def index(request):
    return render(request, 'mainApp/homePage.html')

def contact(request):
    return render(request, 'mainApp/basic.html', {'values': ['Для вступления в нашу школу серфинга звоните по телефону:', '+375 29 111-22-33']})
