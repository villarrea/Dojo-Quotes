from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *


def index(request):
    return render(request, "exam_app/index.html")


def process(request):
    print('==========================================')
    register_errors = User.objects.basic_validator(request.POST)
    if len(register_errors) > 0:
        for key, value in register_errors.items():
            messages.error(request, value)
        return redirect ("/")
    else:
        request.session['first_name'] = request.POST['first_name']
        request.session['email'] = request.POST['email']
        first_name_from_form = request.POST["first_name"] 
        last_name_from_form = request.POST["last_name"] 
        email_from_form = request.POST["email"]
        password_from_form = request.POST["password"]
        birthdate_from_form = request.POST['birthdate']
        user = User.objects.create(first_name = first_name_from_form, last_name = last_name_from_form, email = email_from_form, password = password_from_form, birthdate = birthdate_from_form)
        request.session['id'] = user.id
    return redirect("/wall")

def wall(request): 
    try:
        user = User.objects.get(id = request.session['id'])
        quotes = Quote.objects.all()
        favorites = Favorite.objects.all()
        context = {
            "user" : user,
            "quotes" : quotes,
            "favorites" : favorites
        }
        return render(request, "exam_app/wall.html", context)
    except:
        return redirect("/")

def login(request):
    login_errors = User.objects.basic_validator_two(request.POST)
    if len(login_errors) > 0:
        for key, value in login_errors.items():
            messages.error(request, value)
        return redirect ("/")
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['id'] = user.id
        return redirect("/wall")
    # return redirect ("/")


def logout(request):
    del request.session['id']
    return redirect("/")


def post_quote(request):
    quote_errors = Quote.objects.quote_validator(request.POST)
    if len(quote_errors) > 0:
        for key, value in quote_errors.items():
            messages.error(request, value)
        return redirect ("/wall")
    else:
        quote_from_form = request.POST['quote']
        author_from_form = request.POST['author']
        user = User.objects.get(id = request.session['id'])
        Quote.objects.create(message = quote_from_form, author = author_from_form, user = user)
        return redirect("/wall")
    return redirect ("/")

def user_info(request, user_id): 
    try:
        user = User.objects.get(id = user_id)
        quotes = Quote.objects.all()
        favorites = Favorite.objects.all()
        count = Quote.objects.count()
        counts = Quote.objects.filter(user_id = user).count()

        context = {
            "user" : user,
            "quotes" : quotes,
            "favorites" : favorites,
            "count" : count,
            "counts" : counts
        }
        return render(request, "exam_app/user.html", context)
    except:
        return redirect("/")

def add_favorite(request, user_id):
    
    user = User.objects.get(id = request.session["id"])
    author = Quote.objects.get(id = user_id)
    quote = Quote.objects.get(id = user_id)
    comment = Quote.objects.get(id = user_id)

    Favorite.objects.create(user = user, author = author, quote = quote, comment = comment)
    return redirect("/wall")


def remove(request, user_id):
    f = Favorite.objects.get(id = user_id)
    f.delete()
    return redirect("/wall")
    

# def readd(request, user_id):
#     user = User.objects.get(id = request.session["id"])
#     author = Favorite.objects.get(id = user_id)
#     comment = Favorite.objects.get(id = user_id)
#     Favorite.objects.create(user = user, author = author, message = comment)
#     return redirect("/remove")
    