from alert_service import AlertService
import time
import csv

service = AlertService()
limit = 100  # milliseconds

print("ELDERLY CARE MONITORING")
print("Response Time Monitoring")
print("-" * 50)

with open("performance_log.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Run", "Response Time (ms)", "Status"])

    for i in range(1, 11):
        start = time.perf_counter()
        service.create(i, "Fall")
        elapsed = (time.perf_counter() - start) * 1000

        status = "NORMAL" if elapsed <= limit else "WARNING"

        print(f"Run {i:02d} | {elapsed:.4f} ms | {status}")
        writer.writerow([i, elapsed, status])

        if i < 10:
            time.sleep(60)

print("-" * 50)
print("Monitoring completed.")
print("Results saved to performance_log.csv")