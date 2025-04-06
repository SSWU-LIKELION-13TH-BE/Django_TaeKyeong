from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from user.models import CustomUser
from .models import Post

# index.html 페이지를 부르는 index 함수
def index(request):
    return render(request, 'main/index.html')

# blog.html 페이지를 부르는 blog 함수
def blog(request):
    # 모든 Post를 가져와 postlist에 저장
    postList = Post.objects.all()
    return render(request, 'main/blog.html', {'postlist':postList})

# blog의 게시글(posting)을 부르는 posting 함수
def posting(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)을 검색
    post=Post.objects.get(pk=pk)
    # author가 None이 아니면 nickname을 가져오고, None이면 '익명'으로 처리
    nickname = post.author.nickname if post.author else '익명'
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'main/posting.html', {'post': post, 'nickname': nickname})

# new_post 연결 함수
def new_post(request):
    if request.method == 'POST':
        postname = request.POST.get('postname')
        contents = request.POST.get('contents')
        mainphoto = request.FILES.get('mainphoto')
        techstack = request.POST.get('techstack')
        github = request.POST.get('github')
        
        # 로그인된 사용자 정보를 가져와서 author로 저장
        author = request.user

        Post.objects.create(
            postname=postname,
            contents=contents,
            mainphoto=mainphoto,
            techstack=techstack,
            author=author,
            github=github,
        )
        return redirect('/blog/')

    # 로그인된 사용자 닉네임을 템플릿에 전달
    nickname = getattr(request.user, 'nickname')
    return render(request, 'main/new_post.html', {'nickname':nickname})

# 게시글 삭제하는 remove_post 함수 생성
def remove_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog/')
    return render(request, 'main/remove_post.html', {'Post': post})

# 게시글에 좋아요한 사람 중에 pk가 현재 유저의 pk랑 같은 것이 존재하는지 판단
@require_POST
def like_post(request, post_pk):
    if request.user.is_authenticated:
        post=get_object_or_404(Post, pk=post_pk)

        if post.like_users.filter(pk=request.user.pk).exists():
            post.like_users.remove(request.user)
        else:
            post.like_users.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/user/login/')