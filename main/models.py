from django.db import models
from user.models import CustomUser
from django.utils import timezone
# try
from django.contrib.auth import get_user_model

# 게시글 - 제목(postname), 내용(contents) 넣기
class Post(models.Model):
    postname = models.CharField(max_length=300)
    contents = models.TextField()
    mainphoto = models.ImageField(blank=True, null=True)
    techstack = models.CharField(max_length=100, default='Frontend')
    github = models.CharField(max_length=500, default='https://github.com/')
    view_count = models.PositiveIntegerField(default=0)

    # CustomUSer와의 관계를 설정
    author=models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Many-to-Many 관계 추가 : 'like_users'는 좋아요를 누른 사용자들을 저장
    like_users = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)

    # 게시글의 제목(postman)이 Post object 대신하기
    
    def __str__(self):
        return self.postname

    # 좋아요 수 반환
    def likes_count(self):
        return self.like_users.count()


# 댓글 기능
User = get_user_model()

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')  # 대댓글
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(User, related_name='liked_comments', blank=True)  # 댓글 좋아요

    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f'{self.author} - {self.content[:20]}'