
import os
import platform
import shutil
import psutil

print("=== Linux Audit Report ===")

print("\nHostname:")
print(platform.node())

print("\nCurrent User:")
print(os.getenv("USER"))

print("\nSystem:")
print(platform.platform())

total, used, free = shutil.disk_usage("/")

print("\nDisk Usage:")
print(f"Total: {total // (2**30)} GB")
print(f"Used : {used // (2**30)} GB")
print(f"Free : {free // (2**30)} GB")

print("\nCPU Cores:")
print(psutil.cpu_count())

ram = psutil.virtual_memory()

print("\nRAM:")
print(f"Total: {ram.total // (1024**3)} GB")
print(f"Used : {ram.used // (1024**3)} GB")
print(f"Available : {ram.available // (1024**3)} GB")



import subprocess

print("\nOpen Ports:")

result = subprocess.run(
    ["ss", "-tuln"],
    capture_output=True,
    text=True
)

print(result.stdout)
