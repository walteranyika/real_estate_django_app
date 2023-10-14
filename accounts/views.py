from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth

from contacts.models import Contact


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect("dashboard")
        else:
            messages.error(request, 'Invalid credentials')
            return redirect("login")
    else:
        return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already taken')
                    return redirect('register')

                else:
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name, last_name=last_name)
                    # auth.login(request, user) Login automatically
                    user.save()
                    messages.success(request, 'You are now registered')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do dont match')
            return redirect('register')
    return render(request, 'accounts/register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are now logged out")
    return redirect('index')


def dashboard(request):
    user_id = request.user.id
    contacts = Contact.objects.filter(user_id=user_id)
    context = {
        'contacts': contacts
    }
    return render(request, 'accounts/dashboard.html', context)
