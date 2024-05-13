from django.core.mail import send_mail

from core.constants import ADMIN_EMAIL


def send_confirmation_code(email, code):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения {code}',
        from_email=ADMIN_EMAIL,
        recipient_list=(email,),
        fail_silently=False,
    )
