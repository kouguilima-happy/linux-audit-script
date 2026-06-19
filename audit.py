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

# 2. Calcul du Score de Sécurité (Base 100)
security_score = 100
findings = []

# Règle 1 : Vérification de l'utilisateur
if current_user == "root":
    security_score -= 30
    findings.append("[CRITICAL] Executed as root")
else:
    findings.append("[OK] Executed as standard user")

# Règle 2 : Vérification du Disque
if disk_usage_percent > 90:
    security_score -= 20
    findings.append("[HIGH] Disk usage above 90%")
else:
    findings.append("[OK] Disk usage is safe")

# Règle 3 : Vérification de la RAM
if ram.percent > 90:
    security_score -= 20
    findings.append("[HIGH] RAM usage above 90%")
else:
    findings.append("[OK] RAM usage is safe")

# 3. Création du dictionnaire de rapport JSON
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
        "score": max(0, security_score),
        "summary": "SECURE" if security_score >= 80 else "WARNING",
        "details": findings
    }
}

# 4. Affichage dans le terminal et sauvegarde dans le fichier
print(json.dumps(report, indent=4))

with open("report.json", "w") as f:
    json.dump(report, f, indent=4)

print("\nReport saved to report.json")
