from django.contrib import messages
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import LoginForm, UserForm
from .models import Profile
from .models import Contact
from .models import User
from .forms import ContactForm
from django.contrib.auth.hashers import make_password







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
from django.conf import settings  # 👈 import this at the top

def login_View(request):
    demo_credentials = getattr(settings, "DEMO_CREDENTIALS", [])  # 👈 add this line

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
                return render(
                    request,
                    'login.html',
                    {'form': form, 'error': 'Invalid credentials', 'demo_credentials': demo_credentials}  # 👈 include here
                )
    else:
        form = LoginForm()

    # 👇 Always return something for GET
    return render(request, 'login.html', {'form': form, 'demo_credentials': demo_credentials})  # 👈 and here




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



@login_required
def delete_contact(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    if request.user.is_superuser:
        return redirect('admin_dashboard')  # Redirect admin to admin dashboard
    else:
        return redirect('dashboard') 





@login_required
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            # ✅ Redirect based on user type
            if request.user.is_superuser:
                # add ?section=manage_contact to tell dashboard which section to load
                return redirect('/admin_dashboard/?section=manage_contact')
            else:
                return redirect('dashboard')
    else:
        form = ContactForm(instance=contact)
    
    return render(request, 'edit.html', {'form': form})





def dashboard_content(request):
    total_users = User.objects.count()
    total_contacts = Contact.objects.count()

    context = {
        'total_users': total_users,
        'total_contacts': total_contacts
    }
    return render(request, 'partials/dashboard_content.html',context)
def manage_users(request):
    users = User.objects.all()  # fetch all users
    return render(request, 'partials/manage_users.html', {'users': users})


def manage_contact(request):
    contacts = Contact.objects.all()
    return render(request, 'partials/manage_contact.html', {'contacts': contacts})


# --- Logout ---
def logout_view(request):
    logout(request)
    return redirect('login')







@login_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()

    if request.user.is_superuser:
        url = reverse('admin_dashboard') + '?section=manage_users'
        return redirect(url)
    else:
        return redirect('dashboard')
    
    
    
@login_required
def edit_user(request, pk):
    # Get the user to edit
    user_obj = get_object_or_404(User, pk=pk)

    # Permission check: only superuser or the user themselves can edit
    if not request.user.is_superuser and request.user.pk != user_obj.pk:
        messages.error(request, "You do not have permission to edit this user.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:  # Only update password if provided
                user.password = make_password(password)
            user.save()
            messages.success(request, "User updated successfully!")

            # Redirect based on user type
            if request.user.is_superuser:
                url = reverse('admin_dashboard') + '?section=manage_users'
                return redirect(url)
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserForm(instance=user_obj)
        form.fields['password'].initial = ''
        form.fields['confirm_password'].initial = ''

    return render(request, 'edit_user.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # ✅ Redirect to reset-password page with username
            return redirect('reset_password', username=user.username)
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
    return render(request, 'forgot_password.html')


def reset_password(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user.password = make_password(password)
            user.save()
            messages.success(request, "Password reset successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'reset_password.html', {'username': username})