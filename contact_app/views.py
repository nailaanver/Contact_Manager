from django.shortcuts import render

# Create your views here.
def contact_manager(request):
    return render(request,'dashboard.html')