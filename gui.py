import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pyttsx3
import threading # for better performance (TTS not to block gui)

from sklearn.cluster import KMeans

from processor import ImageProcessor
from utils import rgb_to_hex, get_closest_color_name


class picasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PICAS")
        self.root.geometry("600x700")
        self.processor = ImageProcessor()

        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
        except Exception as e:
            print("Could not initialize pyttsx3 module", e)
            self.tts_engine = None

    """Uploading a picture"""
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")]
        )

        if not file_path:
            return

        success = self.processor.load_image(file_path)
        if success:
            self.display_image()
            self.generate_palette()
        else:
            messagebox.showerror("Error", "Could not load image")

    def display_image(self):
        array_img = self.processor.get_display_image(max_size=(500, 400))

        if array_img is None:
            pil_img = Image.fromarray(array_img)
            img_tk = ImageTk.PhotoImage(pil_img)

            self.image_container.configure(image=img_tk, text="")
            self.image_container.image = img_tk # garbage collector reference

    def generate_palette(self):
        for widget in self.swatches_container.winfo_children():
            widget.destroy()

        colors = self.processor.extract_palette(n_colors=5)

        for rgb in colors:
            hex_code = rgb_to_hex(rgb)
            color_name = get_closest_color_name(rgb)

            swatch_frame = tk.Frame(self.swatches_container, padx=5)
            swatch_frame.pack(side="left", padx=5)

            btn = tk.Button(swatch_frame, bg=hex_code, width=8, height=4,
                            command=lambda c=color_name, h=hex_code: self.speak_color(c,h))
            btn.pack()

            lbl = tk.Label(swatch_frame, text=hex_code, font=("Consolas", 9))

    def speak_color(self, name, hex_code):
        print(f"User clicked: {name} ({hex_code}") # debugging

        text_to_say = f"{name}"

        def run_speech():
            if self.tts_engine:
                self.tts_engine.say(text_to_say)
                self.tts_engine.runAndWait()

        threading.Thread(target=run_speech, daemon=True).start()

    def _setup_ui(self):
        header_frame = tk.Frame(self.root, pady=10)
        header_frame.pack()

        btn_load = tk.Button(header_frame, text="Uplaod Image", command=self.upload_image,
                             bg="#4a90e2", fg="white", font=("Arial", 12, "bold"))
        btn_load.pack()

        self.image_container = tk.Label(self.root, text="No selected image", bg="f0f0f0")
        self.image_container.pack(pady=20, expand=True)

        self.palette_frame = tk.Frame(self.root)
        self.pallete_frame.pack(pady=20, fill="x")

        lbl_info = tk.Label(self.palette_frame, text="Dominant colours (click for audio):",
                            font=("Arial", 10, "italic"))
        lbl_info.pack(pady=5)

        self.swatches_container = tk.Frame(self.palette_frame)
        self.swatches_container.pack()
