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
    'default': ThreadPoolExecutor(20)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = GeventScheduler(executors=self.executors, job_defaults=self.job_defaults, timezone=self.timezone)
scheduler.start()

def schedule(*args,**kwargs):
    job = scheduler.add_job(*args, **kwargs)
    return job