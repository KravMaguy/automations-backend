import tkinter as tk
from tkinter import filedialog, scrolledtext

class SimpleUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Desktop Application")
        self.geometry("800x400")

        left_frame = tk.Frame(self, width=400, height=400)
        left_frame.pack(side="left", fill="both", expand=True)

        self.upload_button = tk.Button(left_frame, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=20)

        self.file_path_label = tk.Label(left_frame, text="No file uploaded")
        self.file_path_label.pack(pady=20)

        right_frame = tk.Frame(self, width=400, height=400)
        right_frame.pack(side="right", fill="both", expand=True)

        self.terminal_output = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=50, height=20)
        self.terminal_output.pack(padx=20, pady=20)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_label.config(text=file_path)
            # terminal output:
            self.terminal_output.insert(tk.END, f"File uploaded: {file_path}\n")

if __name__ == "__main__":
    app = SimpleUI()
    app.mainloop()
