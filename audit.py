import os
import platform
import shutil
import psutil
import json

# 1. Collecte des métriques brutes
total, used, free = shutil.disk_usage("/")
ram = psutil.virtual_memory()
current_user = os.getenv("USER")
disk_usage_percent = (used / total) * 100

# 2. Algorithme du Security Score (Base de 100)
security_score = 100
findings = []

# Règle 1 : Vérification de l'utilisateur Root
if current_user == "root":
    security_score -= 30
    findings.append("[CRITICAL] Script executed as ROOT user. High risk of privilege escalation.")
else:
    findings.append("[OK] Script executed as standard user.")

# Règle 2 : Seuil critique du disque dur
if disk_usage_percent > 90:
    security_score -= 20
    findings.append(f"[HIGH] Disk usage is critical ({disk_usage_percent:.1f}%). Risk of log blackouts.")
else:
    findings.append(f"[OK] Disk usage is safe ({disk_usage_percent:.1f}%).")

# Règle 3 : Seuil critique de la RAM
if ram.percent > 90:
    security_score -= 20
    findings.append(f"[HIGH] RAM utilization is dangerously high ({ram.percent}%).")
else:
    findings.append(f"[OK] RAM utilization is safe ({ram.percent}%).")

# 3. Structuration du rapport JSON final
report = {
    "hostname": platform.node(),
    "user": current_user,
    "system": platform.platform(),
    "metrics": {
        "disk_used_percent": round(disk_usage_percent, 2),
        "ram_used_percent": ram.percent,
        "cpu_cores": psutil.cpu_count()
    },
    "security_audit": {
        "score": max(0, security_score),  # Empêche un score négatif
        "summary": "SECURE" if security_score >= 80 else "WARNING" if security_score >= 50 else "DANGEROUS",
        "details": findings
    }
}

# Affichage propre dans le terminal pour l'auditeur
print("\n" + "="*40)
print(f"🛡️  LOCAL SECURITY AUDIT REPORT")
print("="*40)
print(json.dumps(report, indent=4))
print("="*40)

# Sauvegarde persistante du rapport
with open("report.json", "w") as f:
    json.dump(report, f, indent=4)

print("\n[+] Final audit report with Security Score saved to report.json")
