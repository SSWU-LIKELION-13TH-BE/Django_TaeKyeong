from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import SignUpForm, LoginForm, UserUpdateForm, GuestbookForm
from .models import CustomUser, Guestbook
from main.models import Post

#회원가입 기능
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        user_id = request.POST.get('id')
        if form.is_valid():
            form.save()
            #비밀번호 찾기시에 암호화된 비밀번호가 아닌 실제 비번을 불러와야하기 때문에 따로 필드에 저장시켜줌
            user= CustomUser.objects.get(id=user_id)
            user.raw_password=request.POST.get('password1')
            user.save()
            return redirect('signup') 
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

#로그인 기능
def login_view(request):
    form = LoginForm()  

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']

            #기존 authenticate의 경우 username과 pwd를 바탕으로 유효한 유저인지 검증을 하나, 이 함수를 커스터마이즈하여
            #id와 pwd를 기준으로 유효한 유저인지 검증을 하고 싶어서 다음과 같이 바꿔줌.
            #이 코드에서 사용자가 제출한 id와 pwd가 실제 db에 있는 유저인지 검증
            user = authenticate(request, username=id, password=password)

            print (f'views.py, user: {user}, id: {id}, password: {password}')

            if user is not None:
                #user 변수에 재대로 유저변수가 들어옴 = 로그인 진행시켜!(회원가입을 했던 유저이므로)
                login(request, user)
                # 로그인 성공 후 사용자 정보를 템플릿으로 전달
                return JsonResponse({
                    'id': user.id,
                    'username': user.username,
                    'nickname':user.nickname,
                    'is_authenticated': True,
                    'redirect_url': '/',
                    })
            else:
                #db에 해당하는 유저가 없으면
                return JsonResponse({
                    'error' : '해당하는 유저가 없습니다.',
                    'is_authenticated' : False
                }, status=401)

    return render(request, 'login.html', {'form': form})


#비밀번호 찾기 기능(아이디를 입력하면 그에 해당하는 유저의 비밀번호를 반환해주는 형식)
def password_search(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')  # 폼에서 입력한 id 값을 user_id 변수에 저장
        found_password=""

        try:
            # CustomUser 테이블에 해당 ID가 있는지 확인
            exist_user = CustomUser.objects.get(id=user_id)
            #해당 유저의 비밀번호를 불러옴
            found_password=exist_user.raw_password
        except CustomUser.DoesNotExist:
            messages.error(request, '해당 아이디를 가진 유저가 없습니다.')
    
        return render(request, 'password.html', {'found_password' :found_password})
        
    return render(request,'password.html')

# mypage 구현
@login_required
def update_user_view(request):
    user = request.user
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            updated_user.username = user.username           
            new_password = form.cleaned_data.get('password')
            if new_password:
                updated_user.set_password(new_password)
                # updated_user.raw_password = new_password
            print (f'user name : {updated_user.username}')
            print (f'user nickname : {updated_user.nickname}')
            print (f'user id : {updated_user.id}')
            print (f'user password : {updated_user.password}')
            updated_user.save()
            update_session_auth_hash(request, updated_user)
            messages.success(request, '회원 정보가 성공적으로 수정되었습니다.')
            return redirect('user:mypage')
        else:
            print("invalid form")
            form = UserUpdateForm(instance=user)
        return render(request, 'update_user.html', {'form':form})
    else:
        form = UserUpdateForm(instance=user)
        return render(request, 'update_user.html', {'form':form})


# mypage에 내 게시글 나타나도록
@login_required
def my_posts_view(request):
    user=request.user
    my_posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'my_posts.html', {'posts':my_posts})

# mypage에서 게시글 삭제하기
@login_required
def delete_my_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, '게시글이 삭제되었습니다.')
        return redirect('user:my_posts')

    return render(request, 'user/confirm_delete.html', {'post': post})

# 게시글 수정하기
@login_required
def edit_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        post.postname = request.POST.get('postname')
        post.contents = request.POST.get('contents')
        post.techstack = request.POST.get('techstack')
        post.github = request.POST.get('github')
        if request.FILES.get('mainphoto'):
            post.mainphoto = request.FILES['mainphoto']
        post.save()
        messages.success(request, '게시글이 수정되었습니다.')
        return redirect('user:my_posts')

    return render(request, 'edit_post.html', {
        'post': post,
        'nickname': request.user.nickname
    })

# 방명록
@login_required
def mypage_view(request):
    user = request.user
    form = UserUpdateForm(instance=user)

    # 방명록 작성 처리
    if request.method == 'POST':
        gb_form = GuestbookForm(request.POST)
        if gb_form.is_valid():
            guestbook = gb_form.save(commit=False)
            guestbook.owner = user
            guestbook.writer = request.user
            guestbook.save()
            return redirect('user:mypage')
    else:
        gb_form = GuestbookForm()

    guestbooks = Guestbook.objects.filter(owner=user).order_by('-created_at')

    return render(request, 'mypage.html', {
        'form': form,
        'guestbooks': guestbooks,
        'gb_form': gb_form,
    })
