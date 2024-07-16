import tkinter as tk
from tkinter import scrolledtext, ttk
import queue
from character_data import characters

class DnDChatbotGUI:
    def __init__(self, master, chat_function, process_tool_call):
        self.master = master
        master.title("D&D 5e Combat Simulator")
        master.configure(bg='#2C3E50')  # Dark blue background

        self.chat_function = chat_function
        self.process_tool_call = process_tool_call

        self.create_widgets()
        self.conversation = []
        self.response_queue = queue.Queue()

        self.display_greeting()
        self.update_chat()

    def create_widgets(self):
        main_frame = tk.Frame(self.master, bg='#2C3E50')
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame, bg='#2C3E50')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(main_frame, bg='#2C3E50', width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Chat window
        self.chat_log = scrolledtext.ScrolledText(left_frame, state='disabled', bg='#34495E', fg='white', font=('Courier', 12))
        self.chat_log.pack(expand=True, fill='both')

        # Configure text tags
        self.chat_log.tag_configure("user", foreground="#3498DB")
        self.chat_log.tag_configure("assistant", foreground="#2ECC71")
        self.chat_log.tag_configure("system", foreground="#F1C40F")
        self.chat_log.tag_configure("combat", foreground="#E74C3C")

        # Input field
        self.input_field = tk.Entry(left_frame, bg='#7F8C8D', fg='white', insertbackground='white')
        self.input_field.pack(expand=True, fill='x', pady=10)
        self.input_field.bind("<Return>", self.send_message)

        # Send button
        send_button = tk.Button(left_frame, text="Send", command=self.send_message, bg='#27AE60', fg='white')
        send_button.pack(pady=5)

        # Model selection
        self.model_var = tk.StringVar(value="claude-3-haiku-20240307")  # Set default to Haiku
        model_label = tk.Label(right_frame, text="Select Model:", bg='#2C3E50', fg='white')
        model_label.pack(pady=5)
        self.model_dropdown = ttk.Combobox(right_frame, textvariable=self.model_var, 
                                           values=["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"])
        self.model_dropdown.pack(pady=5)

        # Turn count display
        self.turn_count_var = tk.StringVar(value="Turn: 0")
        tk.Label(right_frame, textvariable=self.turn_count_var, bg='#2C3E50', fg='white').pack(pady=5)

        # HP displays
        self.hp_vars = {}
        for char_name in characters.keys():
            self.hp_vars[char_name] = tk.StringVar(value=f"{char_name} HP: 0/0")
            tk.Label(right_frame, textvariable=self.hp_vars[char_name], bg='#2C3E50', fg='white').pack(pady=5)

        # Tool Input/Output Display
        tool_label = tk.Label(right_frame, text="Tool Input/Output:", bg='#2C3E50', fg='white')
        tool_label.pack(pady=(10, 5))
        self.tool_display = scrolledtext.ScrolledText(right_frame, height=15, width=35, bg='#34495E', fg='white')
        self.tool_display.pack(pady=5)
        self.tool_display.config(state='disabled')

    def display_greeting(self):
        greeting = "Welcome to the D&D 5e Combat Simulator!\n"
        greeting += "You can simulate combat between characters or ask questions about D&D.\n"
        greeting += "Type 'exit' to end the conversation.\n\n"
        self.update_chat_log(greeting, "system")

    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if message == "":
            return
        self.input_field.delete(0, tk.END)

        if message.lower() == 'exit':
            self.master.quit()
            return

        self.conversation.append({"role": "user", "content": message})
        self.update_chat_log(message, "user")

        self.master.after(0, self.get_claude_response, message)

    def get_claude_response(self, message):
        selected_model = self.model_var.get()
        response = self.chat_function(self.conversation, selected_model)
        if response:
            self.conversation.append({"role": "assistant", "content": response})
            self.response_queue.put(response)
        else:
            self.response_queue.put("I'm sorry, I encountered an error. Please try again.")

    def update_chat_log(self, message, tag):
        self.chat_log.config(state='normal')
        if tag == "user":
            self.chat_log.insert(tk.END, f"You: {message}\n", tag)
        elif tag == "assistant":
            self.chat_log.insert(tk.END, f"Claude: {message}\n", tag)
        else:
            self.chat_log.insert(tk.END, f"{message}\n", tag)
        self.chat_log.config(state='disabled')
        self.chat_log.see(tk.END)

    def update_tool_display(self, tool_name, tool_input, tool_output):
        self.tool_display.config(state='normal')
        self.tool_display.delete('1.0', tk.END)
        self.tool_display.insert(tk.END, f"Tool: {tool_name}\n\n")
        self.tool_display.insert(tk.END, f"Input:\n{tool_input}\n\n")
        self.tool_display.insert(tk.END, f"Output:\n{tool_output}")
        self.tool_display.config(state='disabled')

    def update_combat_info(self, turn_count, characters):
        self.turn_count_var.set(f"Turn: {turn_count}")
        for char_name, char in characters.items():
            # Find the matching key in self.hp_vars, ignoring case
            matching_key = next((key for key in self.hp_vars.keys() if key.lower() == char_name.lower()), None)
            if matching_key:
                self.hp_vars[matching_key].set(f"{matching_key} HP: {char.current_hp}/{char.max_hp}")
            else:
                print(f"Warning: No matching HP variable found for character '{char_name}'")

    def update_chat(self):
        try:
            message = self.response_queue.get_nowait()
            self.update_chat_log(message, "assistant")
        except queue.Empty:
            pass
        finally:
            self.master.after(100, self.update_chat)