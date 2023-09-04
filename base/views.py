from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Rental, Car
from account.models import User
from .forms import RentalModelForm


@login_required(login_url='login_page')
def home(request):
    total_customers = User.objects.all().count()
    total_rentals = Rental.objects.filter(Q(status='P') | Q(status='A')).count()
    available_cars = Car.objects.filter(is_booked=False).count()

    context = {
        'name': (request.user.full_name).split()[0],
        'page': 'home',
        'total_customers': total_customers,
        'total_rentals': total_rentals,
        'available_cars': available_cars,
    }
    return render(request, 'home.html', context)


@login_required(login_url='login_page')
def rentals_page(request):
    rentals = Rental.objects.all()
    context = {
        'name': (request.user.full_name).split()[0],
        'rentals': rentals,
        'page': 'rental',
    }
    return render(request, 'rentals_page.html', context)


@login_required(login_url='login_page')
def add_rental(request):
    form = RentalModelForm()

    if request.method == 'POST':
        form = RentalModelForm(request.POST)
        if form.is_valid():
            car_id = form.data.get('car')
            car = Car.objects.get(id=car_id)
            car.is_booked = True
            car.save()
            form.save()
            return redirect('rentals_page')
    
    context = {
        'form': form
    }    
    return render(request, 'add_rental.html', context)


@login_required(login_url='login_page')
def edit_rental(request, pk):
    rental = Rental.objects.get(id=pk)
    form = RentalModelForm(instance=rental)

    if request.method == 'POST':
        form = RentalModelForm(data=request.POST, instance=rental)
        if form.is_valid():
            form.save()
            return redirect('rentals_page')
    
    context = {
        'form': form
    }    
    return render(request, 'edit_rental.html', context)


@login_required(login_url='login_page')
def checkout_rental(request, pk):
    rental = Rental.objects.get(id=pk)

    if request.method == 'POST':
        rental.status = 'C'
        rental.check_out_date = datetime.today()
        rental.car.is_booked = False
        rental.car.save()
        rental.save()
        messages.success(request, "Rental Checked Out.")
        return redirect('rentals_page')

    context = {
        'rental': rental
    }    
    return render(request, 'checkout_rental.html', context)

def cars_page(request):
    cars = Car.objects.all()
    context = {
        'cars': cars,
        'page': 'car',
        'name': str(request.user).split()[0]
    }
    return render(request, 'cars_page.html', context)

def users_page(request):
    users = User.objects.filter(is_admin=False)
    context = {
        'users': users,
        'page': 'user',
        'name': str(request.user).split()[0]
    }
    return render(request, 'users_page.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if (user is not None) and (user.is_admin):
            login(request, user)
            return redirect('home')
        messages.error(request, "Invalid user.", extra_tags='danger')

    context = {
        'page': 'login_page'
    }
    return render(request, 'login_page.html', context)

@login_required(login_url='login_page')
def logout_user(requset):
    logout(requset)
    return redirect('login_page')