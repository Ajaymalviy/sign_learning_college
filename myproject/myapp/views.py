from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password


def home(request):
    print(request)
    return render(request, 'index.html')


def about(request):
    return render(request, 'aboutus.html')

def features(request):
    return render(request, 'service.html')

def contactpage(request):
    return render(request, 'con.html')

def back(request):
    return render(request, 'mainnew.html')


from django.contrib.auth.models import User

def signup_view(request):
    print('goodydm')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        print(f"Received: {username}, {password}, {email}")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'registration.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email address is already in use.")
            return render(request, 'registration.html')

        # Hash the password
        hashed_password = make_password(password)

        try:
            # Create a new user
            print('inside try')
            user = User(username=username, password=hashed_password, email=email)
            user.save()
            print('User saved successfully.')

            # Optional: Add a message for successful registration
            messages.success(request, 'Your account has been created successfully!')
            return render(request, 'login.html')  # Redirect to the login page after successful registration
        except Exception as e:
            # Log the exception and show a generic error message
            print(f"Error saving user: {e}")
            messages.error(request, "An error occurred while creating your account. Please try again later.")
            return render(request, 'registration.html')
    return render(request, 'registration.html')

def login_views(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user) 
            messages.success(request, 'You have been successfully logged in.')
            return render(request, 'index.html')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')