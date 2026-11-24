import time
from threading import RLock

class AlertService:
    def __init__(self, delay=10):
        self.delay=delay
        self.alerts={}
        self.lock=RLock()
    def create(self, senior, event):
        if not isinstance(senior,int) or isinstance(senior,bool) or not 1<=senior<=3000:
            raise ValueError('Senior ID must be 1–3000')
        if event not in ('Fall','Missed medicine'):
            raise ValueError('Invalid event')
        with self.lock:
            for a in self.alerts.values():
                if a['senior']==senior and a['event']==event and a['status']!='Acknowledged':
                    return a
            a=dict(id=len(self.alerts)+1,senior=senior,event=event,status='Pending',created=time.time(),recipient='Primary caregiver')
            self.alerts[a['id']]=a
            return a
    def acknowledge(self, aid):
        with self.lock:
            self.alerts[aid]['status']='Acknowledged'
    def escalate(self, now=None):
        with self.lock:
            for a in self.alerts.values():
                if a['status']=='Pending' and (time.time() if now is None else now)-a['created']>=self.delay:
                    a.update(status='Escalated',recipient='Backup caregiver')
    def snapshot(self):
        with self.lock:
            return [a.copy() for a in self.alerts.values()]
