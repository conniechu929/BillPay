from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
# from .models import Bill
# from .models import User
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from .forms import RegisterForm, LoginForm, RegistrationForm
import bcrypt
import forms

def index(request):
    form = RegisterForm()
    form2 = LoginForm()
    context = { "regForm": form,
                "logForm": form2
                }
    return render(request, "bills/index.html", context)

def process(request):
    bound_form = RegistrationForm()

    if request.method == "POST":
        bound_form = RegistrationForm(request.POST or None)

        if bound_form.is_valid():
            user = bound_form.save()
            if user[0] == True:
                request.session['user_id'] = user[1].id
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
#
# def login(request):
#     # next = request.POST.get('next', request.GET.get('next', ''))
#     # context = {'next': request.GET['next'] if request.GET and 'next' in request.GET else ''}
#     if request.method == 'POST':
#         kwargs = {
#             'email': request.POST['email'],
#             'password': request.POST['password'].encode()
#         }
#         # email = request.POST['email']
#         # password = request.POST['password'].encode()
#         user = authenticate(email=email, password=password)
#         user = User.objects.login(**kwargs)
#         if user[0] == False:
#             messages.error(request,user[1])
#             return redirect('/')
#         elif user[0] == True:
#             request.session['user_id'] = user[1].id
#             request.session["first_name"] = user[1].first_name
#             # if next:
#             #     return HttpResponseRedirect(next)
#             return redirect('/bills')
#             # return redirect(request.POST.get('next','/bills'))
#
#         # if 'next' in request.POST:
#         #     return HttpResponseRedirect(request.POST['next'], '/bills')
#         # else:
#         #     return HttpResponseRedirect('/')
#     else:
#         return redirect('/')

# @login_required(login_url='/')
def bills(request):
    # context = {'next': request.GET['next'] if request.GET and 'next' in request.GET else ''}
    print request.session['user_id']
    return render(request, 'bills/bills.html')



def logout(request):
    request.session.clear()
    return redirect('/')
