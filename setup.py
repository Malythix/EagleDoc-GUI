import os
import sys
import subprocess
import platform

VENV = ".venv"
PYTHON = sys.executable

def run(cmd, **kwargs):
    subprocess.run(cmd, check=True, **kwargs)

def main():
    print("Creating virtual environment...")
    run([PYTHON, "-m", "venv", VENV])

    pip = os.path.join(VENV, "Scripts" if platform.system() == "Windows" else "bin", "pip")

    print("Installing dependencies...")
    run([pip, "install", "-r", "requirements.txt"])

    print("\nSetup complete. Run 'python start.py' to launch the app.")

if __name__ == "__main__":
    main()
