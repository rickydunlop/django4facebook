import django.dispatch

facebook_registration = django.dispatch.Signal(providing_args=["user", "django_facebook"])
