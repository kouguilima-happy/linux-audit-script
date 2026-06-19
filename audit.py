import os
import platform
import shutil
import psutil
import json


def get_system_info():
    total, used, free = shutil.disk_usage("/")
    ram = psutil.virtual_memory()

    return {
        "hostname": platform.node(),
        "user": os.getenv("USER"),
        "cpu_cores": psutil.cpu_count(),
        "disk_used_percent": round((used / total) * 100, 2),
        "ram_used_percent": ram.percent
    }


def calculate_score(info):
    score = 100
    findings = []

    if info["user"] == "root":
        score -= 30
        findings.append("Running as root")

    if info["disk_used_percent"] > 90:
        score -= 20
        findings.append("Disk usage above 90%")

    if info["ram_used_percent"] > 90:
        score -= 20
        findings.append("RAM usage above 90%")

    return score, findings


info = get_system_info()
score, findings = calculate_score(info)

report = {
    "system_info": info,
    "security_score": score,
    "findings": findings
}

print(json.dumps(report, indent=4))

with open("report.json", "w") as file:
    json.dump(report, file, indent=4)
