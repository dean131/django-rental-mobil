from django.utils import timezone
from decimal import Decimal

from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account.models import User
from .models import Rental, Car
from .forms import RentalModelForm


@login_required(login_url='login_page')
def home(request):
    total_customers = User.objects.filter(is_admin=False).count()
    total_rentals = Rental.objects.filter(Q(status='pending') | Q(status='aktif')).count()
    available_cars = Car.objects.filter(is_booked=False).count()

    context = {
        'name': (request.user.full_name).split()[0],
        'total_customers': total_customers,
        'total_rentals': total_rentals,
        'available_cars': available_cars,
        'menus': {
            'menu': 'homeMenu',
            'submenu': '',
        },
    }
    return render(request, 'home.html', context)


@login_required(login_url='login_page')
def rentals_page(request):
    rentals = Rental.objects.filter(Q(status='pending') | Q(status='aktif')).order_by('status')
    context = {
        'name': (request.user.full_name).split()[0],
        'rentals': rentals,
        'menus': {
            'menu': 'rentalsMenu',
            'submenu': 'retalListMenu',
        },
    }
    return render(request, 'rentals_page.html', context)


@login_required(login_url='login_page')
def add_rental(request):
    form = RentalModelForm()

    if request.method == 'POST':
        car_id = request.POST.get('car')
        car = Car.objects.get(id=car_id)
        if car.is_booked == False:
            form = RentalModelForm(request.POST)
            if form.is_valid():
                car.is_booked = True
                car.save()
                form.save()
                return redirect('rentals_page')
        else:
            messages.error(
                request=request, 
                message='The car is currently being booked by another user.', 
                extra_tags='danger'
            )
    
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
def delete_rental(request, pk):
    rental = Rental.objects.get(id=pk)

    if request.method == 'POST':
        rental.car.is_booked = False
        rental.car.save()
        rental.delete()
        return redirect('rentals_page')
    context ={
        'rental': rental,
    }
    return render(request, 'delete_rental.html', context=context)


@login_required(login_url='login_page')
def checkin_rental(request, pk):
    rental = Rental.objects.get(id=pk)

    if request.method == 'POST':
        rental.status = 'aktif'
        rental.save()
        messages.success(request, message='Rental checkin successfully')
        return redirect('rentals_page')
    context ={
        'rental': rental,
    }
    return render(request, 'checkin_rental.html', context=context)


@login_required(login_url='login_page')
def checkout_rental(request, pk):
    rental = Rental.objects.get(id=pk)

    if request.method == 'POST':
        rental.status = 'selesai'
        rental.check_out_date = timezone.now().date()
        rental.car.is_booked = False
        rental.car.save()
        rental.save()
        messages.success(request, "Rental Checked Out.")
        return redirect('rentals_page')
    
    late_fee = 0
    if timezone.now().date() > rental.end_date:
        days = (timezone.now().date() - rental.end_date).days
        late_fee = int(days * (Decimal(0.02) * rental.total_cost))

    context = {
        'rental': rental,
        'late_fee': late_fee,
    }    
    return render(request, 'checkout_rental.html', context)


@login_required(login_url='login_page')
def checked_out_rentals_page(request):
    rentals = Rental.objects.filter(status='selesai').order_by('status')
    context = {
        'name': (request.user.full_name).split()[0],
        'rentals': rentals,
        'menus': {
            'menu': 'rentalsMenu',
            'submenu': 'checkedOutRentalsMenu',
        },
    }
    return render(request, 'checked_out_rentals_page.html', context)


@login_required(login_url='login_page')
def cars_page(request):
    cars = Car.objects.all()
    context = {
        'cars': cars,
        'name': str(request.user).split()[0],
        'menus': {
            'menu': 'carsMenu',
            'submenu': '',
        },
    }
    return render(request, 'cars_page.html', context)


@login_required(login_url='login_page')
def users_page(request):
    users = User.objects.filter(is_admin=False)
    context = {
        'users': users,
        'name': str(request.user).split()[0],
        'menus': {
            'menu': 'usersMenu',
            'submenu': '',
        },
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