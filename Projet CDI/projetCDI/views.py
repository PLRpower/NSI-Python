from django.shortcuts import render, redirect
from .models import Livre


def home(request):
    books = Livre.objects.all()
    return render(request, 'home.html', {'books': books})


def add(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        pub_date = request.POST['pub_date']
        Livre.objects.create(title=title, author=author, pub_date=pub_date)
        return redirect('home')

    return render(request, "add.html")


def remove(request, isbn):
    if request.method == 'POST':
        livre = Livre.objects.get(pk=isbn)
        livre.delete()
    return redirect('home')


def login(request):
    return render(request, 'login.html')
