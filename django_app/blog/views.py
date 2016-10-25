from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages

from .models import Post, Comment
from .forms import PostForm


@login_required
def post_list(request):
    # posts = Post.objects\
    #         .filter(published_date__lte=timezone.now())\
    #         .order_by('published_date')
    user = request.user
    posts = Post.objects\
                .filter(
                    Q(published_date__lte=timezone.now()) &
                    Q(author__pk=user.pk)
                ).order_by('published_date')
    return render(request, 'blog/post_list.html', {'post_list': posts})


@login_required
def post_detail(request, pk):
    # 아래와 같이 쓸 경우, pk값에 해당하는 Post객체가 존재하지 않을 경우
    # DoesNotExist에러 발생
    # post = Post.objects.get(pk=pk)

    # Post객체가 존재하지 않을 경우에는 404Error를 리턴해준다.
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('created_date')
    context ={
        'post': post,
        'comments': comments
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_new(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse("로그인하세요")

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)

        #테스트용
        # data_form_is_valid = form.is_valid()
        # data_title = request.POST['title']
        # data_text = request.POST['text']
        # print(data_title)
        # print(data_text)
        # data_str = '%s : %s (유효검사:%s)' % (
        #     data_title,
        #     data_text,
        #     data_form_is_valid
        #  )
        # return HttpResponse(data_str)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def comment_add(request, post_pk):
    if request.method == 'POST':
        try:
            post = Post.objects.get(pk=post_pk)
            content = request.POST['content']
            author = request.user
        except KeyError:
            return HttpResponse("입력 내용을 확인해 주세요.")
        Comment.objects.create(
            post=post,
            author=author,
            content=content,
        )
        messages.success(request, '댓글이 달렸습니다.')
        return redirect('blog:post_detail', pk=post.pk)
