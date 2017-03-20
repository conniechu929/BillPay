from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Bill
from .models import History
from .models import User
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from .forms import RegisterForm, LoginForm, RegistrationForm, LogForm
import bcrypt
import forms
import datetime
from datetime import datetime

def index(request):
    form = RegisterForm()
    form2 = LoginForm()
    context = { "regForm": form,
                "logForm": form2
                }
    return render(request, "bills/index.html", context)

def process(request):
    try:
        if request.method == "GET":
            return redirect('/')
    except:
        return request.POST

    bound_form = RegistrationForm()

    if request.method == "POST":
        bound_form = RegistrationForm(request.POST or None)

        if bound_form.is_valid():
            user = bound_form.save()
            if user[0] == True:
                request.session['user_id'] = user[1].id
                request.session['first_name'] = user[1].first_name
                print 'USER ID:', request.session['user_id']
            else:
                messages.error(request, "Unable to save user info.")
                return redirect('/')
            return HttpResponseRedirect("/bills")

        else:
            errors = {}
            for key in bound_form.errors:
                print "KEY: ",key
                if key == "first_name" or key == "last_name" or key == "email" or key == "phone_number" or key == "password" or key == "__all__":
                    errors[key] = bound_form.errors[key]

            categories = ['phone_number', 'first_name', 'last_name', 'email', 'password', '__all__']

            for category in categories:
                if category in errors:
                    messages.error(request, errors[category])

            return redirect('/')

        return HttpResponseRedirect('/')

def login(request):
    try:
        if request.method == "GET":
            return redirect('/')
    except:
        return request.POST

    bound_log = LogForm()

    if request.method == "POST":
        bound_log = LogForm(request.POST or None)

        if bound_log.is_valid():
            info = bound_log.find()
            if info[0] == True:
                request.session['user_id'] = info[1].id
                request.session['first_name'] = info[1].first_name
                print 'USER ID:', request.session['user_id']
            else:
                for key in bound_log.errors:
                    print "KEY: ",key
                    if key == "email" or key == "password" or key == "__all__":
                        messages.error(request, bound_log.errors[key])
                        return redirect('/')
            return HttpResponseRedirect("/bills")
        else:
            for key in bound_log.errors:
                print "KEY: ",key
                if key == "email" or key == "password" or key == "__all__":
                    messages.error(request, bound_log.errors[key])
                    return redirect('/')
        return redirect('/')

def bills(request):
    print '*********************'
    lol = History.objects.filter(user_id = request.session["user_id"])
    print lol
    try:
        request.session['user_id']
        try:
            context = {
                "mybills": Bill.objects.filter(user_id = request.session["user_id"]).order_by('date'),
                "past_bills": History.objects.filter(user_id = request.session["user_id"]).order_by('-created_at')
            }
        except:
            context = {}
    except:
        return redirect('/')

    return render(request, 'bills/bills.html', context)


def addBill(request):
    try:
        if request.method == "GET":
            return redirect('/')
    except:
        return request.POST

    if request.method == 'POST':

        # if len(request.POST['times']) >0:
        #     print "TIMES IS LEMGTH IS: "
        #     print len(request.POST['times'])
        # print request.POST.get('undef_times', False)
        kwargs = {
            'user_id': request.session["user_id"],
            'title': request.POST['title'],
            'amount': request.POST['amount'],
            'date': request.POST['date'],
            'payday': request.POST['payday'],
            'link': request.POST['link'],
            'type': request.POST['type'],
            'times': request.POST['times'],
            'undef_times': request.POST.get('undef_times', False)
        }

        bill = Bill.objects.addBill(**kwargs)

        if bill[0] == False:
            for error in bill[1]:
                messages.error(request, error)
            return redirect('/bills')
        elif bill[0] == True:
            return redirect('/bills')
    else:
        return redirect('/bills')

def markBill(request, id):
    try:
        if request.method == "GET":
            return redirect('/')
    except:
        return request.POST

    if request.method == 'POST':
        kwargs = {
            'user_id': request.session["user_id"],
            'bill_id': id,
        }
        bill = Bill.objects.markBill(**kwargs)
        if bill[0] == False:
            for error in bill[1]:
                messages.error(request, error)
            return redirect('/bills')
        elif bill[0] == True:
            return redirect('/bills')
    else:
        return redirect('/bills')


def logout(request):
    request.session.clear()
    return redirect('/')
