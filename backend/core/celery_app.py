from celery import Celery
from app import create_app

flask_app = create_app()

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config.get("CELERY_BROKER_URL"),
        backend=app.config.get("CELERY_RESULT_BACKEND"),
        include=[
            "core.jobs.doctor_jobs"
        ]
    )
    celery.conf.update(
        app.config,
        timezone="Asia/Kolkata",
        enable_utc=False
    )
    celery.conf.beat_schedule = {
        "update-doctor-slots-weekly": {
            "task": "core.jobs.doctor_jobs.update_doctor_slots",
            "schedule": {"type": "crontab", "hour": 23, "minute": 59, "day_of_week": "sun"}
        }
    }
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(flask_app)