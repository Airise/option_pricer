import tkinter as tk
from tkinter import ttk


class ResultPanel:
    def __init__(self, parent: tk.Widget):
        frame = ttk.Frame(parent, style="App.TFrame")
        frame.pack(fill="both", expand=False, pady=(24, 0))

        # --- Highlight Result Area (Rounded Rectangle) ---
        self.highlight_canvas = tk.Canvas(frame, bg="#f8fafc", highlightthickness=0, height=80)
        self.highlight_canvas.pack(fill="x", pady=(0, 20))
        
        self.latest_message = "Ready to calculate..."
        self.highlight_canvas.bind("<Configure>", self._on_canvas_resize)

        # --- Terminal Area ---
        # Title
        ttk.Label(frame, text="Terminal Output", style="ResultTitle.TLabel").pack(anchor="w", pady=(0, 12))

        # Text container for thin border effect
        text_container = tk.Frame(frame, bg="#e2e8f0", padx=1, pady=1)
        text_container.pack(fill="both", expand=True)

        # Dark terminal output box
        self.text = tk.Text(text_container, height=8, width=100,
                            font=("Cascadia Code", 10),
                            bg="#0f172a",
                            fg="#f8fafc",
                            relief="flat",
                            highlightthickness=0,
                            padx=20, pady=20)
        self.text.pack(fill="both", expand=True)
        self.text.configure(state="disabled")

    def _on_canvas_resize(self, event):
        self.highlight_canvas.delete("all")
        w = event.width
        h = event.height
        if w <= 1 or h <= 1:
            return
            
        x1, y1 = 4, 4
        x2, y2 = w - 4, h - 4
        
        fill_color = "#e0f2fe"
        outline_color = "#bae6fd"
        
        # Draw a simple rectangle
        self.highlight_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color, width=2)
        
        # Draw text in the center
        self.highlight_canvas.create_text(w/2, h/2, text=self.latest_message, 
                                          font=("Segoe UI", 16, "bold"), fill="#0369a1", 
                                          justify="center")

    def write(self, message: str) -> None:
        # Output to GUI and terminal
        print(message)
        
        # Extract only the result part (e.g., "Price = 10.450584")
        display_text = message.split("] ", 1)[-1] if "] " in message else message
        self.latest_message = display_text
        
        w = self.highlight_canvas.winfo_width()
        h = self.highlight_canvas.winfo_height()
        if w > 1 and h > 1:
            # Manually trigger redraw
            self._on_canvas_resize(type('Event', (), {'width': w, 'height': h})())

        # Update terminal
        self.text.configure(state="normal")
        self.text.insert("end", message + "\n")
        self.text.see("end")
        self.text.configure(state="disabled")

    def clear(self) -> None:
        self.latest_message = "Ready to calculate..."
        w = self.highlight_canvas.winfo_width()
        h = self.highlight_canvas.winfo_height()
        if w > 1 and h > 1:
            self._on_canvas_resize(type('Event', (), {'width': w, 'height': h})())
            
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")
