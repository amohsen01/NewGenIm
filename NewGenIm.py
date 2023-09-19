import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image
from moviepy.editor import VideoFileClip
import sys

class NewGenImConverter:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x400")
        self.root.title('NewGenIm Converter')
        self.root.resizable(0, 0)

        self.setup_gui()
        self.setup_logging()

    def setup_gui(self):
        html_label = tk.Label(self.root, text="HTML Directory:")
        html_label.grid(row=2, column=0, sticky=tk.W, padx=20, pady=10)
        self.html_directory_entry = tk.Entry(self.root, width=50)
        self.html_directory_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=10)
        browse_button = tk.Button(text="Choose HTML folder", command=self.browse_button)
        browse_button.grid(row=3, column=1, padx=150)
        convert_button = tk.Button(text="Convert!", command=self.convert_files)
        convert_button.grid(row=4, column=1, padx=150)
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.grid(row=5, column=1, pady=20)
        self.log_text = tk.Text(self.root, height=10, width=60)
        self.log_text.grid(row=6, column=1, padx=10, pady=10)
        self.log_text.tag_configure("stdout", foreground="black")
        self.log_text.tag_configure("stderr", foreground="red")

    def setup_logging(self):
        sys.stdout = Logger(self.log_text, "stdout")
        sys.stderr = Logger(self.log_text, "stderr")

    def browse_button(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.html_directory_entry.delete(0, tk.END)
            self.html_directory_entry.insert(0, folder_path)

    def convert_image(self, image_path):
        try:
            im = Image.open(image_path).convert('RGBA')
            image_name = os.path.splitext(image_path)[0]
            im.save(f"{image_name}.webp", 'webp')
        except Exception as e:
            messagebox.showerror("Error", f"Error converting {image_path}: {str(e)}")

    def convert_files(self):
        html_directory = self.html_directory_entry.get()
        if not os.path.exists(html_directory):
            messagebox.showerror("Error", "Invalid HTML directory path")
            return
        image_files = []
        html_files = []
        for root, _, files in os.walk(html_directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_extension = file_path.lower().split('.')[-1]
                if file_extension in ['jpg', 'jpeg', 'png']:
                    image_files.append(file_path)
                elif file_extension == 'html':
                    html_files.append(file_path)
        total_files = len(image_files) + len(html_files)
        current_file = 0
        for image_file in image_files:
            self.convert_image(image_file)
            current_file += 1
            self.update_progress(current_file, total_files)
        for html_file in html_files:
            self.edit_html(html_file)
            current_file += 1
            self.update_progress(current_file, total_files)
        messagebox.showinfo("NewGenIm Converter", "Conversion and editing completed successfully!")

    def update_progress(self, current, total):
        progress = int((current / total) * 100)
        self.progress_bar["value"] = progress
        self.root.update_idletasks()

    def edit_html(self, html_path):
        try:
            with open(html_path, 'r') as file:
                lines = file.readlines()
            with open(html_path, 'w') as file:
                for line in lines:
                    line = line.replace('.jpg"', '.webp"').replace('.jpeg"', '.webp"').replace('.png"', '.webp"')
                    line = line.replace('.jpg\'', '.webp\'').replace('.jpeg\'', '.webp\'').replace('.png\'', '.webp\'')
                    line = line.replace('.gif"', '.webm"').replace('.gif\'', '.webm\'')
                    file.write(line)
            self.log_text.insert(tk.END, f"Done editing {html_path}\n", "stdout")
        except Exception as e:
            messagebox.showerror("Error", f"Error editing {html_path}: {str(e)}")
            self.log_text.insert(tk.END, f"Error editing {html_path}: {str(e)}\n", "stderr")

class Logger:
    def __init__(self, text_widget, tag):
        self.text_widget = text_widget
        self.tag = tag

    def write(self, message):
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, message, (self.tag,))
        self.text_widget.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = NewGenImConverter(root)
    root.mainloop()
