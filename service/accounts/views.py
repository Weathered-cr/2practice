from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Главная страница
def home(request):
    return render(request, 'accounts/home.html')

# Вход в систему
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') # Перенаправление после успешного входа
        else:
            messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'accounts/login.html')

# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home') # Перенаправление после успешной регистрации
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})