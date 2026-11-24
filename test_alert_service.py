import pytest
from alert_service import AlertService

def test_fall(): assert AlertService().create(1,'Fall')['status']=='Pending'
def test_medicine(): assert AlertService().create(2,'Missed medicine')['event']=='Missed medicine'
def test_boundary(): assert AlertService().create(3000,'Fall')['senior']==3000
def test_invalid_id():
    with pytest.raises(ValueError): AlertService().create(3001,'Fall')
def test_invalid_event():
    with pytest.raises(ValueError): AlertService().create(1,'Unknown')
def test_duplicate():
    s=AlertService(); assert s.create(1,'Fall')['id']==s.create(1,'Fall')['id']
def test_escalation():
    s=AlertService(); a=s.create(1,'Fall'); s.escalate(a['created']+10); assert a['status']=='Escalated'
def test_acknowledgement():
    s=AlertService(); a=s.create(1,'Fall'); s.acknowledge(a['id']); s.escalate(a['created']+20); assert a['status']=='Acknowledged'
