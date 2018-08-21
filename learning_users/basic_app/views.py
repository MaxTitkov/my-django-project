from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm


#imports for authenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse



# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

def logout_page(request):
    return render(request, 'basic_App/logout_page.html')

@login_required
def special(request):
    return HttpResponse('Some special page needs the login')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered': registered})
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('logout_page'))

def user_login(request):
    if request.method == 'POST': #the user filled all fields correctly
        username = request.POST.get('username') #the name of input field
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else: #if the account is not active
                return HttpResponse('Account is not active')
        else:
            print('The user is not registered!')
            print('Username: {}; password: {}'.format(username, password))
            return HttpResponse('Invalid login or password')
    else:
        return render(request, 'basic_app/login.html',{})
