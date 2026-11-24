from alert_service import AlertService
import time

service = AlertService(delay=10)

print("=" * 55)
print("CASE 61 - ELDERLY CARE MONITORING")
print("Alert Service with Escalation")
print("=" * 55)

print("\n[TC-01] FALL DETECTION")
fall = service.create(101, "Fall")
print("Senior ID:", fall["senior"])
print("Event:", fall["event"])
print("Status:", fall["status"])
print("Recipient:", fall["recipient"])

print("\n[TC-02] MISSED MEDICINE")
medicine = service.create(102, "Missed medicine")
print("Senior ID:", medicine["senior"])
print("Event:", medicine["event"])
print("Status:", medicine["status"])
print("Recipient:", medicine["recipient"])

print("\n[TC-03] DUPLICATE ALERT DETECTION")
duplicate = service.create(101, "Fall")
print("Original Alert ID:", fall["id"])
print("Duplicate Alert ID:", duplicate["id"])
print("Duplicate prevented:", fall["id"] == duplicate["id"])

print("\n[TC-04] ALERT ESCALATION")
print("Waiting for 10 seconds...")
time.sleep(10)
service.escalate()
print("Status:", fall["status"])
print("Recipient:", fall["recipient"])

print("\n[TC-05] CAREGIVER ACKNOWLEDGEMENT")
service.acknowledge(fall["id"])
print("Alert ID:", fall["id"])
print("Status:", fall["status"])

print("\n[TC-06] INVALID SENIOR ID")
try:
    service.create(3001, "Fall")
except ValueError as error:
    print("Input rejected:", error)

print("\n[TC-07] INVALID EVENT")
try:
    service.create(103, "Unknown")
except ValueError as error:
    print("Input rejected:", error)

print("\n[TC-08] BOUNDARY TESTING")
for senior_id in [1, 3000]:
    alert = service.create(senior_id, "Fall")
    print("Senior ID:", senior_id, "| Status:", alert["status"])

print("\n" + "=" * 55)
print("DEMONSTRATION COMPLETED")
print("=" * 55)