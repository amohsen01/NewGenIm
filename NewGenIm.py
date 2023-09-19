import fileinput
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image
from moviepy.editor import VideoFileClip

class NewGenImConverter:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x300")
        self.root.title('NewGenIm Converter')
        self.root.resizable(0, 0)

        self.setup_gui()

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

    def convert_gif(self, gif_path):
        try:
            clip = VideoFileClip(gif_path)
            webm_path = os.path.splitext(gif_path)[0] + ".webm"
            clip.write_videofile(webm_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error converting {gif_path} to WebM: {str(e)}")

    def edit_html(self, html_path):
        try:
            with fileinput.FileInput(html_path, inplace=True, backup='.bak') as file:
                for line in file:
                    line = line.replace('.jpg"', '.webp"').replace('.jpeg"', '.webp"').replace('.png"', '.webp"')
                    line = line.replace('.jpg\'', '.webp\'').replace('.jpeg\'', '.webp\'').replace('.png\'', '.webp\'')
                    line = line.replace('.gif"', '.webm"').replace('.gif\'', '.webm\'')
                    print(line, end="")
            print(f"Done editing {html_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error editing {html_path}: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NewGenImConverter(root)
    root.mainloop()
