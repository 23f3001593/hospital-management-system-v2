from celery import Celery
from celery.schedules import crontab
from core.config import Config
from app import create_app

flask_app = create_app()

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=Config.broker_url,
        backend=Config.result_backend,
        include=[
            "core.jobs.doctor_jobs"
        ]
    )
    celery.conf.update(
        timezone=Config.timezone,
        enable_utc=Config.enable_utc
    )
    celery.conf.beat_schedule_filename = Config.celerybeat_schedule_path
    celery.conf.beat_schedule = {
        "update-doctor-slots-weekly": {
            "task": "core.jobs.doctor_jobs.update_doctor_slots",
            "schedule": crontab(hour=23, minute=59, day_of_week="sun")
        }
    }
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(flask_app)