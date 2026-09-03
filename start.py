import os
import subprocess
import platform

VENV = ".venv"

def main():
    uvicorn = os.path.join(VENV, "Scripts" if platform.system() == "Windows" else "bin", "uvicorn")
    subprocess.run([uvicorn, "main:app", "--reload", "--reload-exclude", ".venv/*"])

if __name__ == "__main__":
    main()
