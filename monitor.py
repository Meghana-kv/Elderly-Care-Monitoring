import requests,time,csv
with open('monitor_log.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['timestamp','response_ms','status'])
    for i in range(10):
        start=time.perf_counter()
        try:
            r=requests.get('http://127.0.0.1:5000/health',timeout=3); ms=round((time.perf_counter()-start)*1000,2); status='OK' if r.ok and ms<=500 else 'ALERT'
        except requests.RequestException:
            ms=round((time.perf_counter()-start)*1000,2); status='ALERT'
        row=[time.strftime('%H:%M:%S'),ms,status]; w.writerow(row); f.flush(); print(*row,flush=True); time.sleep(60)
