# Renata x Rico 2CamInput

A production-ready Python desktop application designed to streamline barcode registry validation and physical multi-view image capture stations. 

## 🌟 Core Features

- **Local Secure Authentication:** Replaces hardcoded credentials with a robust SQLite database footprint. New users can securely register accounts directly through the UI, utilizing `bcrypt` hashing for industry-standard credential defense.
- **Hardware Scanner & Webcam Ready:** Configurable to support raw physical handheld barcode scanners interacting over USB, or native webcam QR decoding via the `pyzbar` pipeline.
- **Dual-Camera Capturing Engine:** Utilizes OpenCV MSMF threading to support dual-camera arrays (Left & Right cameras) asynchronously recording precisely mapped views of a product (Front, Back, Top, Bottom, Left, Right).
- **Polished Application UI:** Built entirely in PyQt6, the application features an immersive dark/light mode palette with fading stacked transitions, breathing text input animations, and native geometric graphic indicators that replace jarring popups with seamless inline interfaces.

## 📦 Distribution & Packaging

End-users don't need Python or any development tools installed to use this station software! 
The project includes a `build_exe.bat` script that commands `PyInstaller` to generate a bundled Windows `.exe` application.

### Building the Executable
1. Open the source directory.
2. Double click the `build_exe.bat` script.
3. Wait for compilation. The standalone application will securely package all necessary libraries (like `pyzbar`, `bcrypt`, `opencv`) into the `dist/main` folder. 
4. Launch `dist/main/main.exe`!

## 🧩 Modifying Operation Modes
If you wish to switch the scanner terminal behavior as a developer, you can toggle the global variable in `main.py`:
```python
# main.py
USE_CAMERA_FOR_QR = False  # Set to 'False' for USB Hardware Scanners. 'True' for Webcams.
```

## 🛠️ Developer Environment Requirements
If you are developing or modifying the codebase, you must first pull the repository and synchronize the dependencies:
- Python 3.10+
- `uv` (highly recommended environment manager) or `pip`

**Setup & Running with `uv`:**
```bash
git clone https://github.com/UdayG01/Rico_2Cam_App.git
cd Rico_2Cam_App
uv sync
uv run main.py
```

**First Time Database Initialization:**
The `app_data.db` SQLite database is generated dynamically the first time you execute `main.py`. The root fallback account to access the station initially is always `admin` with password `admin`.
