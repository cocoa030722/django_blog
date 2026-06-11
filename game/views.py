import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from .models import MainUser, SubUser

# Create your views here.

def index(request):
    main_user = MainUser.objects.all()
    return render(request, 'game/index.html', {'main_user':main_user})
    
@login_required(login_url='/common/login')
def create_game(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        MainUser.objects.create(owner=request.user, choice=choice)
        return redirect('game:index')
    return render(request, 'game/main_user_choice.html')

@login_required(login_url='/common/login')
def sub_user_choice(request, main_pk):
    return render(request, 'game/sub_user_choice.html', {'main_pk':main_pk})

def send_choice(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        main_pk = payload.get('mainPk')
        choice = payload.get('subChoice')
        print('main_pk', main_pk)
        main_user = MainUser.objects.get(pk=main_pk)
        sub_user = SubUser.objects.create(owner=request.user, main_user=main_user, choice=choice)
        
        # 승패 판정 로직
        if sub_user.choice == main_user.choice:
            sub_user.result = 'draw'
        elif (sub_user.choice == 'rock' and main_user.choice == 'scissors') or \
             (sub_user.choice == 'paper' and main_user.choice == 'rock') or \
             (sub_user.choice == 'scissors' and main_user.choice == 'paper'):
            sub_user.result = 'win'
        else:
            sub_user.result = 'lose'
            
        sub_user.save()
        result = {'gameResult':sub_user.result, 'mainUserChoice':main_user.choice, 'subUserChoice':sub_user.choice}
        return JsonResponse(result)
    else:
        return JsonResponse({})

def get_main(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        main_pk = payload.get('mainPk')
        
        main_user = MainUser.objects.get(pk=main_pk)
        result = {'mainUserChoice':main_user.choice}
        return JsonResponse(result)
    else:
        return JsonResponse({})
        
def socket_test(request):
    return render(request, 'game/socket_test.html')