import tkinter as tk
import math

class SimulacionDifraccionLaser:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Simulador de Láser con Lente y Rendija")
        self.raiz.configure(bg='black')

        # Constantes físicas
        self.longitud_onda = 633e-9  # Longitud de onda del láser HeNe (rojo)
        self.k = 2 * math.pi / self.longitud_onda
        self.ancho_haz = 2  # Ancho del haz láser en mm
        self.distancia_focal = 50  # Distancia focal fija de la lente (cm)

        # Parámetros ajustables
        self.ancho_rendija = tk.DoubleVar(value=0.1)  # Ancho de la rendija (mm)
        self.distancia_pantalla = tk.DoubleVar(value=100)  # Distancia a la pantalla (cm)
        self.posicion_y = tk.DoubleVar(value=0)  # Posición Y en la pantalla (mm)

        # Crear frames para los paneles
        self.marco_montaje = tk.Frame(self.raiz, bg='black')
        self.marco_montaje.pack(side=tk.LEFT, padx=10, pady=10)

        self.marco_pantalla = tk.Frame(self.raiz, bg='black')
        self.marco_pantalla.pack(side=tk.RIGHT, padx=10, pady=10)

        self.marco_distribucion = tk.Frame(self.raiz, bg='black')
        self.marco_distribucion.pack(side=tk.BOTTOM, fill=tk.X, expand=True, padx=10, pady=10)

        # Canvas para el montaje óptico y la pantalla
        self.lienzo_montaje = tk.Canvas(self.marco_montaje, width=600, height=400, bg='black')
        self.lienzo_montaje.pack(pady=10)

        self.lienzo_pantalla = tk.Canvas(self.marco_pantalla, width=400, height=400, bg='black')
        self.lienzo_pantalla.pack(pady=10)
        self.lienzo_pantalla.bind("<Motion>", self.mostrar_intensidad)

        # Canvas para la distribución de intensidad
        self.lienzo_distribucion = tk.Canvas(self.marco_distribucion,
                                             width=self.raiz.winfo_screenwidth(),
                                             height=200,
                                             bg='black')
        self.lienzo_distribucion.pack(fill=tk.X, expand=True, pady=10)

        # Etiquetas
        tk.Label(self.marco_montaje,
                 text="Montaje Experimental",
                 bg='black',
                 fg='white',
                 font=('Arial', 12)).pack(pady=5)
        tk.Label(self.marco_pantalla,
                 text="Proyección en Pantalla",
                 bg='black', fg='cyan',
                 font=('Arial', 12)).pack()

        tk.Label(self.marco_distribucion,
                 text="Distribución de Intensidad",
                 bg='black', fg='cyan',
                 font=('Arial', 12)).pack()

        self.etiqueta_intensidad = tk.Label(self.marco_pantalla,
                                            text="Intensidad: ",
                                            bg='black', fg='cyan',
                                            font=('Arial', 10))
        self.etiqueta_intensidad.pack()

        self.crear_controles()
        self.actualizar_simulacion()

    def crear_controles(self):
        marco_control = tk.Frame(self.raiz, bg='black')
        marco_control.pack(side=tk.BOTTOM, pady=10)

        # Control para el ancho de la rendija
        tk.Scale(marco_control,
                 variable=self.ancho_rendija,
                 from_=0.05, to=0.5,
                 resolution=0.01,
                 label='Ancho de la Rendija (mm)',
                 orient='horizontal',
                 command=lambda x: self.actualizar_simulacion(),
                 length=200,
                 bg='black',
                 fg='cyan').pack(pady=5)

        # Control para la distancia a la pantalla
        tk.Scale(marco_control,
                 variable=self.distancia_pantalla,
                 from_=50, to=600,
                 resolution=1,
                 label='Distancia a la Pantalla (cm)',
                 orient='horizontal',
                 command=lambda x: self.actualizar_simulacion(),
                 length=200,
                 bg='black',
                 fg='cyan').pack(pady=5)

        # Control para la posición Y en la pantalla
        tk.Scale(marco_control,
                 variable=self.posicion_y,
                 from_=-10, to=10,
                 resolution=0.1,
                 label='Posición Y en la Pantalla (mm)',
                 orient='horizontal',
                 command=lambda x: self.actualizar_simulacion(),
                 length=200,
                 bg='black',
                 fg='cyan').pack(pady=5)

    def dibujar_haz_laser(self):
        """Dibuja el haz láser con rayos calculados usando fórmulas ópticas"""
        ancho = 600
        alto = 400
        centro_y = alto / 2

        # Posiciones de los componentes
        x_laser = 50
        x_lente = 200
        x_rendija = 400
        x_pantalla = 550

        # Dibujar el láser
        self.lienzo_montaje.create_rectangle(x_laser - 15, centro_y - 10, x_laser, centro_y + 10,
                                             fill='red', outline='yellow')
        self.lienzo_montaje.create_text(x_laser - 7, centro_y + 25,
                                        text="Láser", fill='white')

        # Parámetros del sistema óptico
        f = self.distancia_focal * 1e-2  # Distancia focal en metros
        d1 = (x_lente - x_laser) * 1e-2  # Distancia del láser a la lente en metros
        d2 = (x_rendija - x_lente) * 1e-2  # Distancia de la lente a la rendija en metros

        # Calcular la posición de la imagen usando la fórmula de la lente delgada
        d2_calc = 1 / (1 / f - 1 / d1)

        # Número de rayos a dibujar
        n_rayos = 5
        separacion_rayos = self.ancho_haz / 2  # Mitad del ancho del haz láser

        for i in range(n_rayos):
            # Posición vertical inicial del rayo
            desplazamiento_y = (i - (n_rayos - 1) / 2) * separacion_rayos

            # Rayo antes de la lente
            self.lienzo_montaje.create_line(x_laser, centro_y + desplazamiento_y,
                                            x_lente, centro_y + desplazamiento_y,
                                            fill='red', width=1)

            # Calcular la altura del rayo en la rendija usando la fórmula de aumento
            m = -d2_calc / d1
            y_en_rendija = m * desplazamiento_y

            # Rayo desde la lente hasta la rendija
            self.lienzo_montaje.create_line(x_lente, centro_y + desplazamiento_y,
                                            x_rendija, centro_y + y_en_rendija,
                                            fill='red', width=1)

            # Rayo desde la rendija hasta la pantalla
            self.lienzo_montaje.create_line(x_rendija, centro_y + y_en_rendija,
                                            x_pantalla, centro_y + y_en_rendija,
                                            fill='red', width=1)

        # Dibujar la lente (simplificada)
        altura_lente = 80
        self.lienzo_montaje.create_line(x_lente, centro_y - altura_lente / 2,
                                        x_lente, centro_y + altura_lente / 2,
                                        fill='cyan', width=2)
        self.lienzo_montaje.create_text(x_lente, centro_y + altura_lente / 2 + 15,
                                        text=f"Lente (f={self.distancia_focal}cm)", fill='white')

        # Dibujar la rendija
        altura_rendija = 80
        self.lienzo_montaje.create_line(x_rendija, centro_y - altura_rendija / 2,
                                        x_rendija, centro_y + altura_rendija / 2,
                                        fill='yellow', width=2)
        self.lienzo_montaje.create_text(x_rendija, centro_y + altura_rendija / 2 + 15,
                                        text="Rendija", fill='white')

        # Dibujar la pantalla
        altura_pantalla = 160
        self.lienzo_montaje.create_line(x_pantalla, centro_y - altura_pantalla / 2,
                                        x_pantalla, centro_y + altura_pantalla / 2,
                                        fill='white', width=2)
        self.lienzo_montaje.create_text(x_pantalla, centro_y + altura_pantalla / 2 + 15,
                                        text="Pantalla", fill='white')

    def calcular_patron_difraccion(self, y):
        """Calcula el patrón de difracción de una rendija única usando la fórmula de Fraunhofer"""
        a = self.ancho_rendija.get() * 1e-3  # Ancho de la rendija en metros
        L = self.distancia_pantalla.get() * 1e-2  # Distancia a la pantalla en metros
        k = 2 * math.pi / self.longitud_onda  # Número de onda

        theta = math.atan(y / L)
        beta = k * a * math.sin(theta) / 2

        if beta == 0:
            return 1.0
        else:
            return (math.sin(beta) / beta) ** 2

    def dibujar_patron_pantalla(self):
        """Dibuja el patrón de difracción en la pantalla"""
        ancho = 400
        alto = 400

        # Limpiar el canvas de la pantalla
        self.lienzo_pantalla.delete('all')

        # Dibujar el marco de la pantalla
        self.lienzo_pantalla.create_rectangle(10, 10, ancho - 10, alto - 10, outline='white')

        # Calcular y dibujar el patrón de difracción
        escala_y = 1e-3  # Factor de escala para la coordenada y (en metros)

        # Calcular intensidades
        valores_y = [(py - alto / 2) * escala_y for py in range(alto)]
        intensidades = [self.calcular_patron_difraccion(y) for y in valores_y]

        # Normalizar intensidades
        intensidad_maxima = max(intensidades)
        if intensidad_maxima > 0:
            intensidades = [i / intensidad_maxima for i in intensidades]

        # Dibujar el patrón
        for py, intensidad in enumerate(intensidades):
            color = self.intensidad_a_color(intensidad)
            self.lienzo_pantalla.create_line(10, py, ancho - 10, py, fill=color)

        # Dibujar el punto ajustable
        y_pixel = int(alto / 2 - self.posicion_y.get() / escala_y)


    def intensidad_a_color(self, intensidad):
        """Convierte una intensidad (0-1) a un color RGB"""
        rojo = int(255 * intensidad)
        return f'#{rojo:02x}0000'

    def dibujar_distribucion_intensidad(self):
        """Dibuja la distribución de intensidad usando tkinter"""
        ancho = self.lienzo_distribucion.winfo_width()  # Obtener el ancho real del canvas
        alto = 200
        margen = 20
        escala_x = (ancho - 2 * margen) / 20  # Rango de 20mm centrado en 0
        escala_y = alto - 2 * margen

        # Limpiar el canvas
        self.lienzo_distribucion.delete('all')

        # Dibujar ejes
        self.lienzo_distribucion.create_line(margen, alto - margen, ancho - margen, alto - margen,
                                             fill='white')  # Eje X
        self.lienzo_distribucion.create_line(margen, alto - margen, margen, margen, fill='white')  # Eje Y

        # Etiquetas de los ejes
        self.lienzo_distribucion.create_text(ancho / 2, alto - 5, text="", fill='white')
        self.lienzo_distribucion.create_text(10, alto / 2, text="", angle=90, fill='white')

        # Calcular y dibujar la distribución de intensidad
        puntos = []
        for x in range(ancho):
            y = (x - ancho / 2) / escala_x  # Convertir pixel a mm
            intensidad = self.calcular_patron_difraccion(y * 1e-3)  # Convertir mm a m
            y_pixel = alto - margen - int(intensidad * escala_y)
            puntos.extend([x, y_pixel])

        # Asegurarse de que hay al menos dos puntos antes de dibujar la línea
        if len(puntos) >= 4:
            self.lienzo_distribucion.create_line(puntos, fill='red', smooth=True)

        # Dibujar marcas en el eje X
        for i in range(-10, 11, 5):
            x = margen + (i + 10) * escala_x
            self.lienzo_distribucion.create_line(x, alto - margen, x, alto - margen + 5, fill='white')
            self.lienzo_distribucion.create_text(x, alto - margen + 10, text=str(i), fill='white')

        # Dibujar marcas en el eje Y
        for i in range(0, 11, 2):
            y = alto - margen - i * (escala_y / 10)
            self.lienzo_distribucion.create_line(margen - 5, y, margen, y, fill='white')
            self.lienzo_distribucion.create_text(margen - 10, y, text=f"{i / 10:.1f}", fill='white')

        # Dibujar línea vertical en la posición Y actual
        y_actual = self.posicion_y.get()
        x_actual = margen + (y_actual + 10) * escala_x
        self.lienzo_distribucion.create_line(x_actual, margen, x_actual, alto - margen, fill='yellow', dash=(4, 4))

    def mostrar_intensidad(self, evento):
        """Muestra la intensidad en el punto donde está el cursor"""
        ancho = 400
        alto = 400
        escala_y = 1e-3  # Factor de escala para la coordenada y (en metros)

        # Calcular la posición y en metros
        y = (evento.y - alto / 2) * escala_y

        # Calcular la intensidad en ese punto
        intensidad = self.calcular_patron_difraccion(y)

        # Actualizar la etiqueta con la intensidad
        self.etiqueta_intensidad.config(text=f"Intensidad: {intensidad:.4f} W/m²")

    def actualizar_simulacion(self):
        """Actualiza toda la simulación"""
        self.lienzo_montaje.delete('all')
        self.lienzo_pantalla.delete('all')
        self.lienzo_distribucion.delete('all')
        self.dibujar_haz_laser()
        self.dibujar_patron_pantalla()
        self.dibujar_distribucion_intensidad()

        # Actualizar la intensidad en el punto ajustable
        y = self.posicion_y.get() * 1e-3  # Convertir mm a metros
        intensidad = self.calcular_patron_difraccion(y)
        self.etiqueta_intensidad.config(text=f"Intensidad en Y={self.posicion_y.get():.1f} mm: {intensidad:.4f} W/m²")

    def ejecutar(self):
        self.raiz.mainloop()

if __name__ == "__main__":
    app = SimulacionDifraccionLaser()
    app.ejecutar()

print("El código de la simulación ha sido actualizado. Ejecute la simulación creando una instancia de SimulacionDifraccionLaser y llamando a su método ejecutar.")