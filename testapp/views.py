from django.contrib import messages
from testapp.forms import RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

# Home View
#-----------------------------------------------------------------------------------
def home(request):
    context={

    }
    return render(request,'home.html',context)

# register View
#-----------------------------------------------------------------------------------
def registerView(request):
    form=RegisterForm()
    context={
        'form':form
    }
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            print(username)
            messages.success(request,'{}, you have been successfully registered.Please Login !!'.format(username))
            form.save()
            return redirect('testapp:home')
        else:
            username = form.data.get('username')
            email = form.data.get('email')
            first_name = form.data.get('first_name')
            last_name = form.data.get('last_name')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            print(username)
            print(password1)
            print(password2)

            user_exists = User.objects.filter(username=username).exists()
            print(user_exists, 'debuging exist 1')

            if user_exists:
                print("username already exists")
                messages.warning(request,"{}, already exists.. try using another username!\n".format(username))
            
            email_exists= User.objects.filter(email=email).exists()
            if email_exists:
                messages.warning(request, f"{email} is already in use. Please try another email.")
            
            # Check if first and last names are not empty (optional)
            if not first_name:
                messages.warning(request, "First name is required.")
            if not last_name:
                messages.warning(request, "Last name is required.")
            
            if password1 != password2:
                print(password1,password2)
                messages.warning(request," Passwords do not match! !\n")
    
    else:    
      form = RegisterForm()

    context = {
        'form': form
    }
        
    return render(request,'register.html',context)


# login View
#----------------------------------------------------------------------------------
def loginView(request):
    if request.method == "POST":
        print(request.GET ,"DEBUGGING Get")
        print(request.POST ,"DEBUGGING Post")

        username=request.POST.get('username')
        password=request.POST.get('password')

        print(username)
        print(password)

        if not username or not password:
            messages.warning(request, 'Both username and password are required.')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.warning(request, 'The username you entered does not exist.')

        user_auth=authenticate(username=username,password=password)
        print(user_auth)
        if user_auth is not None:
            login(request,user_auth)
            messages.success(request,'{}, you have been successfully logged in !!!'.format(username))
            return redirect('testapp:home')
        else:
            messages.warning(request,'The password you entered is incorrect.Please Try Again !!')
        
    context={

    }
    return render(request,'login.html',context)

# Logout View
#-------------------------------------------------------------------------------------------------------

def logoutView(request):
    current_path=request.path
    print(current_path, "debug1")

    previous_path=request.META.get('HTTP_REFERER')
    print(previous_path)

    if request.method == "POST":
        username=request.user.username
        logout(request)
        messages.success(request," {}, you have been successfully logged out !!".format(username))
        return redirect("testapp:home")
    
    context={
        'previous_path':previous_path
    }

    return render(request,'logout.html',context)