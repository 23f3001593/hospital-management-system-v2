from celery import Celery
from celery.schedules import crontab
from core.config import Config
from app import create_app

flask_app = create_app()

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND,
        include=[
            "core.jobs.doctor_jobs",
            "core.jobs.patient_jobs"
        ]
    )
    celery.conf.update(
        timezone=Config.CELERY_TIMEZONE,
        enable_utc=Config.CELERY_ENABLE_UTC
    )
    celery.conf.beat_schedule_filename = Config.CELERYBEAT_SCHEDULE_PATH
    celery.conf.beat_schedule = {
        "update_slots_weekly": {
            "task": "core.jobs.doctor_jobs.update_slots",
            "schedule": crontab(hour=23, minute=59, day_of_week="sun")
        },
        "send_reports_monthly": {
            "task": "core.jobs.doctor_jobs.send_reports",
            "schedule": crontab(hour=8, minute=0, day_of_month="1")
        },
        "send_appointment_reminders_daily": {
            "task": "core.jobs.patient_jobs.send_appointment_reminders",
            "schedule": crontab(hour=8, minute=0)
        },
        "delete_stale_appointments_daily": {
            "task": "core.jobs.patient_jobs.delete_stale_appointments",
            "schedule": crontab(hour=23, minute=59)
        }
    }
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(flask_app)