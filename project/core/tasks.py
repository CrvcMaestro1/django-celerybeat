import random

import celery
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")


@shared_task
def send_email_report():
    call_command("email_report", )


# @shared_task(bind=True)
# def task_process_notification(self):
#     try:
#         if not random.choice([0, 1]):
#             # mimic random error
#             raise Exception('Random error')
#         requests.post('https://httpbin.org/delay/5')
#     except Exception as e:
#         logger.error('exception raised, it would be retry after 5 seconds')
#         raise self.retry(exc=e, countdown=5)


# # Auto retry
# @shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 7, 'countdown': 5})
# def task_process_notification(self):
#     if not random.choice([0, 1]):
#         # mimic random error
#         raise Exception()
#     requests.post('https://httpbin.org/delay/5')

# # Exponential backoff
# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
# def task_process_notification(self):
#     if not random.choice([0, 1]):
#         # mimic random error
#         raise Exception()
#     requests.post('https://httpbin.org/delay/5')


# # Retry jitter to prevent thundering herd
# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_jitter=True,
#              retry_kwargs={'max_retries': 5})
# def task_process_notification(self):
#     if not random.choice([0, 1]):
#         # mimic random error
#         raise Exception()
#
#     requests.post('https://httpbin.org/delay/5')

class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True
    retry_jitter = True

    def run(self, *args, **kwargs):
        super().run(self, *args, **kwargs)


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_process_notification(self):
    raise Exception()
