import streamlit as st
import threading
import queue
import traceback

class DnDChatbotGUI:
    def __init__(self, chat_function, process_tool_call):
        self.chat_function = chat_function
        self.process_tool_call = process_tool_call

        # Initialize session state
        if 'conversation' not in st.session_state:
            st.session_state.conversation = []
        if 'model' not in st.session_state:
            st.session_state.model = "claude-3-haiku-20240307"
        if 'tool_display' not in st.session_state:
            st.session_state.tool_display = ""
        if 'error' not in st.session_state:
            st.session_state.error = None

        self.response_queue = queue.Queue()

        self.create_layout()

    def create_layout(self):
        st.title("D&D 5e Combat Simulator")

        # Sidebar
        with st.sidebar:
            st.session_state.model = st.selectbox(
                "Select Model:",
                ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
                index=2  # Default to Haiku
            )

            st.text("Characters:\nOrc\nGoblin")

        # Main chat area
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.conversation:
                if message['role'] == 'user':
                    st.text_area("You:", value=message['content'], height=100, disabled=True)
                elif message['role'] == 'assistant':
                    st.text_area("Claude:", value=message['content'], height=100, disabled=True)
                else:
                    st.text_area("System:", value=message['content'], height=100, disabled=True)

        # Tool display
        if st.session_state.tool_display:
            st.text_area("Tool Input/Output:", value=st.session_state.tool_display, height=200, disabled=True)

        # Error display
        if st.session_state.error:
            st.error(f"An error occurred: {st.session_state.error}")

        # Input area
        user_input = st.text_input("Enter your message:")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Send") or user_input:
                self.send_message(user_input)
        with col2:
            if st.button("Exit"):
                st.stop()

    def send_message(self, message):
        if message.strip() == "":
            return

        st.session_state.conversation.append({"role": "user", "content": message})
        
        try:
            response = self.chat_function(st.session_state.conversation, self.process_tool_call, st.session_state.model)
            if response:
                st.session_state.conversation.append({"role": "assistant", "content": response})
            else:
                st.session_state.conversation.append({"role": "assistant", "content": "I'm sorry, I encountered an error. Please try again."})
        except Exception as e:
            st.session_state.error = str(e)
            st.error(f"An error occurred: {e}")
            st.session_state.conversation.append({"role": "assistant", "content": "An error occurred. Please check the error message and try again."})

        st.experimental_rerun()

    def update_tool_display(self, tool_name, tool_input, tool_output):
        st.session_state.tool_display = f"Tool: {tool_name}\n\nInput:\n{tool_input}\n\nOutput:\n{tool_output}"

    def display_greeting(self):
        greeting = "Welcome to the D&D 5e Combat Simulator!\n"
        greeting += "You can simulate combat between characters or ask questions about D&D.\n"
        greeting += "Type 'exit' or use the Exit button to end the conversation.\n\n"
        st.session_state.conversation.append({"role": "system", "content": greeting})

def create_gui(chat_function, process_tool_call):
    st.set_page_config(page_title="D&D Combat Simulator", layout="wide")
    return DnDChatbotGUI(chat_function, process_tool_call)

if __name__ == "__main__":
    # This is for testing purposes only
    def dummy_chat_function(conversation, process_tool_call, model):
        return "This is a dummy response."

    def dummy_process_tool_call(tool_name, tool_input):
        return "This is a dummy tool result."

    create_gui(dummy_chat_function, dummy_process_tool_call)