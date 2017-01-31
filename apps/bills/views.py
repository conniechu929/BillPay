from django.shortcuts import render, redirect, HttpResponse
from .models import User, Bill
from django.contrib import messages

def index(request):
    return render(request, 'bills/index.html')

def process(request):
    if request.method == 'POST':
        kwargs = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'phone_number': request.POST['phone_number'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'confirm_pw': request.POST['confirm_pw']
        }

        user = User.objects.register(**kwargs)

        if user[0] == False:
            for error in user[1]:
                messages.error(request, error)
            return redirect('/')
        elif user[0] == True:
            messages.error(request,'The email address you entered (__) is a VALID email address! Thank you!')
            request.session["first_name"] = user[1].first_name
            return redirect('/books')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        kwargs = {
            'email': request.POST['email'],
            'password': request.POST['password'].encode()
        }
        user = User.objects.login(**kwargs)

        if user[0] == False:
            messages.error(request,user[1])
            return redirect('/')
        elif user[0] == True:
            request.session['user_id'] = user[1].id
            request.session["first_name"] = user[1].first_name
            return redirect('/bills')
        return HttpResponse('Done running')
    else:
        return redirect('/')

def bills(request):
    return render(request, 'bills/bills.html')

def logout(request):
	request.session.clear()
	return redirect('/')
