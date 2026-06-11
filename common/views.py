from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
import psutil

from .forms import UserForm
# Create your views here.
            
def logout_view(request):
    logout(request)
    return redirect("common:index")

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인

            return redirect('common:index', permanent=True)
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def resource_monitor(request):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    context = {
        'cpu_usage': cpu_usage,
        'memory_total': memory_info.total,
        'memory_available': memory_info.available,
        'disk_total': disk_usage.total,
        'disk_used': disk_usage.used,
        'disk_free': disk_usage.free,
    }
    return render(request, 'common/resource_monitor.html', context)
    