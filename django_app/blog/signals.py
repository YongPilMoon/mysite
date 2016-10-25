from django.db.models.signals import post_save
from blog.models import Comment
from apis.sms import *
from apis.mail import *


def send_comment_mail_sms(sender, instance, **kwargs):
    title = "{}에 댓글이 달렸어요".format(instance.post.title)
    content = "{}에 댓글이 추가 되었습니다.".format(instance.post.title)
    send_sms(content, instance.post.author.phone_number)
    send_mail(title, content)
post_save.connect(send_comment_mail_sms, sender=Comment)