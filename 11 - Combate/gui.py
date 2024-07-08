import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import queue
import logging

class DnDChatbotGUI:
    def __init__(self, master, chat_function, process_tool_call):
        self.master = master
        master.title("D&D 5e Combat Simulator Chatbot")

        self.chat_function = chat_function
        self.process_tool_call = process_tool_call

        # Chat window
        self.chat_log = scrolledtext.ScrolledText(master, state='disabled', wrap=tk.WORD)
        self.chat_log.pack(expand=True, fill='both')

        # Configure text tags
        self.chat_log.tag_configure("user", foreground="green")
        self.chat_log.tag_configure("assistant", foreground="black")
        self.chat_log.tag_configure("hit", foreground="blue")
        self.chat_log.tag_configure("damage", foreground="red")
        self.chat_log.tag_configure("narrative", font=("TkDefaultFont", 10, "italic"))

        # Model selection dropdown
        self.model_var = tk.StringVar(value="claude-3-opus-20240229")
        model_label = tk.Label(master, text="Select Model:")
        model_label.pack()
        self.model_dropdown = ttk.Combobox(master, textvariable=self.model_var, 
                                           values=["claude-3-opus-20240229", 
                                                   "claude-3-sonnet-20240229",
                                                   "claude-3-haiku-20240307"])
        self.model_dropdown.pack()

        # Input field
        self.input_field = tk.Entry(master)
        self.input_field.pack(expand=True, fill='x')
        self.input_field.bind("<Return>", self.send_message)

        # Button frame
        button_frame = tk.Frame(master)
        button_frame.pack(fill='x')

        # Send button
        self.send_button = tk.Button(button_frame, text="Send", command=self.send_message)
        self.send_button.pack(side='left', padx=5, pady=5)

        # Exit button
        self.exit_button = tk.Button(button_frame, text="Exit", command=self.exit_program)
        self.exit_button.pack(side='right', padx=5, pady=5)

        self.conversation = []
        self.response_queue = queue.Queue()

        # Display greeting message
        self.display_greeting()

        self.update_chat()

    def display_greeting(self):
        greeting = "Welcome to the D&D 5e Combat Simulator Chatbot!\n"
        greeting += "You can simulate combat between characters or ask questions about D&D.\n"
        greeting += "Select a Claude model from the dropdown menu above.\n"
        greeting += "Type 'exit' or click the Exit button to end the conversation.\n\n"
        self.update_chat_log(greeting, "assistant")

    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if message == "":
            return
        self.input_field.delete(0, tk.END)

        if message.lower() == 'exit':
            self.exit_program()
            return

        self.conversation.append({"role": "user", "content": message})
        self.update_chat_log(message, "user")

        threading.Thread(target=self.get_claude_response, args=(message,)).start()

    def get_claude_response(self, message):
        selected_model = self.model_var.get()
        response = self.chat_function(self.conversation, self.process_tool_call, selected_model)
        if response:
            self.conversation.append({"role": "assistant", "content": response})
            self.response_queue.put(response)
        else:
            self.response_queue.put("I'm sorry, I encountered an error. Please try again.")

    def update_chat_log(self, message, tag):
        self.chat_log.config(state='normal')
        if tag == "user":
            self.chat_log.insert(tk.END, f"You: {message}\n", tag)
        else:
            self.chat_log.insert(tk.END, f"{message}\n", tag)
        self.chat_log.config(state='disabled')
        self.chat_log.see(tk.END)

    def update_chat(self):
        try:
            message = self.response_queue.get_nowait()
            self.update_chat_log(message, "assistant")
        except queue.Empty:
            pass
        finally:
            self.master.after(100, self.update_chat)

    def exit_program(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            logging.info("User exited the program")
            self.master.quit()