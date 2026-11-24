
from flask import Flask, request, redirect, render_template_string, jsonify
from alert_service import AlertService
from threading import Thread
import time

app = Flask(__name__)
service = AlertService()

PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Elderly Care Monitoring</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #f0f5f9;
    color: #183347;
}

header {
    background: linear-gradient(120deg, #102f46, #116b73);
    color: white;
    padding: 30px 6%;
}

header h1 {
    margin: 0 0 8px;
    font-size: 30px;
}

header p {
    margin: 0;
    color: #c8e5e8;
    font-size: 14px;
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 15px;
}

.online {
    background: #ffffff20;
    padding: 10px 18px;
    border-radius: 30px;
    font-size: 13px;
}

.dot {
    display: inline-block;
    width: 9px;
    height: 9px;
    background: #5ee6a8;
    border-radius: 50%;
    margin-right: 7px;
}

main {
    max-width: 1250px;
    margin: 30px auto;
    padding: 0 25px;
}

.overview {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}

.overview h2 {
    margin-bottom: 5px;
}

.subtitle {
    color: #718096;
    font-size: 14px;
    margin-top: 0;
}

.target {
    background: #e0f2f1;
    color: #08756d;
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
}

.stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin: 24px 0;
}

.stat-card {
    background: white;
    padding: 22px;
    border-radius: 12px;
    box-shadow: 0 3px 15px #1833470a;
    border-left: 5px solid;
}

.stat-card span {
    color: #64748b;
    font-size: 14px;
    font-weight: 600;
}

.stat-card h2 {
    font-size: 36px;
    margin: 10px 0 0;
}

.total {
    border-color: #2563eb;
    color: #2563eb;
}

.pending {
    border-color: #e5a023;
    color: #b7791f;
}

.escalated {
    border-color: #dc4545;
    color: #dc4545;
}

.acknowledged {
    border-color: #16a085;
    color: #16a085;
}

.panel {
    background: white;
    padding: 25px;
    border-radius: 14px;
    margin-bottom: 24px;
    box-shadow: 0 3px 15px #1833470a;
}

.panel h2 {
    font-size: 20px;
    margin-top: 0;
    margin-bottom: 6px;
}

.form-row {
    display: flex;
    align-items: flex-end;
    gap: 18px;
    flex-wrap: wrap;
    margin: 24px 0;
}

.field {
    flex: 1;
    min-width: 150px;
}

label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 8px;
}

input, select {
    width: 100%;
    padding: 12px;
    background: #f8fafc;
    border: 1px solid #d5e0e8;
    border-radius: 8px;
    font-size: 14px;
    color: #183347;
}

input:focus, select:focus {
    outline: 2px solid #75c7c4;
    border-color: #0f766e;
}

button {
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: background 0.2s;
}

.generate {
    background: #0f766e;
    color: white;
    padding: 13px 25px;
    font-size: 14px;
}

.generate:hover {
    background: #115e59;
}

.notice {
    background: #edf7ff;
    border-left: 4px solid #3985c6;
    padding: 13px 16px;
    border-radius: 6px;
    color: #356486;
    font-size: 13px;
}

.error {
    color: #b91c1c;
    font-weight: 600;
}

.table-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
}

.refresh {
    text-decoration: none;
    background: #edf5f6;
    color: #116b73;
    padding: 10px 15px;
    border-radius: 7px;
    font-size: 13px;
    font-weight: 600;
}

.table-wrapper {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    font-size: 14px;
}

th {
    background: #f1f5f9;
    color: #52677a;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

th, td {
    text-align: left;
    padding: 17px 12px;
    border-bottom: 1px solid #e8eef3;
}

tr:hover td {
    background: #f8fafc;
}

.status {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.Pending {
    background: #fff3d6;
    color: #a15c00;
}

.Escalated {
    background: #fee2e2;
    color: #b42318;
}

.Acknowledged {
    background: #d1fae5;
    color: #047857;
}

.ack-button {
    background: #e0f2f1;
    color: #0f766e;
    padding: 9px 13px;
}

.ack-button:hover {
    background: #b2dfdb;
}

.completed {
    color: #16803c;
    font-size: 13px;
}

.empty {
    text-align: center;
    color: #94a3b8;
    padding: 40px;
}

footer {
    text-align: center;
    padding: 20px;
    color: #8494a5;
    font-size: 12px;
}

@media (max-width: 800px) {
    .stats {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .stats {
        grid-template-columns: 1fr;
    }
    .generate {
        width: 100%;
    }
}
</style>
</head>

<body>

<header>
    <div class="header-content">
        <div>
            <h1>&#9825; Elderly Care Monitoring</h1>
            <p>CASE 61 &bull; Intelligent Caregiver Alert System</p>
        </div>
        <div class="online">
            <span class="dot"></span> System Online
        </div>
    </div>
</header>

<main>

<div class="overview">
    <div>
        <h2>Monitoring Overview</h2>
        <p class="subtitle">Monitor and manage simulated senior alerts</p>
    </div>
    <div class="target">Target Population: 3,000 Seniors</div>
</div>

<div class="stats">

    <div class="stat-card total">
        <span>TOTAL ALERTS</span>
        <h2>{{alerts|length}}</h2>
    </div>

    <div class="stat-card pending">
        <span>PENDING ALERTS</span>
        <h2>{{alerts|selectattr('status','equalto','Pending')|list|length}}</h2>
    </div>

    <div class="stat-card escalated">
        <span>ESCALATED ALERTS</span>
        <h2>{{alerts|selectattr('status','equalto','Escalated')|list|length}}</h2>
    </div>

    <div class="stat-card acknowledged">
        <span>ACKNOWLEDGED</span>
        <h2>{{alerts|selectattr('status','equalto','Acknowledged')|list|length}}</h2>
    </div>

</div>

<section class="panel">

    <h2>Wearable Device Simulator</h2>
    <p class="subtitle">
        Simulate an emergency or medication-related event.
    </p>

    <form method="post" action="/alert">
        <div class="form-row">

            <div class="field">
                <label>Senior ID</label>
                <input name="senior" type="number"
                       min="1" max="3000" value="1" required>
            </div>

            <div class="field">
                <label>Event Type</label>
                <select name="event">
                    <option>Fall</option>
                    <option>Missed medicine</option>
                </select>
            </div>

            <button class="generate">
                + Generate Alert
            </button>

        </div>
    </form>

    <div class="notice">
        <strong>Escalation Policy:</strong>
        Unattended alerts are escalated to a backup caregiver
        after 10 seconds. All notifications are simulated.
    </div>

    {% if error %}
        <p class="error">{{error}}</p>
    {% endif %}

</section>

<section class="panel">

    <div class="table-heading">
        <div>
            <h2>Live Alert History</h2>
            <p class="subtitle">
                Track caregiver responses and alert escalation.
            </p>
        </div>

        <a href="/" class="refresh">
            &#8635; Refresh Dashboard
        </a>
    </div>

    <div class="table-wrapper">
        <table>
            <thead>
                <tr>
                    <th>Alert ID</th>
                    <th>Senior ID</th>
                    <th>Event</th>
                    <th>Status</th>
                    <th>Assigned Caregiver</th>
                    <th>Action</th>
                </tr>
            </thead>

            <tbody>

            {% for a in alerts %}
                <tr>
                    <td>#{{a.id}}</td>
                    <td>{{a.senior}}</td>
                    <td>{{a.event}}</td>

                    <td>
                        <span class="status {{a.status}}">
                            {{a.status}}
                        </span>
                    </td>

                    <td>{{a.recipient}}</td>

                    <td>
                        {% if a.status != 'Acknowledged' %}
                        <form method="post" action="/ack/{{a.id}}">
                            <button class="ack-button">
                                Acknowledge
                            </button>
                        </form>
                        {% else %}
                            <span class="completed">
                                &#10003; Completed
                            </span>
                        {% endif %}
                    </td>
                </tr>

            {% else %}
                <tr>
                    <td colspan="6" class="empty">
                        No alerts recorded. Generate an alert to begin monitoring.
                    </td>
                </tr>
            {% endfor %}

            </tbody>
        </table>
    </div>

</section>

</main>

<footer>
    Elderly Care Monitoring &bull; Case 61 &bull;
    Academic Prototype &bull; Synthetic Data Only
</footer>

<script>
setInterval(() => {
    if (!document.querySelector('input:focus, select:focus')
        && !document.querySelector('.error')) {
        location.reload();
    }
}, 4000);
</script>

</body>
</html>
'''

@app.get('/')
def home():
    return render_template_string(
        PAGE, alerts=service.snapshot(), error=''
    )

@app.post('/alert')
def alert():
    try:
        service.create(
            int(request.form.get('senior', '')),
            request.form.get('event')
        )
    except ValueError as e:
        return render_template_string(
            PAGE, alerts=service.snapshot(), error=str(e)
        ), 400

    return redirect('/')

@app.post('/ack/<int:aid>')
def ack(aid):
    try:
        service.acknowledge(aid)
    except KeyError:
        return 'Unknown alert', 404

    return redirect('/')

@app.get('/health')
def health():
    return jsonify(status='ok')

def worker():
    while True:
        service.escalate()
        time.sleep(0.25)

if __name__ == '__main__':
    Thread(target=worker, daemon=True).start()
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )
