import os
import platform
import shutil

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
