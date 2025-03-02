from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User, MasterAccount
import hashlib

def home(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'status': 'error', 'message': 'Username and password are required!'})

        # Check master account
        try:
            master_account = MasterAccount.objects.get(username=username)
            if master_account.check_password(password):
                request.session['username'] = username
                return JsonResponse({'status': 'success', 'message': 'Login successful!', 'redirect': '/master_menu'})
            return JsonResponse({'status': 'error', 'message': 'Invalid password!'})
        except MasterAccount.DoesNotExist:
            pass

        # Check regular account
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                request.session['username'] = username
                return JsonResponse({'status': 'success', 'message': 'Login successful!', 'redirect': '/main_menu'})
            return JsonResponse({'status': 'error', 'message': 'Invalid password!'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Username not found!'})

    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        pin = request.POST.get('pin')

        if len(username) < 7:
            return JsonResponse({'status': 'error', 'message': 'Username must be longer than 7 characters!'})
        if len(password) < 7:
            return JsonResponse({'status': 'error', 'message': 'Password must be longer than 7 characters!'})
        if not (pin.isdigit() and len(pin) == 4):
            return JsonResponse({'status': 'error', 'message': 'PIN must be a 4-digit integer!'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already taken!'})

        user = User(username=username, pin=pin)
        user.set_password(password)
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Account created successfully!', 'redirect': '/'})

    return render(request, 'register.html')

def main_menu(request):
    if 'username' not in request.session:
        return redirect('/')
    return render(request, 'main_menu.html', {'username': request.session['username']})

def master_menu(request):
    if 'username' not in request.session or request.session['username'] != MasterAccount.objects.first().username:
        return redirect('/')
    return render(request, 'master_menu.html')

def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('/')

def deposit(request):
    if 'username' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized!'})
    username = request.session['username']
    amount = float(request.POST.get('amount'))
    if amount <= 0 or amount > 50000:
        return JsonResponse({'status': 'error', 'message': 'Invalid deposit amount!'})
    user = User.objects.get(username=username)
    user.balance += amount
    user.save()
    return JsonResponse({'status': 'success', 'message': f'Deposited ${amount} successfully!'})

def withdraw(request):
    if 'username' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized!'})
    username = request.session['username']
    pin = request.POST.get('pin')
    amount = float(request.POST.get('amount'))
    user = User.objects.get(username=username)
    if amount <= 0 or amount > user.balance:
        return JsonResponse({'status': 'error', 'message': 'Invalid withdrawal amount!'})
    if pin != user.pin:
        return JsonResponse({'status': 'error', 'message': 'Incorrect PIN!'})
    user.balance -= amount
    user.save()
    return JsonResponse({'status': 'success', 'message': f'Withdrew ${amount} successfully!'})

def balance(request):
    if 'username' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized!'})
    username = request.session['username']
    user = User.objects.get(username=username)
    return JsonResponse({'status': 'success', 'balance': user.balance})