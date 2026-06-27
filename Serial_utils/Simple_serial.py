import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import serial
import serial.tools.list_ports
import threading
import queue
import time


class SerialTerminal:
    def __init__(self, root):
        self.root = root
        root.title("Serial Terminal")

        self.ser = None
        self.reader_thread = None
        self.read_queue = queue.Queue()
        self.stop_event = threading.Event()

        self._build_ui()
        self._poll_queue()

    def _build_ui(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=6, pady=6)

        ttk.Label(top_frame, text="Port:").pack(side=tk.LEFT)
        self.port_cb = ttk.Combobox(top_frame, width=18, values=self._list_ports())
        self.port_cb.pack(side=tk.LEFT, padx=(4, 8))

        ttk.Button(top_frame, text="Refresh", command=self._refresh_ports).pack(side=tk.LEFT)

        ttk.Label(top_frame, text="Baud:").pack(side=tk.LEFT, padx=(12, 0))
        self.baud_cb = ttk.Combobox(top_frame, width=10, values=["9600","19200","38400","57600","115200","230400"])
        self.baud_cb.set("115200")
        self.baud_cb.pack(side=tk.LEFT, padx=(4, 8))

        self.connect_btn = ttk.Button(top_frame, text="Connect", command=self._toggle_connect)
        self.connect_btn.pack(side=tk.LEFT, padx=(8, 0))

        mid_frame = ttk.Frame(self.root)
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=6)

        self.term_text = scrolledtext.ScrolledText(mid_frame, wrap=tk.NONE, height=20, state=tk.DISABLED)
        self.term_text.pack(fill=tk.BOTH, expand=True)

        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=6, pady=6)

        self.send_entry = ttk.Entry(bottom_frame)
        self.send_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.send_entry.bind('<Return>', lambda e: self._send())

        ttk.Button(bottom_frame, text="Send", command=self._send).pack(side=tk.LEFT, padx=(8,0))
        ttk.Button(bottom_frame, text="Clear", command=self._clear).pack(side=tk.LEFT, padx=(6,0))

    def _list_ports(self):
        ports = []
        for p in serial.tools.list_ports.comports():
            ports.append(p.device)
        return ports

    def _refresh_ports(self):
        self.port_cb['values'] = self._list_ports()

    def _toggle_connect(self):
        if self.ser and self.ser.is_open:
            self._disconnect()
        else:
            self._connect()

    def _connect(self):
        port = self.port_cb.get()
        if not port:
            messagebox.showwarning("Port missing", "Please select a COM port.")
            return
        try:
            baud = int(self.baud_cb.get())
        except Exception:
            baud = 115200
        try:
            self.ser = serial.Serial(port, baudrate=baud, timeout=0.5)
        except Exception as e:
            messagebox.showerror("Connection error", str(e))
            return

        self.stop_event.clear()
        self.reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self.reader_thread.start()
        self.connect_btn.config(text="Disconnect")
        self._append_text(f"Connected to {port} @ {baud}\n")

    def _disconnect(self):
        self.stop_event.set()
        if self.reader_thread:
            self.reader_thread.join(timeout=1)
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
        except Exception:
            pass
        self.ser = None
        self.connect_btn.config(text="Connect")
        self._append_text("Disconnected\n")

    def _reader_loop(self):
        while not self.stop_event.is_set() and self.ser and self.ser.is_open:
            try:
                data = self.ser.readline()
                if data:
                    text = data.decode(errors='replace')
                    self.read_queue.put(text)
                else:
                    time.sleep(0.05)
            except Exception as e:
                self.read_queue.put(f"<ERROR reading: {e}>\n")
                break

    def _poll_queue(self):
        try:
            while True:
                line = self.read_queue.get_nowait()
                self._append_text(line)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)

    def _append_text(self, s):
        self.term_text.config(state=tk.NORMAL)
        self.term_text.insert(tk.END, s)
        self.term_text.see(tk.END)
        self.term_text.config(state=tk.DISABLED)

    def _send(self):
        text = self.send_entry.get()
        if not text:
            return
        if not (self.ser and self.ser.is_open):
            messagebox.showwarning("Not connected", "Open a port first.")
            return
        try:
            # send raw bytes (append newline)
            self.ser.write((text + "\n").encode())
            self._append_text(f"> {text}\n")
            self.send_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Send error", str(e))

    def _clear(self):
        self.term_text.config(state=tk.NORMAL)
        self.term_text.delete('1.0', tk.END)
        self.term_text.config(state=tk.DISABLED)

    def close(self):
        self._disconnect()


def main():
    root = tk.Tk()
    app = SerialTerminal(root)
    def on_closing():
        app.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()
