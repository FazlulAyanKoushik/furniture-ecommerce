import os
import dotenv

from celery import Celery, shared_task
from celery.schedules import crontab

from django.core.management import call_command

# Load .env variables
dotenv.read_dotenv()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectile.settings")

app = Celery("projectile")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


@shared_task
def remove_expire_otps():
    call_command("otpio_tempy")


# Define a periodic task to run the `remove_expire_otps` command every 4 hours
app.conf.beat_schedule = {
    "remove-expire-otps-every-4-hours": {
        "task": "projectile.celeryapp.remove_expire_otps",
        "schedule": crontab(minute=0, hour="*/4"),
    },
}
