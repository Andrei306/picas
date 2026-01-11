# picas
PICAS - Palette Identifier and Color Analysis System

## Key Features
- Color Extraction: uses K-Means clustering to find the main colors.
- Audio Feedback: click any color block to hear its name (e.g., "Dark Teal").
- Smart Naming: accurately identifies complex colors using weighted algorithms.

## 🛠️ Installation & Usage 

1. **Clone the repository**
   ```bash
   git clone https://github.com/Andrei306/picas.git
   cd picas

2. **Install dependencies**
    ```bash
   pip install -r requirements.txt

3. **Run the application**
    ```bash
   python main.py

## 📂 Project Structure

- main.py: entry point of the application.
- gui.py: handles the frontend, threading, and TTS logic.
- processor.py: handles image processing and K-Means clustering.
- utils.py: contains mathematical formulas and the color database.

***
Project developed for the Human-Computer Interaction laboratory.