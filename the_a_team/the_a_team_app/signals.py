from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import APIKey

@receiver(post_save, sender=APIKey)
def api_key_created(sender, instance, created, **kwargs):
    if created:
        send_mail(
            '📦[THE-A-TEAM] Here is your API Key',
            f'Your API Key has been generated: \n{instance.key}',
            'from@example.com',
            [instance.email],
            fail_silently=False,
        )
