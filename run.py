import subprocess
import sys
import time
import os
import webbrowser

def main():
    print("=" * 65)
    print("  🛡️  Starting FraudShield AI Platform (Backend + Frontend)")
    print("=" * 65)
    
    root_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(root_dir)
    
    # 1. Start FastAPI backend
    print("\n[1/2] Launching FastAPI Backend on http://localhost:8000 ...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=root_dir
    )
    
    time.sleep(3)
    
    # 2. Start Streamlit frontend
    print("[2/2] Launching Streamlit UI on http://localhost:8501 ...")
    frontend_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"],
        cwd=root_dir
    )
    
    print("\n" + "=" * 65)
    print("  ✅ Both services are now RUNNING!")
    print("  👉 Streamlit Dashboard : http://localhost:8501")
    print("  👉 FastAPI API Docs   : http://localhost:8000/docs")
    print("=" * 65)
    print("\nPress Ctrl+C anytime to stop both servers.\n")
    
    time.sleep(2)
    webbrowser.open("http://localhost:8501")
    
    try:
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down FraudShield AI...")
        frontend_proc.terminate()
        backend_proc.terminate()
        print("Done.")

if __name__ == "__main__":
    main()
