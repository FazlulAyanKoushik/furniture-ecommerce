from django.apps import AppConfig


class NotificationioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notificationio"

    def ready(self):
        from notificationio import signals

        from catalogio.models import Product

        from collabio.models import Project

        from newsdeskio.models import NewsdeskPost

        signals.post_save.connect(
            signals.create_notification_for_product, sender=Product
        )
        signals.post_save.connect(
            signals.create_notification_for_project, sender=Project
        )
        signals.post_save.connect(
            signals.create_notification_for_news_event_post, sender=NewsdeskPost
        )
