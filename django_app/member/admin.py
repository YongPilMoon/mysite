from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from member.models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = '__all__'


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = '__all__'


class MyUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'id', 'date_joined')
    list_filter = ('is_staff',)
    ordering = ('-date_joined', )
    readonly_fields = ('date_joined', )
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
                'last_name',
                'first_name',
                'nickname',
                'date_joined',
                'is_staff',
                'phone_number',
                'is_facebook_user',
                'facebook_id',
                'img_profile_url',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'email',
                'password1',
                'password2',
                'last_name',
                'first_name',
                'is_staff',
            )
        }),
    )
    add_form = MyUserCreationForm
    form = MyUserChangeForm

admin.site.register(MyUser, MyUserAdmin)
