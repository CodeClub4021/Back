from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from .forms import ManagerEditForm 

def choose_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')

        if user_type == 'admin':
            return redirect('choose_method')
        elif user_type == 'coach':
            return redirect('choose_method')
        elif user_type == 'user':
            return redirect('choose_method')
        else:
            return render(request, 'choose.html', {'error_message': 'Invalid selection'})

    return render(request, 'choose.html')

def choose_method(request):
    if request.method == 'POST':
        user_method = request.POST.get('user_method')

        if user_method == 'login':
            return redirect('login')
        elif user_method == 'signup':
            return redirect('signup')
        else:
            return render(request, 'choose_method.html', {'error_message': 'Invalid selection'})

    return render(request, 'choose_method.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('loginsuc'))
    return render(request, 'login.html')

def loginsuc(request):
    return render(request, 'login_success.html')


@login_required
def edit_manager(request):
    if request.method == 'POST':
        form = ManagerEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.cleaned_data['email'] = request.user.email
            form.save()
            return redirect('edit_manager') 
    else:
        form = ManagerEditForm(instance=request.user)
    return render(request, 'edit_manager.html', {'form': form})