import tkinter as tk
from tkinter import scrolledtext
import logging

class DebugConsole(logging.Handler):
    def __init__(self, parent):
        logging.Handler.__init__(self)
        self.parent = parent
        self.create_console()

    def create_console(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Debug Console")
        self.window.geometry("800x600")

        self.text_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, bg="black", fg="white")
        self.text_area.pack(expand=True, fill='both')

        self.text_area.tag_config("DEBUG", foreground="cyan")
        self.text_area.tag_config("INFO", foreground="green")
        self.text_area.tag_config("WARNING", foreground="yellow")
        self.text_area.tag_config("ERROR", foreground="red")
        self.text_area.tag_config("CRITICAL", foreground="red", underline=1)

    def emit(self, record):
        msg = self.format(record)
        self.text_area.insert(tk.END, msg + "\n", record.levelname)
        self.text_area.see(tk.END)

    def clear(self):
        self.text_area.delete(1.0, tk.END)