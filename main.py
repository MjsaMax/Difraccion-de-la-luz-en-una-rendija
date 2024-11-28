import tkinter as tk
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class LaserDiffractionSimulation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador de Láser con Lente y Rendija")
        self.root.configure(bg='black')

        # Constantes físicas
        self.wavelength = 633e-9  # Longitud de onda del láser HeNe (rojo)
        self.k = 2 * math.pi / self.wavelength
        self.beam_width = 2  # Ancho del haz láser en mm

        # Parámetros ajustables
        self.focal_length = tk.DoubleVar(value=50)  # Distancia focal de la lente (cm)
        self.slit_width = tk.DoubleVar(value=0.1)  # Ancho de la rendija (mm)
        self.screen_distance = tk.DoubleVar(value=100)  # Distancia a la pantalla (cm)

        # Crear frames para los paneles
        self.setup_frame = tk.Frame(self.root, bg='black')
        self.setup_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.screen_frame = tk.Frame(self.root, bg='black')
        self.screen_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.distribution_frame = tk.Frame(self.root, bg='black')
        self.distribution_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        # Canvas para el montaje óptico y la pantalla
        self.setup_canvas = tk.Canvas(self.setup_frame, width=600, height=400, bg='black')
        self.setup_canvas.pack(pady=10)

        self.screen_canvas = tk.Canvas(self.screen_frame, width=400, height=400, bg='black')
        self.screen_canvas.pack(pady=10)

        # Matplotlib figure para la distribución de intensidad
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.distribution_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Etiquetas
        tk.Label(self.screen_frame,
                 text="Proyección en Pantalla",
                 bg='black', fg='cyan',
                 font=('Arial', 12)).pack()

        tk.Label(self.distribution_frame,
                 text="Distribución de Intensidad",
                 bg='black', fg='cyan',
                 font=('Arial', 12)).pack()

        self.create_controls()
        self.update_simulation()

    def create_controls(self):
        control_frame = tk.Frame(self.root, bg='black')
        control_frame.pack(side=tk.BOTTOM, pady=10)

        # Control para la distancia focal
        tk.Scale(control_frame,
                 variable=self.focal_length,
                 from_=10, to=100,
                 resolution=1,
                 label='Distancia Focal de la Lente (cm)',
                 orient='horizontal',
                 command=lambda x: self.update_simulation(),
                 length=200,
                 bg='black',
                 fg='cyan').pack(pady=5)

        # Control para el ancho de la rendija
        tk.Scale(control_frame,
                 variable=self.slit_width,
                 from_=0.05, to=0.5,
                 resolution=0.01,
                 label='Ancho de la Rendija (mm)',
                 orient='horizontal',
                 command=lambda x: self.update_simulation(),
                 length=200,
                 bg='black',
                 fg='cyan').pack(pady=5)

        # Control para la distancia a la pantalla
        tk.Scale(control_frame,
                 variable=self.screen_distance,
                 from_=50, to=600,
                 resolution=1,
                 label='Distancia a la Pantalla (cm)',
                 orient='horizontal',
                 command=lambda x: self.update_simulation(),
                 length=200,
                 bg='black',
                 fg='cyan').pack(pady=5)

    def draw_laser_beam(self):
        """Dibuja el haz láser con rayos visibles en todo el recorrido"""
        width = 600
        height = 400
        center_y = height / 2

        # Posiciones de los componentes
        laser_x = 50
        lens_x = 200
        slit_x = 400
        screen_x = 550

        # Dibujar el láser
        self.setup_canvas.create_rectangle(laser_x - 15, center_y - 10, laser_x, center_y + 10,
                                           fill='red', outline='yellow')
        self.setup_canvas.create_text(laser_x - 7, center_y + 25,
                                      text="Láser",
                                      fill='white')

        # Número de rayos a dibujar
        n_rays = 3
        ray_spread = self.beam_width / 2  # Mitad del ancho del haz láser

        # Calcular el punto focal
        f = self.focal_length.get() * 2  # Escalado para visualización
        focal_point_x = lens_x + f

        # Dibujar rayos múltiples
        for i in range(n_rays):
            # Posición vertical inicial del rayo
            y_offset = (i - 1) * ray_spread

            # Rayo antes de la lente
            self.setup_canvas.create_line(laser_x, center_y + y_offset,
                                          lens_x, center_y + y_offset,
                                          fill='red', width=1)

            # Rayo desde lente hasta el foco
            self.setup_canvas.create_line(lens_x, center_y + y_offset,
                                          focal_point_x, center_y,
                                          fill='red', width=1)

            # Rayo desde el foco hasta la rendija
            y_at_slit = center_y - y_offset  # Inversión después del foco
            self.setup_canvas.create_line(focal_point_x, center_y,
                                          slit_x, y_at_slit,
                                          fill='red', width=1)

            # Rayo desde la rendija hasta la pantalla
            self.setup_canvas.create_line(slit_x, y_at_slit,
                                          screen_x, y_at_slit,
                                          fill='red', width=1)

        # Dibujar la lente (simplificada)
        lens_height = 80
        self.setup_canvas.create_line(lens_x, center_y - lens_height / 2,
                                      lens_x, center_y + lens_height / 2,
                                      fill='cyan', width=2)
        self.setup_canvas.create_text(lens_x, center_y + lens_height / 2 + 15,
                                      text="Lente",
                                      fill='white')

        # Punto focal
        self.setup_canvas.create_oval(focal_point_x - 3, center_y - 3,
                                      focal_point_x + 3, center_y + 3,
                                      fill='yellow')
        self.setup_canvas.create_text(focal_point_x, center_y + 15,
                                      text="Foco",
                                      fill='yellow')

        # Dibujar la rendija
        slit_height = 80
        self.setup_canvas.create_line(slit_x, center_y - slit_height / 2,
                                      slit_x, center_y + slit_height / 2,
                                      fill='yellow', width=2)
        self.setup_canvas.create_text(slit_x, center_y + slit_height / 2 + 15,
                                      text="Rendija",
                                      fill='white')

        # Dibujar la pantalla
        screen_height = 160
        self.setup_canvas.create_line(screen_x, center_y - screen_height / 2,
                                      screen_x, center_y + screen_height / 2,
                                      fill='white', width=2)
        self.setup_canvas.create_text(screen_x, center_y + screen_height / 2 + 15,
                                      text="Pantalla",
                                      fill='white')

    def calculate_diffraction_pattern(self, y):
        """Calcula el patrón de difracción de una rendija única usando la fórmula de Fraunhofer"""
        a = self.slit_width.get() * 1e-3  # Ancho de la rendija en metros
        L = self.screen_distance.get() * 1e-2  # Distancia a la pantalla en metros
        k = 2 * math.pi / self.wavelength  # Número de onda

        theta = math.atan(y / L)
        alpha = k * a * math.sin(theta) / 2

        if alpha == 0:
            return 1.0
        else:
            return (math.sin(alpha) / alpha) ** 2

    def draw_screen_pattern(self):
        """Dibuja el patrón de difracción en la pantalla"""
        width = 400
        height = 400

        # Limpiar el canvas de la pantalla
        self.screen_canvas.delete('all')

        # Dibujar el marco de la pantalla
        self.screen_canvas.create_rectangle(10, 10, width - 10, height - 10,
                                            outline='white')

        # Calcular y dibujar el patrón de difracción
        y_scale = 0.0005  # Factor de escala para la coordenada y

        # Calcular intensidades
        intensities = [self.calculate_diffraction_pattern((py - height / 2) * y_scale) for py in range(height)]

        # Normalizar intensidades
        max_intensity = max(intensities)
        if max_intensity > 0:
            intensities = [i / max_intensity for i in intensities]

        # Dibujar el patrón
        for py in range(height):
            intensity = intensities[py]
            color = self.intensity_to_color(intensity)
            self.screen_canvas.create_line(10, py, width - 10, py, fill=color)

    def intensity_to_color(self, intensity):
        """Convierte una intensidad (0-1) a un color RGB"""
        red = int(255 * intensity)
        return f'#{red:02x}0000'

    def draw_intensity_distribution(self):
        """Dibuja la distribución de intensidad usando matplotlib"""
        self.ax.clear()

        y = np.linspace(-0.01, 0.01, 1000)
        intensities = [self.calculate_diffraction_pattern(yi) for yi in y]

        self.ax.plot(y, intensities)
        self.ax.set_title('Distribución de Intensidad')
        self.ax.set_xlabel('Posición en la pantalla (m)')
        self.ax.set_ylabel('Intensidad relativa')
        self.ax.grid(True)

        self.canvas.draw()

    def update_simulation(self):
        """Actualiza toda la simulación"""
        self.setup_canvas.delete('all')
        self.screen_canvas.delete('all')
        self.draw_laser_beam()
        self.draw_screen_pattern()
        self.draw_intensity_distribution()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = LaserDiffractionSimulation()
    app.run()

print(
    "Simulation code has been defined. Run the simulation by creating an instance of LaserDiffractionSimulation and calling its run method.")

# un ejemplo de modificacion