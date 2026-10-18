"""
Quick launcher for the Next-Gen Contact Intelligence Backend Server.
Run this script to launch the FastAPI server with auto-reload.
"""
import sys
import os

# Fix Windows console UTF-8 encoding
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure backend folder is in PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

if __name__ == "__main__":
    import uvicorn
    print("\nStarting PulseCheck.AI Server on http://127.0.0.1:8000")
    print("Interactive Swagger API Docs available at http://127.0.0.1:8000/docs\n")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
