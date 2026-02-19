# frontend/run.py
import subprocess
import sys


def run_frontend():
    """프론트엔드 실행"""
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "localhost"
    ])


if __name__ == "__main__":
    run_frontend()
