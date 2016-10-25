from django.contrib.auth import get_user_model
User = get_user_model()

#facebook 사용자 정보를 통해서 이ᇿ증하고 싶다.(facebook로그인에는 email, password가 없기 때문에)
class FacebookBackend:
    def authenticate(self, user_info, token=None):
        try:
            user = User.objects.get(facebook_id=user_info.get('id'))
            return user
        except User.DoesNotExist:
            user = User.objects.create_facebook_user(user_info)
            return user

    def get_user(self, user_id): #reqeust에서 유저를 뽑아주는 역할
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None