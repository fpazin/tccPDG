from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login


# Create your views here.

def register_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('PDG')
    else:
        user_form = UserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})

# def login(request):
#     login_form = AuthenticationForm()
#     if request.method == 'POST':
#         print('login01')
#         login_form = AuthenticationForm(data=request.POST)
#         if login_form.is_valid():
#             print('login02')
#             return redirect('PDG')	    
#     return render(request, 'login.html', {'login_form': login_form})

def login_view(request):
    login_form = AuthenticationForm()
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(login(request, user))
                return redirect('PDG')  # Redireciona para a página 'PDG' após o login
    return render(request, 'login.html', {'login_form': login_form})

def logout_view(request):
    logout(request)
    print('logout')	
    return redirect('login')
