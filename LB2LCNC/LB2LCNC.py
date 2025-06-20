import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import datetime

# Konfiguration
HOST = '0.0.0.0'
PORT = 23
LOG_FILE = "lightburn_log.txt"
PROGRAM_FILE = "lightburn_program.ngc"

class GCodeServer:
    def __init__(self, gui_callback, gui_quit):
        self.gui_callback = gui_callback
        self.gui_quit = gui_quit
        self.running = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(1.0)
        self.thread = threading.Thread(target=self.run_server, daemon=True)
        self.thread.start()

    def run_server(self):
        try:
            self.server.bind((HOST, PORT))
            self.server.listen(1)
            self.gui_callback(f"[TCP] Warte auf Verbindung auf {HOST}:{PORT} ...")
            while self.running:
                try:
                    self.conn, self.addr = self.server.accept()
                    self.gui_callback(f"[TCP] Verbunden mit {self.addr}")
                    self.conn.settimeout(1.0)
                    self.conn.sendall(b"Grbl 1.1f ['$' for help]\r\n")
                    self.gui_callback("→ Grbl 1.1f ['$' for help]")
                    self.handle_connection()
                except socket.timeout:
                    continue
        except Exception as e:
            self.gui_callback(f"[Fehler] {e}")
        finally:
            self.stop()

    def handle_connection(self):
        with open(LOG_FILE, "a") as log, open(PROGRAM_FILE, "w") as program:
            while self.running:
                try:
                    data = self.conn.recv(1024)
                    if not data:
                        break
                    lines = data.decode('utf-8', errors='ignore').split('\n')
                    for line in lines:
                        clean = line.strip()
                        if clean:
                            timestamp = datetime.datetime.now().strftime("[%H:%M:%S] ")
                            self.gui_callback(f"{timestamp}← {clean}")
                            log.write(f"{timestamp}← {clean}\n")
                            if not clean.startswith('?') and not clean.startswith('$'):
                                program.write(clean + "\n")
                                program.flush()
                            self.conn.sendall(b"ok\r\n")
                            self.gui_callback(f"{timestamp}→ ok")
