from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from member.forms import SignUpForm
from member.models import MyUser


def signup(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        try:
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            nickname = request.POST['nickname']
            lastname = request.POST['lastname']
            firstname = request.POST['firstname']

        except KeyError:
            return HttpResponse("입력 내용을 다시 확인해 주세요.")

        if password1 != password2:
            print("test")
            return render(request, 'member/signup.html', {'error_message': "check password again"})
        else:
            password = password1

        user = MyUser.objects.create_user(email, lastname, firstname, nickname, password)
        # Model의 테이블 전체에 관한 작업을 할때는 Manager를 이용한다.

        if user is not None:
            auth_login(request, user)
            messages.success(request, '로그인에 성공하였습니다')
            return redirect(next)
        else:
            messages.error(request, '로그인에 실패하였습니다')
            return render(request, 'member/login.html', {})
    else:
        return render(request, 'member/signup.html', {})
