from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from contacts.models import Contact

#user register
def register(request):
    if request.method == 'POST':
       #get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request, "Username already exists")
                return redirect('register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.error(request, "email is being used")
                    return redirect('register')
                else:
                   user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                   user.save()
                   messages.success(request, 'you ar registered and can log in')
                   return redirect('login')
                   #login after register
                #    auth.login(request,user)
                #    messages.success(request,"Account create successfully! your ar logged in")
                #    return redirect('home')
                    
        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

#user login
def user_login(request):
    if request.method == 'POST': 
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')
    

#user logout
def user_logout(request):
     logout(request)
     return HttpResponseRedirect('/')
    
    
#dashboard
def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts' : user_contacts
    }
    return render(request, 'accounts/dashboard.html',context)
   
