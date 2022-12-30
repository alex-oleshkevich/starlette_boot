import shutil
import subprocess

subprocess.call(["black", "."])
shutil.copy(".env.example", ".env")
