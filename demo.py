from alert_service import AlertService
import time
s=AlertService(); start=time.perf_counter()
for i in range(1,3001): s.create(i,'Fall' if i%2 else 'Missed medicine')
print('CASE 61 | Synthetic senior simulation')
print('Target: 3000 | Created:',len(s.snapshot()))
print(f'Elapsed: {time.perf_counter()-start:.3f} seconds')
failures=0
for i in range(50):
    try:
        x=AlertService(); a=x.create(i+1,'Fall'); x.escalate(a['created']+10); assert a['status']=='Escalated'
    except Exception: failures+=1
print('Reliability trial: 50 runs')
print('Failures:',failures,'| Failure rate:',failures/50*100,'%')
print('Note: in-memory simulation, not production capacity or clinical reliability.')
