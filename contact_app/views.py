from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserForm
from .models import Profile
from .models import Contact
from .forms import ContactForm




# --- Register ---
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


# --- Login ---
def login_View(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('dashboard')
            else:
                # Invalid credentials
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()

    # 👇 Always return something for GET
    return render(request, 'login.html', {'form': form})


# --- Dashboards ---
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def user_dashboard(request):
    contacts = Contact.objects.all()  # Fetch all contacts
    return render(request, 'dashboard.html', {'contacts': contacts})


def add_contact(request):
    # your add contact logic here
    return render(request, 'add_contact.html')
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('dashboard')  # Redirect to a list view after saving
    else:
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form})




def delete_contact(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    return redirect('dashboard')




def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)  # get the contact object
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # redirect after saving
    else:
        form = ContactForm(instance=contact)  # pre-fill existing data
    
    return render(request, 'edit.html', {'form': form, 'update': contact})


# --- Logout ---
def logout_view(request):
    logout(request)
    return redirect('login')
