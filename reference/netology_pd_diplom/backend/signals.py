from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created

from .models import ConfirmEmailToken, User, Order

new_user_registered = Signal(
    ['user_id'],
)

new_order = Signal(
    ['user_id', 'order_id'],
)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """
    # send an e-mail to the user

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {reset_password_token.user}",
        # message:
        reset_password_token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.send()


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    """
    отправляем письмо с подтвердждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Email Confirmation Token {token.user.email}",
        # message:
        token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [token.user.email]
    )
    msg.send()


@receiver(new_order)
def new_order_signal(user_id, order_id, **kwargs):
    """
    отправляем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    order = Order.objects.get(id=order_id)
    link = '<a href="https://127.0.0.1:8000">Home</a>'
    msg = EmailMultiAlternatives(
        # title:
        f'Заказ сформирован',
        # message:
        f'Номер вашего заказа:  {order.id}.\n\n'
        f'Наш оператор свяжется с вами в ближайшее время для уточнения деталей заказа\n\n'
        f'Изменения статуса заказа можно увидеть в вашем личном кабинете \n\n'
        f'Чтобы перейти на сайт нажмите здесь: http://127.0.0.1:8000\n\n\n'
        f'Спасибо за заказ!',

        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()
