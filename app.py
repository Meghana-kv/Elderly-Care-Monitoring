from flask import Flask, request, redirect, render_template_string, jsonify
from alert_service import AlertService
from threading import Thread
import time
app=Flask(__name__)
service=AlertService()
PAGE='''<!doctype html><html><head><title>Elderly Care Monitoring</title><style>body{font:16px Arial;background:#eef3f8;color:#193047;max-width:1050px;margin:40px auto;padding:20px}section,table{background:white;padding:22px;border-radius:12px;width:100%;box-sizing:border-box}button,input,select{padding:10px;margin:5px;border:1px solid #bac8d5;border-radius:6px}button{background:#185d78;color:white;cursor:pointer}td,th{text-align:left;padding:12px;border-bottom:1px solid #ddd}.Escalated{color:#b42318}.Acknowledged{color:#16803c}.Pending{color:#a15c00}</style></head><body><h1>Elderly Care Monitoring</h1><p>CASE 61 | Alert Service with Escalation | Target: 3,000 seniors</p><section><h2>Wearable device simulator</h2><form method="post" action="/alert"><label>Senior ID <input name="senior" type="number" min="1" max="3000" value="1" required></label><select name="event"><option>Fall</option><option>Missed medicine</option></select><button>Generate alert</button></form><p>Demo: unattended alerts escalate after 10 seconds. All notifications are simulated.</p><p>{{error}}</p></section><h2>Alert dashboard</h2><p>Total: {{alerts|length}} | Pending: {{alerts|selectattr('status','equalto','Pending')|list|length}} | Escalated: {{alerts|selectattr('status','equalto','Escalated')|list|length}} | Acknowledged: {{alerts|selectattr('status','equalto','Acknowledged')|list|length}}</p><table><tr><th>ID</th><th>Senior</th><th>Event</th><th>Status</th><th>Recipient</th><th>Action</th></tr>{% for a in alerts %}<tr><td>{{a.id}}</td><td>{{a.senior}}</td><td>{{a.event}}</td><td class="{{a.status}}">{{a.status}}</td><td>{{a.recipient}}</td><td>{% if a.status!='Acknowledged' %}<form method="post" action="/ack/{{a.id}}"><button>Acknowledge</button></form>{% endif %}</td></tr>{% endfor %}</table><p><a href="/">Refresh dashboard</a></p><script>setTimeout(()=>{if(!document.querySelector('input:focus,select:focus'))location.reload()},4000)</script></body></html>'''
@app.get('/')
def home():
    return render_template_string(PAGE,alerts=service.snapshot(),error='')
@app.post('/alert')
def alert():
    try: service.create(int(request.form.get('senior','')),request.form.get('event'))
    except ValueError as e: return render_template_string(PAGE,alerts=service.snapshot(),error=str(e)),400
    return redirect('/')
@app.post('/ack/<int:aid>')
def ack(aid):
    try: service.acknowledge(aid)
    except KeyError: return 'Unknown alert',404
    return redirect('/')
@app.get('/health')
def health(): return jsonify(status='ok')
def worker():
    while True:
        service.escalate(); time.sleep(0.25)
if __name__=='__main__':
    Thread(target=worker,daemon=True).start()
    app.run(host="127.0.0.1", port=5001, debug=True)
