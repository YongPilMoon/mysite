from django.db import models
from django.contrib.auth.models import \
    AbstractBaseUser, AbstractUser,\
    BaseUserManager, PermissionsMixin #PermissionsMixin admin을 사용하기위한 클래스


class MyUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            last_name,
            first_name,
            nickname,
            password=None,
            ):
        user = self.model(
            email=email,
            last_name=last_name,
            first_name=first_name,
            nickname=nickname,
        )
        # password를 hashing하는 역할을 한다
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self,
            email,
            last_name,
            first_name,
            nickname,
            password,
            ):
        user = self.model(
            email=email,
            last_name=last_name,
            first_name=first_name,
            nickname=nickname,
        )
        user.set_password(password)

        # True이면 관리자모드로 login가능
        user.is_staff = True

        # True이면 관리자 모드기능을 모두 사용할 수 있다(PermissiontsMixin에서 상속)
        user.is_superuser = True

        user.save()
        return user

    def create_facebook_user(self, user_info):
        user = self.model(
            email=user_info['email'],
            last_name=user_info.get('last_name',''),
            first_name=user_info.get('first_name',''),
            is_facebook_user=True,
            facebook_id=user_info['id'],
            img_profile_url=user_info['picture']['data']['url'],
        )
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=24)
    date_joined = models.DateTimeField(auto_now_add=True, unique=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=50, blank=True)

    # Facebook User
    is_facebook_user = models.BooleanField(default=False)
    facebook_id = models.CharField(max_length=200, blank=True)
    img_profile_url = models.URLField(blank=True)

    # 규약:  username 대신 인증을 위해 사용할 다른 식별자 지정
    USERNAME_FIELD = 'email'

    # superuser를 생성시 입력할 필드 지정
    REQUIRED_FIELDS = ['last_name', 'first_name', 'nickname']

    @property
    def full_name(self):
        return self.get_full_name()

    # CustomUserModel에 맞는 매니저 선언
    objects = MyUserManager()

    def get_full_name(self):
        return '%s%s' % (self.last_name, self.first_name)

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if '-' in self.phone_number:
            self.phone_number = self.phone_number.replace('-', "")
        super().save(*args, **kwargs)
