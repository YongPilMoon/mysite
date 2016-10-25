from django.core.mail import send_mail as django_send_mail

from mysite import settings

__all__ = [
    'send_test',
    'send_mail',
]


def send_test():
    django_send_mail(
        'Subject',
        'Message',
        settings.EMAIL_HOST_USER
        ['m71661@gmail.com']
    )


def send_mail(subject, message, recipient_list=None):
    default_recipient_list = ['m71661@gmail.com']
    django_send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list if recipient_list else default_recipient_list
    )