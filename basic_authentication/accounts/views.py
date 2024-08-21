from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomUserLoginForm, PaymentPendingForm
from .models import PaymentPending

# Function-based view for user registration
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create and save the new user
            login(request, user)  # Log the user in
            return redirect(reverse_lazy('login'))  # Redirect to the login page after successful signup
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

# Function-based view for user login
def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Change 'home' to an existing URL pattern name
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {'form': form})

# Function-based view for home page and handling PaymentPendingForm
def home_view(request):
    if request.method == 'POST':
        form = PaymentPendingForm(request.POST, request.FILES)
        if form.is_valid():
            payment_pending = PaymentPending(
                name=form.cleaned_data['name'],
                payment_remaining=form.cleaned_data['payment_remaining'],
                payment_due_date=form.cleaned_data['payment_due_date'],
                agreement_policies=form.cleaned_data['agreement_policies'],
                signature=form.cleaned_data['signature']
            )
            payment_pending.save()
            return render(request, 'home.html', {'form': form, 'submitted': True})
    else:
        form = PaymentPendingForm()

    return render(request, 'home.html', {'form': form, 'submitted': False})
