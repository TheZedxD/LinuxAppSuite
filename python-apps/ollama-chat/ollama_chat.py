#!/usr/bin/env python3
"""
Ollama Chat Application - A Tkinter-based chat interface for Ollama
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
import re
import os
from datetime import datetime
from typing import List, Dict
from ollama_client import OllamaClient
from tools import ToolRegistry, format_crypto_display


class ChatHistory:
    """Manages chat history persistence"""

    def __init__(self, history_dir: str = None):
        if history_dir is None:
            history_dir = os.path.join(os.path.expanduser("~"), ".ollama_chat", "history")
        self.history_dir = history_dir
        os.makedirs(self.history_dir, exist_ok=True)

    def save_chat(self, messages: List[Dict], model: str) -> str:
        """Save chat to history"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{model.replace(':', '_')}_{timestamp}.json"
        filepath = os.path.join(self.history_dir, filename)

        data = {
            "model": model,
            "timestamp": timestamp,
            "messages": messages
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return filepath

    def list_chats(self) -> List[Dict]:
        """List all saved chats"""
        chats = []
        if not os.path.exists(self.history_dir):
            return chats

        for filename in sorted(os.listdir(self.history_dir), reverse=True):
            if filename.endswith('.json'):
                filepath = os.path.join(self.history_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        chats.append({
                            'filename': filename,
                            'filepath': filepath,
                            'model': data.get('model', 'unknown'),
                            'timestamp': data.get('timestamp', ''),
                            'message_count': len(data.get('messages', []))
                        })
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        return chats

    def load_chat(self, filepath: str) -> Dict:
        """Load a chat from history"""
        with open(filepath, 'r') as f:
            return json.load(f)


class OllamaChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama Chat")
        self.root.geometry("1000x700")

        # Initialize components
        self.client = OllamaClient()
        self.tool_registry = ToolRegistry()
        self.chat_history = ChatHistory()
        self.messages = []
        self.current_model = None
        self.is_streaming = False

        # Setup UI
        self.setup_ui()

        # Check Ollama connection
        self.check_ollama_connection()

    def setup_ui(self):
        """Setup the user interface"""
        # Top frame for controls
        top_frame = ttk.Frame(self.root, padding="5")
        top_frame.pack(fill=tk.X)

        # Model selection
        ttk.Label(top_frame, text="Model:").pack(side=tk.LEFT, padx=(0, 5))
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(top_frame, textvariable=self.model_var,
                                       width=30, state='readonly')
        self.model_combo.pack(side=tk.LEFT, padx=(0, 10))

        # Refresh models button
        ttk.Button(top_frame, text="Refresh Models",
                  command=self.refresh_models).pack(side=tk.LEFT, padx=(0, 10))

        # History button
        ttk.Button(top_frame, text="Chat History",
                  command=self.show_history).pack(side=tk.LEFT, padx=(0, 10))

        # New chat button
        ttk.Button(top_frame, text="New Chat",
                  command=self.new_chat).pack(side=tk.LEFT, padx=(0, 10))

        # Status label
        self.status_label = ttk.Label(top_frame, text="Ready", foreground="green")
        self.status_label.pack(side=tk.RIGHT, padx=(10, 0))

        # Chat display area
        chat_frame = ttk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create text widget with tags for styling
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Monospace", 10),
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground="#0066cc", font=("Monospace", 10, "bold"))
        self.chat_display.tag_config("assistant", foreground="#006600")
        self.chat_display.tag_config("system", foreground="#666666", font=("Monospace", 9, "italic"))
        self.chat_display.tag_config("tool", foreground="#cc6600", font=("Monospace", 9))
        self.chat_display.tag_config("code", background="#f0f0f0", font=("Monospace", 9))
        self.chat_display.tag_config("error", foreground="#cc0000", font=("Monospace", 10, "bold"))

        # Input frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Input text area
        self.input_text = tk.Text(input_frame, height=3, font=("Monospace", 10))
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.input_text.bind("<Return>", self.handle_return_key)
        self.input_text.bind("<Shift-Return>", lambda e: None)  # Allow new line with Shift+Enter

        # Send button
        self.send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))

    def check_ollama_connection(self):
        """Check if Ollama server is available"""
        if self.client.is_available():
            self.set_status("Connected to Ollama", "green")
            self.refresh_models()
        else:
            self.set_status("Ollama server not available", "red")
            messagebox.showwarning(
                "Ollama Not Available",
                "Cannot connect to Ollama server.\n\n"
                "Please make sure Ollama is installed and running:\n"
                "  ollama serve"
            )

    def refresh_models(self):
        """Refresh the list of available models"""
        models = self.client.list_models()
        if models:
            model_names = [m['name'] for m in models]
            self.model_combo['values'] = model_names
            if model_names:
                self.model_combo.current(0)
                self.current_model = model_names[0]
            self.set_status(f"Found {len(models)} model(s)", "green")
        else:
            self.set_status("No models found", "orange")
            messagebox.showinfo(
                "No Models",
                "No Ollama models found.\n\n"
                "Pull a model first:\n"
                "  ollama pull llama2"
            )

    def set_status(self, message: str, color: str = "black"):
        """Update status label"""
        self.status_label.config(text=message, foreground=color)

    def handle_return_key(self, event):
        """Handle Enter key press"""
        # If Shift is not pressed, send message
        if not event.state & 0x1:  # Check if Shift is not held
            self.send_message()
            return "break"  # Prevent default newline insertion
        return None

    def send_message(self):
        """Send a message to the AI"""
        message = self.input_text.get("1.0", tk.END).strip()

        if not message:
            return

        if not self.current_model:
            self.current_model = self.model_var.get()

        if not self.current_model:
            messagebox.showwarning("No Model", "Please select a model first")
            return

        if self.is_streaming:
            messagebox.showinfo("Please Wait", "Already processing a message")
            return

        # Clear input
        self.input_text.delete("1.0", tk.END)

        # Add user message to display
        self.add_message_to_display("User", message, "user")

        # Add to messages list
        self.messages.append({"role": "user", "content": message})

        # Start streaming response in a separate thread
        self.is_streaming = True
        self.send_button.config(state=tk.DISABLED)
        self.set_status("Thinking...", "orange")

        thread = threading.Thread(target=self.stream_response, daemon=True)
        thread.start()

    def stream_response(self):
        """Stream the AI response"""
        try:
            # Get tool definitions
            tools = self.tool_registry.get_tool_definitions()

            # Start assistant message
            self.root.after(0, self.start_assistant_message)

            response_text = ""
            tool_calls = []

            # Stream the response
            for chunk in self.client.chat_stream(
                model=self.current_model,
                messages=self.messages,
                tools=tools
            ):
                if chunk.get("error"):
                    self.root.after(0, self.add_to_current_message,
                                  f"\n[Error: {chunk.get('message')}]", "error")
                    break

                # Handle message content
                if "message" in chunk:
                    msg = chunk["message"]

                    # Handle text content
                    if "content" in msg and msg["content"]:
                        content = msg["content"]
                        response_text += content
                        self.root.after(0, self.add_to_current_message, content, "assistant")

                    # Handle tool calls
                    if "tool_calls" in msg and msg["tool_calls"]:
                        tool_calls.extend(msg["tool_calls"])

                # Check if done
                if chunk.get("done", False):
                    break

            # Handle tool calls if any
            if tool_calls:
                self.root.after(0, self.handle_tool_calls, tool_calls, response_text)
            else:
                # Save assistant message
                if response_text:
                    self.messages.append({"role": "assistant", "content": response_text})
                self.root.after(0, self.finish_streaming)

        except Exception as e:
            error_msg = f"\n[Error: {str(e)}]"
            self.root.after(0, self.add_to_current_message, error_msg, "error")
            self.root.after(0, self.finish_streaming)

    def handle_tool_calls(self, tool_calls: List[Dict], assistant_message: str):
        """Handle tool calls from the AI"""
        # Save assistant message with tool calls
        self.messages.append({
            "role": "assistant",
            "content": assistant_message,
            "tool_calls": tool_calls
        })

        # Execute each tool
        for tool_call in tool_calls:
            function_info = tool_call.get("function", {})
            tool_name = function_info.get("name", "unknown")
            arguments = function_info.get("arguments", {})

            self.add_to_current_message(f"\n\n[Calling tool: {tool_name}]", "tool")

            # Execute the tool
            result = self.tool_registry.execute_tool(tool_name, arguments)

            # Display result
            self.add_to_current_message(f"\n{result}\n", "code")

            # Add tool result to messages
            self.messages.append({
                "role": "tool",
                "content": result
            })

        # Get final response with tool results
        threading.Thread(target=self.stream_final_response, daemon=True).start()

    def stream_final_response(self):
        """Stream final response after tool calls"""
        try:
            response_text = ""

            self.root.after(0, self.add_to_current_message, "\n", "assistant")

            for chunk in self.client.chat_stream(
                model=self.current_model,
                messages=self.messages,
                tools=self.tool_registry.get_tool_definitions()
            ):
                if chunk.get("error"):
                    self.root.after(0, self.add_to_current_message,
                                  f"\n[Error: {chunk.get('message')}]", "error")
                    break

                if "message" in chunk and "content" in chunk["message"]:
                    content = chunk["message"]["content"]
                    if content:
                        response_text += content
                        self.root.after(0, self.add_to_current_message, content, "assistant")

                if chunk.get("done", False):
                    break

            # Save final assistant message
            if response_text:
                self.messages.append({"role": "assistant", "content": response_text})

            self.root.after(0, self.finish_streaming)

        except Exception as e:
            error_msg = f"\n[Error: {str(e)}]"
            self.root.after(0, self.add_to_current_message, error_msg, "error")
            self.root.after(0, self.finish_streaming)

    def start_assistant_message(self):
        """Start a new assistant message in the display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "\nAssistant: ", "assistant")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def add_to_current_message(self, text: str, tag: str = "assistant"):
        """Add text to the current message"""
        self.chat_display.config(state=tk.NORMAL)

        # Simple code block detection
        if "```" in text or tag == "code":
            self.chat_display.insert(tk.END, text, "code")
        else:
            self.chat_display.insert(tk.END, text, tag)

        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def add_message_to_display(self, role: str, content: str, tag: str):
        """Add a complete message to the display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{role}: ", tag)
        self.chat_display.insert(tk.END, f"{content}\n", tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def finish_streaming(self):
        """Finish streaming and re-enable controls"""
        self.is_streaming = False
        self.send_button.config(state=tk.NORMAL)
        self.set_status("Ready", "green")
        self.input_text.focus()

        # Auto-save chat history
        if len(self.messages) > 0:
            try:
                self.chat_history.save_chat(self.messages, self.current_model)
            except Exception as e:
                print(f"Error saving chat history: {e}")

    def new_chat(self):
        """Start a new chat"""
        if self.messages and messagebox.askyesno("New Chat", "Start a new chat? Current chat will be saved."):
            # Save current chat
            if len(self.messages) > 0:
                try:
                    filepath = self.chat_history.save_chat(self.messages, self.current_model)
                    self.set_status(f"Chat saved", "green")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save chat: {e}")

            # Clear messages
            self.messages = []

            # Clear display
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)

            self.set_status("New chat started", "green")

    def show_history(self):
        """Show chat history dialog"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Chat History")
        history_window.geometry("600x400")

        # Create listbox
        frame = ttk.Frame(history_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Previous Chats:", font=("Monospace", 10, "bold")).pack(anchor=tk.W)

        listbox_frame = ttk.Frame(frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=("Monospace", 9))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Load chat history
        chats = self.chat_history.list_chats()

        if not chats:
            listbox.insert(tk.END, "No chat history found")
        else:
            for chat in chats:
                timestamp = chat['timestamp']
                # Format timestamp
                if len(timestamp) == 15:  # YYYYMMDD_HHMMSS
                    formatted = f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:15]}"
                else:
                    formatted = timestamp

                entry = f"{formatted} | {chat['model']} | {chat['message_count']} messages"
                listbox.insert(tk.END, entry)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        def load_selected():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                if idx < len(chats):
                    chat = chats[idx]
                    try:
                        data = self.chat_history.load_chat(chat['filepath'])

                        # Load messages
                        self.messages = data.get('messages', [])
                        self.current_model = data.get('model', self.current_model)

                        # Update model selection
                        if self.current_model in self.model_combo['values']:
                            self.model_combo.set(self.current_model)

                        # Clear and reload display
                        self.chat_display.config(state=tk.NORMAL)
                        self.chat_display.delete(1.0, tk.END)

                        for msg in self.messages:
                            role = msg.get('role', 'unknown')
                            content = msg.get('content', '')

                            if role == 'user':
                                self.add_message_to_display("User", content, "user")
                            elif role == 'assistant':
                                self.add_message_to_display("Assistant", content, "assistant")
                            elif role == 'system':
                                self.add_message_to_display("System", content, "system")
                            elif role == 'tool':
                                self.add_message_to_display("Tool", content, "tool")

                        self.chat_display.config(state=tk.DISABLED)
                        self.set_status("Chat loaded", "green")
                        history_window.destroy()

                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to load chat: {e}")

        ttk.Button(button_frame, text="Load Selected", command=load_selected).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Close", command=history_window.destroy).pack(side=tk.RIGHT)

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = OllamaChatApp(root)
    app.run()


if __name__ == '__main__':
    main()
