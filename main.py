import tkinter as tk
import math
import numpy as np

class LaserDiffractionSimulation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador de Láser con Lente y Rendija")
        self.root.configure(bg='black')

        # Constantes físicas
        self.wavelength = 633e-9  # Longitud de onda del láser HeNe (rojo)
        self.k = 2 * math.pi / self.wavelength
        self.beam_width = 2  # Ancho del haz láser en mm
        self.focal_length = 50  # Distancia focal fija de la lente (cm)

        # Parámetros ajustables
        self.slit_width = tk.DoubleVar(value=0.1)  # Ancho de la rendija (mm)
        self.screen_distance = tk.DoubleVar(value=100)  # Distancia a la pantalla (cm)
        self.y_position = tk.DoubleVar(value=0)  # Posición Y en la pantalla (mm)

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
        self.screen_canvas.bind("<Motion>", self.show_intensity)

        # Canvas para la distribución de intensidad
        self.distribution_canvas = tk.Canvas(self.distribution_frame, width=600, height=200, bg='black')
        self.distribution_canvas.pack(pady=10)

        # Etiquetas
        tk.Label(self.screen_frame,
                 text="Proyección en Pantalla",
                 bg='black', fg='cyan',
                 font=('Arial', 12)).pack()

        tk.Label(self.distribution_frame,
                 text="Distribución de Intensidad",
                 bg='black', fg='cyan',
                 font=('Arial', 12)).pack()

        self.intensity_label = tk.Label(self.screen_frame,
                                        text="Intensidad: ",
                                        bg='black', fg='cyan',
                                        font=('Arial', 10))
        self.intensity_label.pack()

        self.create_controls()
        self.update_simulation()

    def create_controls(self):
        control_frame = tk.Frame(self.root, bg='black')
        control_frame.pack(side=tk.BOTTOM, pady=10)

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

        # Control para la posición Y en la pantalla
        tk.Scale(control_frame,
                 variable=self.y_position,
                 from_=-10, to=10,
                 resolution=0.1,
                 label='Posición Y en la Pantalla (mm)',
                 orient='horizontal',
                 command=lambda x: self.update_simulation(),
                 length=200,
                 bg='black',
                 fg='cyan').pack(pady=5)

    def draw_laser_beam(self):
        """Dibuja el haz láser con rayos calculados usando fórmulas ópticas"""
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
                                      text="Láser", fill='white')

        # Parámetros del sistema óptico
        f = self.focal_length * 1e-2  # Distancia focal en metros
        d1 = (lens_x - laser_x) * 1e-2  # Distancia del láser a la lente en metros
        d2 = (slit_x - lens_x) * 1e-2  # Distancia de la lente a la rendija en metros

        # Calcular la posición de la imagen usando la fórmula de la lente delgada
        d2_calc = 1 / (1 / f - 1 / d1)

        # Número de rayos a dibujar
        n_rays = 5
        ray_spread = self.beam_width / 2  # Mitad del ancho del haz láser

        for i in range(n_rays):
            # Posición vertical inicial del rayo
            y_offset = (i - (n_rays - 1) / 2) * ray_spread

            # Rayo antes de la lente
            self.setup_canvas.create_line(laser_x, center_y + y_offset,
                                          lens_x, center_y + y_offset,
                                          fill='red', width=1)

            # Calcular la altura del rayo en la rendija usando la fórmula de aumento
            m = -d2_calc / d1
            y_at_slit = m * y_offset

            # Rayo desde la lente hasta la rendija
            self.setup_canvas.create_line(lens_x, center_y + y_offset,
                                          slit_x, center_y + y_at_slit,
                                          fill='red', width=1)

            # Rayo desde la rendija hasta la pantalla
            self.setup_canvas.create_line(slit_x, center_y + y_at_slit,
                                          screen_x, center_y + y_at_slit,
                                          fill='red', width=1)

        # Dibujar la lente (simplificada)
        lens_height = 80
        self.setup_canvas.create_line(lens_x, center_y - lens_height / 2,
                                      lens_x, center_y + lens_height / 2,
                                      fill='cyan', width=2)
        self.setup_canvas.create_text(lens_x, center_y + lens_height / 2 + 15,
                                      text=f"Lente (f={self.focal_length}cm)", fill='white')

        # Dibujar la rendija
        slit_height = 80
        self.setup_canvas.create_line(slit_x, center_y - slit_height / 2,
                                      slit_x, center_y + slit_height / 2,
                                      fill='yellow', width=2)
        self.setup_canvas.create_text(slit_x, center_y + slit_height / 2 + 15,
                                      text="Rendija", fill='white')

        # Dibujar la pantalla
        screen_height = 160
        self.setup_canvas.create_line(screen_x, center_y - screen_height / 2,
                                      screen_x, center_y + screen_height / 2,
                                      fill='white', width=2)
        self.setup_canvas.create_text(screen_x, center_y + screen_height / 2 + 15,
                                      text="Pantalla", fill='white')

    def calculate_diffraction_pattern(self, y):
        """Calcula el patrón de difracción de una rendija única usando la fórmula de Fraunhofer"""
        a = self.slit_width.get() * 1e-3  # Ancho de la rendija en metros
        L = self.screen_distance.get() * 1e-2  # Distancia a la pantalla en metros
        k = 2 * math.pi / self.wavelength  # Número de onda

        theta = math.atan(y / L)
        beta = k * a * math.sin(theta) / 2

        if beta == 0:
            return 1.0
        else:
            return (math.sin(beta) / beta) ** 2

    def draw_screen_pattern(self):
        """Dibuja el patrón de difracción en la pantalla"""
        width = 400
        height = 400

        # Limpiar el canvas de la pantalla
        self.screen_canvas.delete('all')

        # Dibujar el marco de la pantalla
        self.screen_canvas.create_rectangle(10, 10, width - 10, height - 10, outline='white')

        # Calcular y dibujar el patrón de difracción
        y_scale = 1e-3  # Factor de escala para la coordenada y (en metros)

        # Calcular intensidades
        y_values = [(py - height / 2) * y_scale for py in range(height)]
        intensities = [self.calculate_diffraction_pattern(y) for y in y_values]

        # Normalizar intensidades
        max_intensity = max(intensities)
        if max_intensity > 0:
            intensities = [i / max_intensity for i in intensities]

        # Dibujar el patrón
        for py, intensity in enumerate(intensities):
            color = self.intensity_to_color(intensity)
            self.screen_canvas.create_line(10, py, width - 10, py, fill=color)

        # Dibujar el punto ajustable
        y_pixel = int(height / 2 - self.y_position.get() / y_scale)
        self.screen_canvas.create_oval(width / 2 - 5, y_pixel - 5, width / 2 + 5, y_pixel + 5, fill='yellow', outline='yellow')

    def intensity_to_color(self, intensity):
        """Convierte una intensidad (0-1) a un color RGB"""
        red = int(255 * intensity)
        return f'#{red:02x}0000'

    def draw_intensity_distribution(self):
        """Dibuja la distribución de intensidad usando tkinter"""
        width = 600
        height = 200
        margin = 20
        x_scale = (width - 2 * margin) / 20  # 20mm range centered at 0
        y_scale = height - 2 * margin

        # Limpiar el canvas
        self.distribution_canvas.delete('all')

        # Dibujar ejes
        self.distribution_canvas.create_line(margin, height - margin, width - margin, height - margin,
                                             fill='white')  # Eje X
        self.distribution_canvas.create_line(margin, height - margin, margin, margin, fill='white')  # Eje Y

        # Etiquetas de los ejes
        self.distribution_canvas.create_text(width / 2, height - 5, text="Posición Y (mm)", fill='white')
        self.distribution_canvas.create_text(10, height / 2, text="Intensidad Relativa", angle=90, fill='white')

        # Calcular y dibujar la distribución de intensidad
        points = []
        for x in range(width):
            y = (x - width / 2) / x_scale  # Convertir pixel a mm
            intensity = self.calculate_diffraction_pattern(y * 1e-3)  # Convertir mm a m
            y_pixel = height - margin - int(intensity * y_scale)
            points.append(x)
            points.append(y_pixel)

        # Dibujar la curva de intensidad
        self.distribution_canvas.create_line(points, fill='red', smooth=True)

        # Dibujar marcas en el eje X
        for i in range(-10, 11, 5):
            x = margin + (i + 10) * x_scale
            self.distribution_canvas.create_line(x, height - margin, x, height - margin + 5, fill='white')
            self.distribution_canvas.create_text(x, height - margin + 10, text=str(i), fill='white')

        # Dibujar marcas en el eje Y
        for i in range(0, 11, 2):
            y = height - margin - i * (y_scale / 10)
            self.distribution_canvas.create_line(margin - 5, y, margin, y, fill='white')
            self.distribution_canvas.create_text(margin - 10, y, text=f"{i / 10:.1f}", fill='white')

        # Dibujar línea vertical en la posición Y actual
        current_y = self.y_position.get()
        x_current = margin + (current_y + 10) * x_scale
        self.distribution_canvas.create_line(x_current, margin, x_current, height - margin, fill='yellow', dash=(4, 4))

    def show_intensity(self, event):
        """Muestra la intensidad en el punto donde está el cursor"""
        width = 400
        height = 400
        y_scale = 1e-3  # Factor de escala para la coordenada y (en metros)

        # Calcular la posición y en metros
        y = (event.y - height / 2) * y_scale

        # Calcular la intensidad en ese punto
        intensity = self.calculate_diffraction_pattern(y)

        # Actualizar la etiqueta con la intensidad
        self.intensity_label.config(text=f"Intensidad: {intensity:.4f} W/m²")

    def update_simulation(self):
        """Actualiza toda la simulación"""
        self.setup_canvas.delete('all')
        self.screen_canvas.delete('all')
        self.distribution_canvas.delete('all')
        self.draw_laser_beam()
        self.draw_screen_pattern()
        self.draw_intensity_distribution()

        # Actualizar la intensidad en el punto ajustable
        y = self.y_position.get() * 1e-3  # Convertir mm a metros
        intensity = self.calculate_diffraction_pattern(y)
        self.intensity_label.config(text=f"Intensidad en Y={self.y_position.get():.1f} mm: {intensity:.4f} W/m²")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LaserDiffractionSimulation()
    app.run()
#Falta redimensionar los paneles
print("Simulation code has been updated. Run the simulation by creating an instance of LaserDiffractionSimulation and calling its run method.")