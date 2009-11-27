import django.dispatch
repository_changed = django.dispatch.Signal(providing_args=["current_rev", "previous_rev"])
