import os
import platform
import shutil
import psutil
import json

total, used, free = shutil.disk_usage("/")
ram = psutil.virtual_memory()

report = {
    "hostname": platform.node(),
    "user": os.getenv("USER"),
    "system": platform.platform(),
    "disk": {
        "total_gb": total // (2**30),
        "used_gb": used // (2**30),
        "free_gb": free // (2**30)
    },
    "cpu": {
        "cores": psutil.cpu_count()
    },
    "ram": {
        "total_gb": ram.total // (1024**3),
        "used_gb": ram.used // (1024**3),
        "available_gb": ram.available // (1024**3)
    }
}

print(json.dumps(report, indent=4))

with open("report.json", "w") as f:
    json.dump(report, f, indent=4)

print("\nReport saved to report.json")
