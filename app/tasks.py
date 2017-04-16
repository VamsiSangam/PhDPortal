from celery.decorators import task, periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.core import serializers

from app.views import send_reminder_to_referees
from app.views import send_text_email


logger = get_task_logger(__name__)


@task(name="send_email_task")
def send_email_task(email, subject, content):
    """ sends an email """
    logger.info("Sent email")
    
    for email in email:
        send_text_email(email, subject, content)
@periodic_task(
    run_every=(crontab(minute='*/1440')),
    name="task_send_reminder_to_referees",
    ignore_result=True
)
def task_send_reminder_to_referees():
    """
    sends reminder to referee automatically after an invitation is sent to remind them to evaluate synopsis 
    """
    send_reminder_to_referees()

    logger.info("task_send_reminder_to_referee")
