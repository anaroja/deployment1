# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from models import *
from time import localtime, strftime, gmtime
from datetime import datetime 
# Create your views here.
def index(request):   
    return redirect('/main')

def main(request):
    return render(request, 'main/index.html')

def register(request):
    print request.POST
    result = User.objects.validate_reg(request.POST)
    if result[0]:
        # if true we register
        request.session['user_id'] = result[1].id
        request.session['user_name'] = result[1].name
        return redirect('/')
    else:
        # show errors
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)

        return redirect('/')

def login(request):
    if request.method == 'POST':
        result = User.objects.validate_log(request.POST)
        if result[0]:
            # we login
            request.session['user_id'] = result[1].id
            request.session['user_name'] = result[1].name
            return redirect('/home')
        else:
            # show errors
            for error in result[1]:
                messages.add_message(request, messages.INFO, error)

            return redirect('/')

    return redirect('/')        

def home(request):
    id=request.session['user_id']
    context = {
        "all_quotes" : Quote.objects.exclude(adders=User.objects.get(id=id)),
        "user" : User.objects.get(id=id).name,
        "my_quotes" : User.objects.get(id=id).added_quotes.exclude(created_by=id),
    }

    return render(request,'main/home.html', context)
 

def create(request):
    errors = Quote.objects.quote_validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/home')
    else:
        id = request.session['user_id']
        name = User.objects.get(id = id)
        create_quote = Quote.objects.create(message=request.POST['message'],quoted_by=request.POST['quoted_by'],created_by= name)
        create_quote.adders.add(name)
        return redirect('/home')

def add_quote(request,quote_id):
    this_user = User.objects.get(id = request.session['user_id'])
    this_quote = Quote.objects.get(id=quote_id)
    this_quote.adders.add(this_user)

    return redirect('/home')

def display_quote(request, created_by_id):
    context = {
        'quotes' : Quote.objects.get(id=created_by_id),
        "my_quotes" : User.objects.get(id=created_by_id).created_quotes.all(),
        'count': Quote.objects.filter(created_by=created_by_id).count()
    }
    return render(request,'main/display.html', context)


def remove(request,quote_id):
    userid = request.session['user_id']
    user = User.objects.get(id = userid)
    user.added_quotes.remove(quote_id)
    return redirect('/home')


def logout(request):
    request.session.clear()
    return redirect('/')     

