from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # 기존 소셜 계정이 이미 DB에 있더라도 그냥 넘어가게끔 override
        return