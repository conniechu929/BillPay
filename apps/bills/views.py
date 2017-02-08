from django.shortcuts import render, redirect, HttpResponse
from .models import User, Bill
from django.contrib import messages
import datetime

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
            messages.error(request,'The email address you entered is a VALID email address! Thank you!')
            request.session["first_name"] = user[1].first_name
            return redirect('/bills')
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
    context = {
        "mybills": Bill.objects.filter(user_id = User.objects.get(id = request.session["user_id"])).order_by('date')
    }

    return render(request, 'bills/bills.html', context)


def addBill(request):
    if request.method == 'POST':
        print '************'
        print 'ID: ',request.session["user_id"]
        print 'payday:', request.POST['payday']
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
        print "*"*20
        print kwargs
        print "*"*20
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
