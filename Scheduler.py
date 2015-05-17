__author__ = 'matt'
import HomerHelper
from apscheduler.schedulers.gevent import GeventScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor



street = HomerHelper.getSettingValue('StreetAddress')
city = HomerHelper.getSettingValue('City')
state = HomerHelper.getSettingValue('State')
timezone = HomerHelper.calcTimeZone(street, city, state)

jobstores = {
    'default': MemoryJobStore
}
executors = {
    'default': ThreadPoolExecutor(40)
}
job_defaults = {
    'misfire_grace_time': None,
    'coalesce': True,
    'max_instances': 3
}
scheduler = GeventScheduler(executors=executors, job_defaults=job_defaults, timezone=timezone)
scheduler.start()

def schedule(*args, **kwargs):
    job = scheduler.add_job(*args, **kwargs)
    return job

def KillJob(*args, **kwargs):
    scheduler.remove_job(*args, **kwargs)

def KillScheduler():
    scheduler.shutdown()

def GetJob(*args, **kwargs):
    job = scheduler.get_job(*args, **kwargs)
    return job
