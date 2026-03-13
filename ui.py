import tkinter as tk
import random
import subprocess
import sys


class SpatialStudioUI:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Spatial Studio")

        # FULLSCREEN
        self.root.attributes("-fullscreen", True)

        self.root.configure(bg="#0b0b0b")

        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.canvas = tk.Canvas(
            self.root,
            bg="#0b0b0b",
            highlightthickness=0
        )

        self.canvas.pack(fill="both", expand=True)

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.particles = []

        self.create_particles()

        self.build_ui()

        self.animate()

        self.root.mainloop()

    # ---------------------------
    # PARTICLE BACKGROUND
    # ---------------------------

    def create_particles(self):

        for _ in range(80):

            x = random.randint(0, self.width)
            y = random.randint(0, self.height)

            size = random.randint(2,4)

            particle = self.canvas.create_oval(
                x, y,
                x+size, y+size,
                fill="#00d9ff",
                outline=""
            )

            self.particles.append((particle, random.uniform(0.5,2)))

    # ---------------------------
    # UI
    # ---------------------------

    def build_ui(self):

        center = tk.Frame(self.canvas, bg="#111111", padx=60, pady=60)
        center.place(relx=0.5, rely=0.5, anchor="center")

        self.title = tk.Label(
            center,
            text="SPATIAL STUDIO",
            font=("Segoe UI", 52, "bold"),
            fg="#00e5ff",
            bg="#111111"
        )

        self.title.pack(pady=(0,20))

        subtitle = tk.Label(
            center,
            text="Gesture Driven Spatial Computing Engine",
            font=("Segoe UI", 16),
            fg="#aaaaaa",
            bg="#111111"
        )

        subtitle.pack(pady=(0,40))

        start_btn = tk.Button(
            center,
            text="START EXPERIENCE",
            font=("Segoe UI", 18, "bold"),
            bg="#2979ff",
            fg="white",
            width=24,
            height=2,
            bd=0,
            command=self.start_engine
        )

        start_btn.pack(pady=15)

        controls = tk.Frame(center, bg="#111111")
        controls.pack(pady=10)

        inst = tk.Button(
            controls,
            text="Instructions",
            font=("Segoe UI", 12),
            bg="#333333",
            fg="white",
            width=16,
            height=2,
            bd=0,
            command=self.instructions
        )

        inst.grid(row=0, column=0, padx=10)

        exit_btn = tk.Button(
            controls,
            text="Exit",
            font=("Segoe UI", 12),
            bg="#d32f2f",
            fg="white",
            width=16,
            height=2,
            bd=0,
            command=self.root.destroy
        )

        exit_btn.grid(row=0, column=1, padx=10)

        footer = tk.Label(
            center,
            text="Spatial Computing Demonstration",
            font=("Segoe UI", 11),
            fg="#666666",
            bg="#111111"
        )

        footer.pack(pady=(30,0))

    # ---------------------------
    # ANIMATION LOOP
    # ---------------------------

    def animate(self):

        for particle, speed in self.particles:

            self.canvas.move(particle, 0, speed)

            pos = self.canvas.coords(particle)

            if pos[1] > self.height:

                x = random.randint(0, self.width)

                self.canvas.coords(
                    particle,
                    x, 0,
                    x+3, 3
                )

        # glow animation
        colors = ["#00e5ff","#00bcd4","#00e5ff","#29b6f6"]
        color = random.choice(colors)

        self.title.config(fg=color)

        self.root.after(40, self.animate)

    # ---------------------------
    # START ENGINE
    # ---------------------------

    def start_engine(self):

        subprocess.Popen([sys.executable, "main.py"])

    # ---------------------------
    # INSTRUCTIONS
    # ---------------------------

    def instructions(self):

        popup = tk.Toplevel(self.root)

        popup.title("Controls")
        popup.geometry("400x300")
        popup.configure(bg="#111111")

        text = """
RIGHT HAND
Index finger → Draw

LEFT HAND
Fist → Erase

KEYBOARD

1 → Cube
2 → Sphere
3 → Pyramid

0 → Stop rotation
S → Save screenshot
ESC → Exit
"""

        label = tk.Label(
            popup,
            text=text,
            font=("Segoe UI", 12),
            fg="white",
            bg="#111111",
            justify="left"
        )

        label.pack(padx=30, pady=30)


if __name__ == "__main__":
    SpatialStudioUI()