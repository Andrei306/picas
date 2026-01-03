import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pyttsx3
import threading # for better performance (TTS not to block gui)
from sklearn.cluster import KMeans
import queue

from processor import ImageProcessor
from utils import rgb_to_hex, get_closest_color_name


class picasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PICAS")
        self.root.geometry("900x600")
        self.processor = ImageProcessor()

        # --- FIX TTS 1: Configurare Coada si Motor ---
        self.speech_queue = queue.Queue()
        self.tts_engine = None

        # starting unique thread for audio
        # daemon=True -> closes when the app is closed
        threading.Thread(target=self._tts_worker, daemon=True).start()

        self._setup_ui()

    """
    Special function to run in a sperate thread permanently.
    It solves the problem with the TTS, now the audio (speaking) works normal.
    """
    def _tts_worker(self):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            self.tts_engine = engine

            while True:
                text = self.speech_queue.get()

                if text is None:
                    break

                #speak the text
                try:
                    engine.say(text)
                    engine.runAndWait()
                except:
                    pass

                # mark task done
                self.speech_queue.task_done()

        except Exception as e:
            print("Error in the audio thread", e)

    def _setup_ui(self):
        header_frame = tk.Frame(self.root, pady=10)
        header_frame.pack()

        btn_load = tk.Button(header_frame, text="Upload Image", command=self.upload_image,
                             bg="#4a90e2", fg="white", font=("Arial", 12, "bold"))
        btn_load.pack()

        self.image_container = tk.Label(self.root, text="No selected image", bg="#f0f0f0")
        self.image_container.pack(pady=20, expand=True)

        self.palette_frame = tk.Frame(self.root)
        self.palette_frame.pack(pady=20, fill="x")

        lbl_info = tk.Label(self.palette_frame, text="Dominant colours (click for audio):",
                            font=("Arial", 10, "italic"))
        lbl_info.pack(pady=5)

        self.swatches_container = tk.Frame(self.palette_frame)
        self.swatches_container.pack()

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

        if array_img is not None:
            pil_img = Image.fromarray(array_img)
            img_tk = ImageTk.PhotoImage(pil_img)

            self.image_container.configure(image=img_tk, text="")
            self.image_container.image = img_tk  # garbage collector reference

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
                            command=lambda c=color_name, h=hex_code: self.speak_color(c, h))
            btn.pack()

            lbl = tk.Label(swatch_frame, text=hex_code, font=("Consolas", 9))
            lbl.pack()

    def speak_color(self, name, hex_code):
        print(f"User clicked: {name} ({hex_code}")  # debugging

        text_to_say = f"{name}"

        def run_speech():
            if self.tts_engine:
                try:
                    if self.tts_engine._inLoop:
                        self.tts_engine.endLoop()

                    self.tts_engine.say(text_to_say)
                    self.tts_engine.runAndWait()
                except Exception as e:
                    print("TTS Error", e)

        if self.tts_engine:
            threading.Thread(target=run_speech, daemon=True).start()
