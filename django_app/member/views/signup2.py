from django.core.checks import messages
from django.shortcuts import render, redirect, HttpResponse
from member.forms import SignUpForm
from member.models import MyUser
from django.contrib.auth import login


def signup2(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():  # 형식이 통과된 데이터만 cleaned_data에 들어간다.
            email = form.cleaned_data['email']  # 왜 cleaned_date를 사용하나요?
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            nickname = form.cleaned_data['nickname']

        if password1 != password2:
            return HttpResponse('패스워드가 서로 다릅니다.')

            user = MyUser.objects.create_user(
                email=email,
                last_name=last_name,
                first_name=first_name,
                nickname=nickname,
                password=password1,
            )

            login(request, user)
            messages.info(request, '회원가입 되었습니다')
            return redirect('blog:post_list')
        else:
            context['form'] = form
    else:
        form = SignUpForm()
        context = {
            'form': form,
        }
    return render(request, 'member/signup2.html', context)
