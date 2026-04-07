import sys
import os
import cv2
import numpy as np
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QComboBox, QStackedWidget, QMessageBox,
    QSplitter, QGridLayout, QFrame, QSizePolicy, QProgressBar, QGraphicsOpacityEffect, QCheckBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QVariantAnimation
from PyQt6.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QPen, QBrush
import auth
# --- Developer Settings ---
USE_CAMERA_FOR_QR = False  # Set to False to use a physical barcode scanner (keyboard input)

# --- Light Professional Theme Styling ---
LIGHT_STYLE_SHEET = """
QMainWindow, QStackedWidget > QWidget {
    background-color: #FAFAFA;
    color: #1A1A1A;
    font-family: 'Segoe UI', 'Inter', sans-serif;
}
QWidget {
    color: #1A1A1A;
}
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    padding: 10px;
    color: #1A1A1A;
    font-size: 14px;
}
QLineEdit:focus {
    border: 2px solid #F56E58;
}
QPushButton {
    background-color: #F56E58;
    border: none;
    border-radius: 6px;
    padding: 10px 16px;
    font-weight: 600;
    font-size: 14px;
    color: white;
}
QPushButton:hover {
    background-color: #FF8A75;
}
QPushButton:pressed {
    background-color: #E25B45;
}
QPushButton:disabled {
    background-color: #FCA595;
    color: #FFF2F0;
}
QPushButton[class="secondary"] {
    background-color: #FFFFFF;
    color: #F56E58;
    border: 1px solid #F56E58;
}
QPushButton[class="secondary"]:hover {
    background-color: #FFF2F0;
}
QPushButton[class="secondary"]:pressed {
    background-color: #FCE1DC;
}
QPushButton[class="secondary"]:disabled {
    color: #D1D5DB;
    border: 1px solid #E5E7EB;
    background-color: #F9FAFB;
}
QPushButton[class="delete-btn"] {
    background-color: #ef4444;
    color: white;
    border: none;
}
QPushButton[class="delete-btn"]:hover {
    background-color: #dc2626;
}
QPushButton[class="delete-btn"]:pressed {
    background-color: #b91c1c;
}
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    padding: 8px;
    color: #1A1A1A;
    font-size: 14px;
}
QLabel#title {
    font-size: 26px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 20px;
}
QLabel#header {
    font-size: 16px;
    font-weight: 600;
    color: #374151;
}
"""

# --- Dark Professional Theme Styling ---
DARK_STYLE_SHEET = """
QMainWindow, QStackedWidget > QWidget {
    background-color: #171717;
    color: #e5e7eb;
    font-family: 'Segoe UI', 'Inter', sans-serif;
}
QWidget {
    color: #e5e7eb;
}
QLineEdit {
    background-color: #262626;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 10px;
    color: #e5e7eb;
    font-size: 14px;
}
QLineEdit:focus {
    border: 1px solid #2563eb;
    background-color: #262626;
}
QPushButton {
    background-color: #2563eb;
    border: none;
    border-radius: 6px;
    padding: 10px 16px;
    font-weight: 600;
    font-size: 14px;
    color: white;
}
QPushButton:hover {
    background-color: #3b82f6;
}
QPushButton:pressed {
    background-color: #1d4ed8;
}
QPushButton:disabled {
    background-color: #404040;
    color: #737373;
}
QPushButton[class="secondary"] {
    background-color: #262626;
    color: #e5e7eb;
    border: 1px solid #404040;
}
QPushButton[class="secondary"]:hover {
    background-color: #404040;
}
QPushButton[class="secondary"]:pressed {
    background-color: #525252;
}
QPushButton[class="secondary"]:disabled {
    color: #737373;
    border: 1px solid #404040;
    background-color: #171717;
}
QPushButton[class="delete-btn"] {
    background-color: #ef4444;
    color: white;
    border: none;
}
QPushButton[class="delete-btn"]:hover {
    background-color: #dc2626;
}
QPushButton[class="delete-btn"]:pressed {
    background-color: #b91c1c;
}
QComboBox {
    background-color: #262626;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 8px;
    color: #e5e7eb;
    font-size: 14px;
}
QComboBox:drop-down {
    border: none;
}
QComboBox QAbstractItemView {
    background-color: #262626;
    color: #e5e7eb;
    selection-background-color: #2563eb;
    border: 1px solid #404040;
}
QLabel#title {
    font-size: 26px;
    font-weight: 700;
    color: #f9fafb;
    margin-bottom: 20px;
}
QLabel#header {
    font-size: 16px;
    font-weight: 600;
    color: #e5e7eb;
}
"""

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

THEMES = {
    "light": {
        "stylesheet": LIGHT_STYLE_SHEET,
        "video_bg": "#E5E7EB",
        "qr_display_bg": "#FFFFFF",
        "qr_display_border": "#D1D5DB",
        "qr_display_text": "#1A1A1A",
        "qr_success_border": "#10B981",
        "qr_success_bg": "#ECFDF5",
        "qr_success_text": "#10B981",
        "btn_success_bg": "#10B981",
        "cam_label_text": "#374151",
        "view_container_bg": "#FFFFFF",
        "view_container_border": "#E5E7EB",
        "view_header_text": "#4B5563",
        "logo_img": resource_path("logo-Renata-IoT_1_new2-768x256.png"),
        "del_btn_style": """
            QPushButton {
                background-color: rgba(245, 110, 88, 0.1);
                color: #F56E58;
                border: 1px solid #F56E58;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: rgba(245, 110, 88, 0.2); }
            QPushButton:pressed { background-color: rgba(245, 110, 88, 0.3); }
        """
    },
    "dark": {
        "stylesheet": DARK_STYLE_SHEET,
        "video_bg": "#262626",
        "qr_display_bg": "#262626",
        "qr_display_border": "#404040",
        "qr_display_text": "#e5e7eb",
        "qr_success_border": "#10b981",
        "qr_success_bg": "#064e3b",
        "qr_success_text": "#34d399",
        "btn_success_bg": "#2563eb",
        "cam_label_text": "#a1a1aa",
        "view_container_bg": "#262626",
        "view_container_border": "#404040",
        "view_header_text": "#d4d4d8",
        "logo_img": resource_path("logo-Renata-IoT_1_new2_darkmode.png"),
        "del_btn_style": """
            QPushButton {
                background-color: rgba(239, 68, 68, 0.1);
                color: #ef4444;
                border: 1px solid #ef4444;
                border-radius: 6px;
                padding: 6px 16px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: rgba(239, 68, 68, 0.2); }
            QPushButton:pressed { background-color: rgba(239, 68, 68, 0.3); }
        """
    }
}

# --- UI Components ---
class ScalableImageLabel(QLabel):
    def __init__(self, theme="dark"):
        super().__init__()
        self.theme = theme
        td = THEMES[self.theme]
        self._pixmap = None
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(80, 60)
        self.setStyleSheet(f"background-color: {td['video_bg']}; border: none;")

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        if not self._pixmap.isNull():
            super().setPixmap(self._pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            super().setPixmap(pixmap)

    def resizeEvent(self, event):
        if self._pixmap and not self._pixmap.isNull():
            super().setPixmap(self._pixmap.scaled(event.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        super().resizeEvent(event)

    def clear(self):
        self._pixmap = None
        super().clear()

class PasswordStrengthBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        self.label = QLabel("Strength: None")
        self.label.setStyleSheet("font-size: 12px; font-weight: 500; color: #9ca3af;")
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.bar.setFixedHeight(6)
        self.bar.setTextVisible(False)
        
        layout.addWidget(self.bar)
        layout.addWidget(self.label)
        self.update_strength("")

    def update_strength(self, pwd):
        if not pwd:
            self.bar.setValue(0)
            self.label.setText("Strength: None")
            self.bar.setStyleSheet("QProgressBar { background-color: #374151; border: none; border-radius: 3px; } QProgressBar::chunk { background-color: #374151; border-radius: 3px; }")
            return

        score = 0
        if len(pwd) >= 8: score += 40
        if any(c.isupper() for c in pwd): score += 20
        if any(c.isdigit() for c in pwd): score += 20
        if any(not c.isalnum() for c in pwd): score += 20
        
        self.bar.setValue(score)
        
        if score < 40: 
            color = "#ef4444" # Weak
            text = "Weak (Too short)"
        elif score < 80: 
            color = "#f59e0b" # Mid
            text = "Medium (Add symbols/caps)"
        else: 
            color = "#10b981" # Strong
            text = "Strong"
            
        self.label.setText(f"Strength: {text}")
        self.label.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {color};")
        self.bar.setStyleSheet(f"""
            QProgressBar {{ background-color: #374151; border: none; border-radius: 3px; }}
            QProgressBar::chunk {{ background-color: {color}; border-radius: 3px; }}
        """)

class FadingStackedWidget(QStackedWidget):
    def fade_to_widget(self, widget):
        self.setCurrentWidget(widget)
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        self.anim = QPropertyAnimation(effect, b"opacity")
        self.anim.setDuration(400)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.start()

# --- Camera Thread ---
class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    qr_detected_signal = pyqtSignal(str)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self._run_flag = True
        self.last_frame = None
        self.scan_requested = False

    def request_scan(self):
        self.scan_requested = True

    def run(self):
        try:
            cap = cv2.VideoCapture(self.camera_index, cv2.CAP_MSMF)
            while self._run_flag:
                ret, frame = cap.read()
                if not ret or frame is None or frame.size == 0:
                    continue

                self.last_frame = frame.copy()
                
                # QR Decoding - Only if scan requested
                if self.scan_requested:
                    try:
                        gray = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2GRAY)
                        from pyzbar import pyzbar
                        barcodes = pyzbar.decode(gray)
                        for barcode in barcodes:
                            barcode_data = barcode.data.decode("utf-8")
                            self.qr_detected_signal.emit(barcode_data)
                            self.scan_requested = False # Stop searching after success
                            break
                    except Exception as pyz_e:
                        print(f"PyZbar error: {pyz_e}")
                
                # Convert BGR to RGB for Qt
                try:
                    rgb_image = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()
                    p = qt_image.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio)
                    self.change_pixmap_signal.emit(p)
                except Exception as qt_e:
                    print(f"Image conversion error: {qt_e}")

        except Exception as e:
            import traceback
            print(f"Camera Thread Fatal Error:")
            traceback.print_exc()
        finally:
            if 'cap' in locals() and cap.isOpened():
                cap.release()

    def stop(self):
        self._run_flag = False
        # self.wait() # Removed to prevent UI blocking during async tear-down

# --- Login Page ---
class LoginPage(QWidget):
    login_success = pyqtSignal(str) # Now passes username directly
    register_requested = pyqtSignal()

    def __init__(self, theme="dark"):
        super().__init__()
        self.theme = theme
        td = THEMES[self.theme]
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_label = QLabel()
        logo_pixmap = QPixmap(td['logo_img'])
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaledToWidth(250, Qt.TransformationMode.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
            layout.addSpacing(20)

        title = QLabel("Login")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ef4444; font-weight: 600;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        layout.addWidget(self.error_label)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedWidth(300)
        layout.addWidget(self.username)
        
        layout.addSpacing(5)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFixedWidth(300)
        layout.addWidget(self.password)
        
        self.show_pwd_cb = QCheckBox("👁️ Show Password")
        self.show_pwd_cb.setStyleSheet("color: #9ca3af; font-size: 13px;")
        self.show_pwd_cb.toggled.connect(self.toggle_pwd_visibility)
        layout.addWidget(self.show_pwd_cb)

        self.username.returnPressed.connect(self.check_login)
        self.password.returnPressed.connect(self.check_login)

        layout.addSpacing(15)

        login_btn = QPushButton("Login")
        login_btn.setFixedWidth(300)
        login_btn.clicked.connect(self.check_login)
        layout.addWidget(login_btn)
        
        layout.addSpacing(5)
        
        register_btn = QPushButton("Register New User")
        register_btn.setFixedWidth(300)
        register_btn.setProperty("class", "secondary")
        register_btn.clicked.connect(self.register_requested.emit)
        layout.addWidget(register_btn)

        # Tab Order
        self.setTabOrder(self.username, self.password)
        self.setTabOrder(self.password, self.show_pwd_cb)
        self.setTabOrder(self.show_pwd_cb, login_btn)
        self.setTabOrder(login_btn, register_btn)

        self.setLayout(layout)

    def toggle_pwd_visibility(self, checked):
        if checked:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)

    def check_login(self):
        self.error_label.hide()
        user = self.username.text()
        pwd = self.password.text()
        success, msg = auth.verify_login(user, pwd)
        if success:
            self.password.clear()
            self.username.clear()
            self.login_success.emit(user)
        else:
            self.error_label.setText(msg)
            self.error_label.show()

# --- Register Page ---
class RegisterPage(QWidget):
    registration_success = pyqtSignal()
    back_to_login = pyqtSignal()

    def __init__(self, theme="dark"):
        super().__init__()
        self.theme = theme
        td = THEMES[self.theme]
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_label = QLabel()
        logo_pixmap = QPixmap(td['logo_img'])
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaledToWidth(250, Qt.TransformationMode.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
            layout.addSpacing(20)

        title = QLabel("Register New User")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ef4444; font-weight: 600;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        layout.addWidget(self.error_label)

        self.username = QLineEdit()
        self.username.setPlaceholderText("New Username")
        self.username.setFixedWidth(300)
        layout.addWidget(self.username)
        
        layout.addSpacing(5)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFixedWidth(300)
        layout.addWidget(self.password)
        
        self.pwd_bar = PasswordStrengthBar()
        self.pwd_bar.setFixedWidth(300)
        layout.addWidget(self.pwd_bar)
        self.password.textChanged.connect(self.pwd_bar.update_strength)
        
        layout.addSpacing(5)
        
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password.setFixedWidth(300)
        layout.addWidget(self.confirm_password)

        self.show_pwd_cb = QCheckBox("👁️ Show Password")
        self.show_pwd_cb.setStyleSheet("color: #9ca3af; font-size: 13px;")
        self.show_pwd_cb.toggled.connect(self.toggle_pwd_visibility)
        layout.addWidget(self.show_pwd_cb)

        self.username.returnPressed.connect(self.check_registration)
        self.password.returnPressed.connect(self.check_registration)
        self.confirm_password.returnPressed.connect(self.check_registration)

        layout.addSpacing(15)

        register_btn = QPushButton("Register")
        register_btn.setFixedWidth(300)
        register_btn.clicked.connect(self.check_registration)
        layout.addWidget(register_btn)
        
        layout.addSpacing(5)
        back_btn = QPushButton("Back to Login")
        back_btn.setFixedWidth(300)
        back_btn.setProperty("class", "secondary")
        back_btn.clicked.connect(self.handle_back)
        layout.addWidget(back_btn)

        # Tab Order
        self.setTabOrder(self.username, self.password)
        self.setTabOrder(self.password, self.confirm_password)
        self.setTabOrder(self.confirm_password, self.show_pwd_cb)
        self.setTabOrder(self.show_pwd_cb, register_btn)
        self.setTabOrder(register_btn, back_btn)

        self.setLayout(layout)

    def toggle_pwd_visibility(self, checked):
        state = QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        self.password.setEchoMode(state)
        self.confirm_password.setEchoMode(state)

    def handle_back(self):
        self.error_label.hide()
        self.username.clear()
        self.password.clear()
        self.confirm_password.clear()
        self.back_to_login.emit()

    def check_registration(self):
        self.error_label.hide()
        user = self.username.text()
        pwd = self.password.text()
        confirm_pwd = self.confirm_password.text()
        
        if pwd != confirm_pwd:
            self.error_label.setText("Passwords do not match!")
            self.error_label.show()
            return
            
        success, msg = auth.register_user(user, pwd)
        if success:
            self.username.clear()
            self.password.clear()
            self.confirm_password.clear()
            self.registration_success.emit()
        else:
            self.error_label.setText(msg)
            self.error_label.show()

# --- Drawing Utilities & Animations ---
class BarcodeIconLabel(QLabel):
    def __init__(self, theme_color_hex, width=150, height=100):
        super().__init__()
        self.setFixedSize(width, height)
        self.theme_color = QColor(theme_color_hex)
        
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pen = QPen(self.theme_color)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        
        lines = [ (10, 4), (20, 2), (28, 6), (40, 2), (48, 8), (62, 4), (72, 2), (80, 5), (92, 3), (102, 6), (114, 2), (122, 4), (132, 8) ]
        
        for x, thick in lines:
            line_x = int(x * (width/150))
            pen.setWidth(int(thick * (width/150)))
            painter.setPen(pen)
            painter.drawLine(line_x, 15, line_x, height - 15)
            
        laser_color = QColor("#F56E58")
        laser_pen = QPen(laser_color)
        laser_pen.setWidth(min(4, max(2, int(4 * (width/150)))))
        laser_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(laser_pen)
        painter.drawLine(0, height // 2, width, height // 2)
        
        glow_pen = QPen(QColor(245, 110, 88, 80))
        glow_pen.setWidth(12)
        painter.setPen(glow_pen)
        painter.drawLine(5, height // 2, width - 5, height // 2)
        
        painter.end()
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class PulsingLineEdit(QLineEdit):
    def __init__(self, theme="dark"):
        super().__init__()
        self.theme = theme
        self.anim = QVariantAnimation()
        self.anim.setDuration(1000)
        
        self.base_col = QColor("#404040") if theme == "dark" else QColor("#D1D5DB")
        self.active_col = QColor(245, 110, 88, 180)
        
        self.anim.setStartValue(self.base_col)
        self.anim.setEndValue(self.active_col)
        
        self.anim.setLoopCount(-1)
        self.anim.valueChanged.connect(self._update_style)
        self.anim.start()
        
    def _update_style(self, color):
        bg = "#262626" if self.theme == "dark" else "#FFFFFF"
        text_col = "#e5e7eb" if self.theme == "dark" else "#1A1A1A"
        
        self.setStyleSheet(f"""
            border: 2px solid {color.name(QColor.NameFormat.HexArgb)}; 
            background-color: {bg}; 
            border-radius: 6px; 
            padding: 10px; 
            color: {text_col};
            font-size: 14px;
        """)

# --- QR Scan Page ---
class QRScanPage(QWidget):
    proceed_signal = pyqtSignal(str)

    def __init__(self, theme="dark"):
        super().__init__()
        self.theme = theme
        self.current_qr = ""
        self.init_ui()
        
    def init_ui(self):
        td = THEMES[self.theme]
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if USE_CAMERA_FOR_QR:
            scan_layout = QHBoxLayout()
            self.qr_display = QLineEdit()
            self.qr_display.setPlaceholderText("Scan QR or Enter Code")
            self.qr_display.setFixedWidth(300)
            
            self.scan_btn = QPushButton("Scan QR Code")
            self.scan_btn.clicked.connect(self.request_qr_scan)
            
            scan_layout.addStretch()
            scan_layout.addWidget(self.qr_display)
            scan_layout.addWidget(self.scan_btn)
            scan_layout.addStretch()

            # Camera selector
            self.camera_select = QComboBox()
            self.camera_select.setFixedWidth(300)
            self.refresh_cameras()
            self.camera_select.currentIndexChanged.connect(self.on_camera_changed)

            # Camera Feed
            self.video_label = ScalableImageLabel(self.theme)
            self.video_label.setStyleSheet(f"background-color: {td['video_bg']}; border-radius: 8px;")
            self.video_label.setMinimumSize(400, 300)

            layout.addWidget(self.camera_select, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addSpacing(10)
            layout.addWidget(self.video_label)
            layout.addSpacing(20)
            layout.addLayout(scan_layout)
            
        else:
            base_icon_col = "#e5e7eb" if self.theme == "dark" else "#374151"
            barcode_icon = BarcodeIconLabel(base_icon_col, width=180, height=110)
            layout.addWidget(barcode_icon, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addSpacing(15)
            
            inst_title = QLabel("Waiting for Scanner Input...")
            obj_color = "#f9fafb" if self.theme == "dark" else "#111827"
            inst_title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {obj_color};")
            inst_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            inst_sub = QLabel("Aim your handheld scanner at the product QR/Barcode\nand pull the trigger.")
            inst_sub.setStyleSheet("font-size: 14px; color: #9ca3af;")
            inst_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            layout.addWidget(inst_title)
            layout.addWidget(inst_sub)
            layout.addSpacing(25)
            
            self.qr_display = PulsingLineEdit(self.theme)
            self.qr_display.setPlaceholderText("Scanner output will appear here...")
            self.qr_display.setFixedWidth(350)
            self.qr_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.qr_display.textChanged.connect(self.on_manual_qr_changed)
            self.qr_display.returnPressed.connect(self.on_proceed)
            
            layout.addWidget(self.qr_display, alignment=Qt.AlignmentFlag.AlignCenter)

        self.proceed_btn = QPushButton("Proceed to Capturing Views")
        self.proceed_btn.setFixedWidth(300)
        self.proceed_btn.setEnabled(False)
        self.proceed_btn.clicked.connect(self.on_proceed)
        layout.addSpacing(20)
        layout.addWidget(self.proceed_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def on_manual_qr_changed(self, text):
        td = THEMES[self.theme]
        if text.strip():
            self.proceed_btn.setEnabled(True)
            self.proceed_btn.setStyleSheet(f"background-color: {td['btn_success_bg']}; color: white;")
        else:
            self.proceed_btn.setEnabled(False)
            self.proceed_btn.setStyleSheet("")

    def refresh_cameras(self):
        self.camera_select.clear()
        for index in range(2):
            cap = cv2.VideoCapture(index, cv2.CAP_MSMF)
            if cap.isOpened() and cap.read()[0]:
                self.camera_select.addItem(f"Camera {index}", index)
            cap.release()

    def on_camera_changed(self, index):
        if self.camera_select.count() == 0: return
        cam_idx = self.camera_select.itemData(index)
        if cam_idx is not None:
             self.start_camera(cam_idx)

    def start_camera(self, index):
        self.stop_camera()
        self.video_label.clear()
        self.video_label.setText("Initializing Camera Feed...")
        self.camera_thread = CameraThread(index)
        self.camera_thread.change_pixmap_signal.connect(self.update_image)
        self.camera_thread.qr_detected_signal.connect(self.update_qr)
        self.camera_thread.start()

    def stop_camera(self):
        if hasattr(self, 'camera_thread'):
            self.camera_thread.stop()

    def update_image(self, qt_image):
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def request_qr_scan(self):
        td = THEMES[self.theme]
        self.qr_display.setStyleSheet(f"background-color: {td['qr_display_bg']}; border: 1px solid {td['qr_display_border']}; color: {td['qr_display_text']};")
        self.qr_display.setText("Scanning...")
        if hasattr(self, 'camera_thread'):
            self.camera_thread.request_scan()

    def update_qr(self, data):
        td = THEMES[self.theme]
        self.qr_display.setText(data)
        self.current_qr = data
        self.qr_display.setStyleSheet(f"border: 2px solid {td['qr_success_border']}; background-color: {td['qr_success_bg']}; color: {td['qr_success_text']};")
        self.proceed_btn.setEnabled(True)
        self.proceed_btn.setStyleSheet(f"background-color: {td['btn_success_bg']}; color: white;")

    def on_proceed(self):
        qr_val = self.qr_display.text().strip()
        if qr_val and qr_val != "Scanning...":
            self.stop_camera()
            self.proceed_signal.emit(qr_val)

# --- Capturing Views Page ---
class CaptureStagePage(QWidget):
    reset_signal = pyqtSignal()

    def __init__(self, qr_val, theme="dark"):
        super().__init__()
        self.theme = theme
        self.qr_val = qr_val
        self.views = ["top", "bottom", "front", "right", "back", "left"]
        self.view_labels = {}
        self.delete_btns = {}
        self.captured_views = {v: False for v in self.views}
        self.init_ui()
        self.start_cameras()

    def init_ui(self):
        td = THEMES[self.theme]
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Title / Info Bar
        top_bar = QHBoxLayout()
        info_label = QLabel(f"Capturing Views for QR: {self.qr_val}")
        info_label.setObjectName("header")
        top_bar.addWidget(info_label)
        top_bar.addStretch()

        self.capture_btn = QPushButton()
        self.capture_btn.setFixedWidth(200)
        self.capture_btn.setFixedHeight(40)
        self.capture_btn.clicked.connect(self.capture_current_view)
        top_bar.addWidget(self.capture_btn)
        
        self.reset_btn = QPushButton("Next")
        self.reset_btn.setFixedWidth(200)
        self.reset_btn.setFixedHeight(40)
        self.reset_btn.setProperty("class", "secondary")
        self.reset_btn.clicked.connect(self.on_reset)
        top_bar.addWidget(self.reset_btn)

        main_layout.addLayout(top_bar)

        self.splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 80% Top Pane (Video)
        self.video_widget = QWidget()
        video_layout = QHBoxLayout(self.video_widget)
        video_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left Section (Rotation camera)
        left_cam_layout = QVBoxLayout()
        self.left_video_label = ScalableImageLabel(self.theme)
        self.left_video_label.setStyleSheet(f"background-color: {td['video_bg']}; border-radius: 8px;")
        left_lbl = QLabel("Camera 1")
        left_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_lbl.setStyleSheet(f"font-weight: 600; color: {td['cam_label_text']};")
        left_cam_layout.addWidget(left_lbl)
        left_cam_layout.addWidget(self.left_video_label, 1) # Add stretch factor 1
        
        # Right Section (Top camera)
        right_cam_layout = QVBoxLayout()
        self.right_video_label = ScalableImageLabel(self.theme)
        self.right_video_label.setStyleSheet(f"background-color: {td['video_bg']}; border-radius: 8px;")
        right_lbl = QLabel("Camera 2")
        right_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_lbl.setStyleSheet(f"font-weight: 600; color: {td['cam_label_text']};")
        right_cam_layout.addWidget(right_lbl)
        right_cam_layout.addWidget(self.right_video_label, 1) # Add stretch factor 1
        
        video_layout.addLayout(left_cam_layout)
        video_layout.addLayout(right_cam_layout)
        
        self.splitter.addWidget(self.video_widget)

        # 20% Bottom Pane (Images Grid)
        self.images_widget = QWidget()
        images_layout = QVBoxLayout(self.images_widget)
        images_layout.setContentsMargins(0, 10, 0, 0)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        row, col = 0, 0
        for view in self.views:
            view_container = QFrame()
            view_container.setStyleSheet(f"background-color: {td['view_container_bg']}; border: 1px solid {td['view_container_border']}; border-radius: 6px;")
            vc_layout = QVBoxLayout(view_container)
            vc_layout.setContentsMargins(5, 5, 5, 5)
            
            header = QLabel(f"{view.capitalize()} View")
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setStyleSheet(f"font-weight: 600; color: {td['view_header_text']}; border: none; background: none;")
            header.setFixedHeight(24)
            
            img_label = ScalableImageLabel(self.theme)
            self.view_labels[view] = img_label
            
            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet(td['del_btn_style'])
            del_btn.hide()
            del_btn.setToolTip("Delete this view")
            del_btn.clicked.connect(lambda checked, v=view: self.delete_view(v))
            self.delete_btns[view] = del_btn
            
            vc_layout.addWidget(header)
            vc_layout.addWidget(img_label, 1)
            vc_layout.addWidget(del_btn)
            
            grid_layout.addWidget(view_container, row, col)
            col += 1
            if col > 5:  # All 6 views in one horizontal row
                col = 0
                row += 1

        images_layout.addLayout(grid_layout)
        self.splitter.addWidget(self.images_widget)
        self.splitter.setSizes([640, 160]) # About 80/20 of 800px

        main_layout.addWidget(self.splitter)
        self.setLayout(main_layout)
        self.update_capture_button()

    def start_cameras(self):
        self.camera_thread_left = CameraThread(0)
        self.camera_thread_left.change_pixmap_signal.connect(self.update_left_image)
        self.camera_thread_left.start()

    def camera_thread_right_init(self):
        self.camera_thread_right = CameraThread(1)
        self.camera_thread_right.change_pixmap_signal.connect(self.update_right_image)
        self.camera_thread_right.start()

    def start_cameras(self):
        self.left_video_label.clear()
        self.left_video_label.setText("Initializing Camera 1...")
        self.camera_thread_left = CameraThread(0)
        self.camera_thread_left.change_pixmap_signal.connect(self.update_left_image)
        self.camera_thread_left.start()
        
        self.right_video_label.clear()
        self.right_video_label.setText("Initializing Camera 2...")
        self.camera_thread_right = CameraThread(1)
        self.camera_thread_right.change_pixmap_signal.connect(self.update_right_image)
        self.camera_thread_right.start()

    def stop_cameras(self):
        if hasattr(self, 'camera_thread_left'):
            self.camera_thread_left.stop()
        if hasattr(self, 'camera_thread_right'):
            self.camera_thread_right.stop()

    def update_left_image(self, qt_image):
        self.left_video_label.setPixmap(QPixmap.fromImage(qt_image))

    def update_right_image(self, qt_image):
        self.right_video_label.setPixmap(QPixmap.fromImage(qt_image))

    def get_next_view(self):
        for view in self.views:
            if not self.captured_views[view]:
                return view
        return None

    def update_capture_button(self):
        next_view = self.get_next_view()
        if next_view:
            self.capture_btn.setText(f"Capture View: {next_view.capitalize()}")
            self.capture_btn.setEnabled(True)
        else:
            self.capture_btn.setText("All Views Captured")
            self.capture_btn.setEnabled(False)

    def capture_current_view(self):
        view_name = self.get_next_view()
        if not view_name: return

        if view_name in ("top", "bottom"):
            target_thread = getattr(self, 'camera_thread_left', None)
            cam_label = "Camera 1"
        else:
            target_thread = getattr(self, 'camera_thread_right', None)
            cam_label = "Camera 2"

        if target_thread is None or target_thread.last_frame is None:
            QMessageBox.warning(self, "Warning", f"{cam_label} is not active or no frame captured.")
            return

        today = datetime.date.today().strftime("%Y-%m-%d")
        parent_dir = "Captures"
        target_dir = os.path.join(parent_dir, today, self.qr_val)
        os.makedirs(target_dir, exist_ok=True)

        filepath = os.path.join(target_dir, f"{self.qr_val}_{view_name}.jpg")
        frame = target_thread.last_frame
        
        cv2.imwrite(filepath, frame)
        
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format.Format_RGB888).copy()
        pixmap = QPixmap.fromImage(qt_image)
        self.view_labels[view_name].setPixmap(pixmap)

        self.captured_views[view_name] = True
        self.delete_btns[view_name].show()
        self.update_capture_button()

    def delete_view(self, view_name):
        target_dir = os.path.join("Captures", datetime.date.today().strftime("%Y-%m-%d"), self.qr_val)
        filepath = os.path.join(target_dir, f"{self.qr_val}_{view_name}.jpg")
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError as e:
                print(f"Error deleting file {filepath}: {e}")
                
        self.view_labels[view_name].clear()
        self.captured_views[view_name] = False
        self.delete_btns[view_name].hide()
        self.update_capture_button()

    def on_reset(self):
        self.stop_cameras()
        self.reset_signal.emit()

# --- App Controller ---
class QRApp(QMainWindow):
    def __init__(self, theme="dark"):
        super().__init__()
        self.theme = theme
        self.setWindowTitle("Renata x Rico 2CamInput")
        self.setFixedSize(1100, 800)
        self.setStyleSheet(THEMES[self.theme]['stylesheet'])

        self.stacked_widget = FadingStackedWidget()
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.header_widget = QWidget()
        self.header_widget.setStyleSheet(f"background-color: {THEMES[self.theme]['view_container_bg']}; border-bottom: 1px solid {THEMES[self.theme]['view_container_border']};")
        
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10) 
        
        self.user_label = QLabel("Logged in as:")
        self.user_label.setStyleSheet("font-weight: bold; font-size: 14px; border: none; padding: 0px;")
        
        self.logout_btn = QPushButton("Log Out")
        self.logout_btn.setFixedWidth(100)
        self.logout_btn.setProperty("class", "secondary")
        self.logout_btn.clicked.connect(self.handle_logout)
        
        header_layout.addWidget(self.user_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_btn)
        
        self.header_widget.hide()
        
        self.main_layout.addWidget(self.header_widget)
        self.main_layout.addWidget(self.stacked_widget)
        
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        self.login_page = LoginPage(self.theme)
        self.login_page.login_success.connect(self.show_qr_scan)
        self.login_page.register_requested.connect(self.show_register_page)
        self.stacked_widget.addWidget(self.login_page)
        
        self.register_page = RegisterPage(self.theme)
        self.register_page.back_to_login.connect(self.show_login_page)
        self.register_page.registration_success.connect(self.show_login_page)
        self.stacked_widget.addWidget(self.register_page)

    def show_login_page(self):
        self.header_widget.hide()
        self.stacked_widget.fade_to_widget(self.login_page)

    def show_register_page(self):
        self.header_widget.hide()
        self.stacked_widget.fade_to_widget(self.register_page)

    def handle_logout(self):
        if hasattr(self, 'qr_scan_page'):
            self.qr_scan_page.stop_camera()
        if hasattr(self, 'capture_stage_page'):
            self.capture_stage_page.stop_cameras()
        self.show_login_page()

    def show_qr_scan(self, username=""):
        if username:
            self.user_label.setText(f"Logged in as: {username}")
        self.header_widget.show()
        
        self.qr_scan_page = QRScanPage(self.theme)
        self.qr_scan_page.proceed_signal.connect(self.show_capture_stage)
        self.stacked_widget.addWidget(self.qr_scan_page)
        self.stacked_widget.fade_to_widget(self.qr_scan_page)
        
        if USE_CAMERA_FOR_QR:
            if hasattr(self.qr_scan_page, 'camera_select') and self.qr_scan_page.camera_select.count() > 0:
                cam_idx = self.qr_scan_page.camera_select.itemData(0)
                if cam_idx is not None:
                    self.qr_scan_page.start_camera(cam_idx)
        else:
            self.qr_scan_page.qr_display.setFocus()

    def show_capture_stage(self, qr_val):
        self.capture_stage_page = CaptureStagePage(qr_val, self.theme)
        self.capture_stage_page.reset_signal.connect(self.reset_to_qr_scan)
        self.stacked_widget.addWidget(self.capture_stage_page)
        self.stacked_widget.fade_to_widget(self.capture_stage_page)

    def reset_to_qr_scan(self):
        if hasattr(self, 'capture_stage_page'):
            self.stacked_widget.removeWidget(self.capture_stage_page)
            self.capture_stage_page.deleteLater()
            del self.capture_stage_page
            
        if hasattr(self, 'qr_scan_page'):
            self.qr_scan_page.stop_camera()
            self.stacked_widget.removeWidget(self.qr_scan_page)
            self.qr_scan_page.deleteLater()
            del self.qr_scan_page

        self.show_qr_scan()

    def closeEvent(self, event):
        if hasattr(self, 'qr_scan_page'):
            self.qr_scan_page.stop_camera()
        if hasattr(self, 'capture_stage_page'):
            self.capture_stage_page.stop_cameras()
        event.accept()

if __name__ == "__main__":
    # Initialize the database
    auth.init_db()
    
    app = QApplication(sys.argv)
    # Default to dark theme. 
    app_theme = "dark"
    if len(sys.argv) > 1 and sys.argv[1].lower() in THEMES:
        app_theme = sys.argv[1].lower()
        
    window = QRApp(theme=app_theme)
    app.setWindowIcon(QIcon(resource_path("favicon.png")))
    window.show()
    sys.exit(app.exec())
