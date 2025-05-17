import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

class DeBroglieApp:
    def __init__(self, root):
        self.root = root
        root.title("Длина волны де Бройля — электрон и протон")

        self.h = 6.62607015e-34
        self.m_e = 9.10938356e-31
        self.m_p = 1.6726219e-27

        self.v_e = 1e6
        self.v_p = 1e5

        self.create_controls(root)
        self.create_text_info(root)
        self.create_plots(root)
        self.create_description(root)

        self.phase = 0
        self.anim = FuncAnimation(self.fig, self.animate, interval=50, blit=False)

        self.update_all()

    def create_controls(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(side='top', fill='x', padx=10, pady=10)

        ttk.Label(frame, text="Скорость электрона (м/с):").grid(row=0, column=0, sticky="w")
        self.scale_v_e = ttk.Scale(frame, from_=100, to=3e8, orient='horizontal', command=self.on_change)
        self.scale_v_e.set(self.v_e)
        self.scale_v_e.grid(row=0, column=1, sticky="ew")
        self.label_v_e = ttk.Label(frame, text=f"{self.v_e:.0f}")
        self.label_v_e.grid(row=0, column=2, sticky="w")

        ttk.Label(frame, text="Скорость протона (м/с):").grid(row=1, column=0, sticky="w")
        self.scale_v_p = ttk.Scale(frame, from_=100, to=3e7, orient='horizontal', command=self.on_change)
        self.scale_v_p.set(self.v_p)
        self.scale_v_p.grid(row=1, column=1, sticky="ew")
        self.label_v_p = ttk.Label(frame, text=f"{self.v_p:.0f}")
        self.label_v_p.grid(row=1, column=2, sticky="w")

        frame.columnconfigure(1, weight=1)

    def create_text_info(self, parent):
        self.text_info = tk.Text(parent, height=6, bg="#f0f0f0", fg="black", relief="flat", font=("Courier", 10))
        self.text_info.pack(fill='x', padx=10, pady=(0, 10))
        self.text_info.configure(state='disabled')

    def create_description(self, parent):
        self.text_desc = tk.Text(parent, height=6, bg="#ffffff", fg="black", relief="flat", wrap='word')
        self.text_desc.pack(fill='both', padx=10, pady=(0, 10))
        self.text_desc.insert("1.0",
                              "Объяснение поведения волновых функций:\n"
                              "Электрон и протон рассматриваются как квантовые волны. Их волновые функции отображаются в виде синусоид, изменяющихся со временем.\n"
                              "Формула волновой функции: ψ(x, t) = sin(kx + φ), где k = 2π / λ.\n"
                              "Электрон — имеет меньшую массу, поэтому при заданной скорости его длина волны больше. Это видно на графике: волна растянута, колебания более редкие.\n"
                              "Протон — гораздо массивнее электрона. При той же скорости длина его волны значительно меньше. Это приводит к частым осцилляциям на графике — волна более сжатая.\n"
                              "Так проявляется принцип де Бройля: чем больше масса или скорость — тем короче длина волны (λ = h / mv)."
                              )
        self.text_desc.configure(state='disabled')

    def create_plots(self, parent):
        self.fig, axs = plt.subplots(1, 2, figsize=(10, 3))
        self.fig.tight_layout(pad=3.0)

        self.ax3, self.ax4 = axs

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.x = np.linspace(0, 1e-8, 1000)

    def de_broglie_wavelength(self, mass, velocity):
        p = mass * np.array(velocity)
        p_safe = np.where(p == 0, 1e-40, p)
        return self.h / p_safe

    def update_all(self):
        self.v_e = self.scale_v_e.get()
        self.label_v_e.config(text=f"{self.v_e:.0f}")

        self.v_p = self.scale_v_p.get()
        self.label_v_p.config(text=f"{self.v_p:.0f}")

        lambda_e = self.de_broglie_wavelength(self.m_e, self.v_e)
        lambda_p = self.de_broglie_wavelength(self.m_p, self.v_p)

        text = (
            f"Формула: λ = h / (mv)\n"
            f"Электрон: λₑ = {self.h:.2e} / ({self.m_e:.2e} × {self.v_e:.2e}) = {lambda_e:.2e} м ≈ {lambda_e*1e9:.2f} нм\n"
            f"Протон:   λₚ = {self.h:.2e} / ({self.m_p:.2e} × {self.v_p:.2e}) = {lambda_p:.2e} м ≈ {lambda_p*1e9:.2f} нм"
        )
        self.text_info.configure(state='normal')
        self.text_info.delete("1.0", tk.END)
        self.text_info.insert(tk.END, text)
        self.text_info.configure(state='disabled')

        # Электрон
        self.ax3.clear()
        k_e = 2 * np.pi / lambda_e
        y_e = np.sin(k_e * self.x + self.phase)
        self.ax3.plot(self.x * 1e9, y_e)
        self.ax3.set_title("Волновая функция электрона")
        self.ax3.set_xlabel("Положение (нм)")
        self.ax3.set_ylabel("Амплитуда")
        self.ax3.set_ylim(-1.5, 1.5)
        self.ax3.grid(True)

        # Протон
        self.ax4.clear()
        k_p = 2 * np.pi / lambda_p
        y_p = np.sin(k_p * self.x + self.phase)
        self.ax4.plot(self.x * 1e9, y_p, 'orange')
        self.ax4.set_title("Волновая функция протона")
        self.ax4.set_xlabel("Положение (нм)")
        self.ax4.set_ylabel("Амплитуда")
        self.ax4.set_ylim(-1.5, 1.5)
        self.ax4.grid(True)

        self.canvas.draw_idle()

    def animate(self, i):
        self.phase += 0.2
        self.update_all()

    def on_change(self, event):
        self.update_all()

if __name__ == "__main__":
    root = tk.Tk()
    app = DeBroglieApp(root)
    root.mainloop()
