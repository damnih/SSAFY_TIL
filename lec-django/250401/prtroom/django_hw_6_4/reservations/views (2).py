from django.shortcuts import render, redirect
from .models import Reservation
from .forms import ReservationForm

# Create your views here.
def index(request):
    reservations = Reservation.objects.all()
    context = {
        'reservations': reservations
    }
    return render(request, 'reservations/index.html', context)

# def new(request):

#     return render(request, 'reservations/new.html', context)

def create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('reservations:index')
    else:
        form = ReservationForm()
    
    context = {
        'form': form
    }

    return render(request, 'reservations/create.html', context)
        
    
