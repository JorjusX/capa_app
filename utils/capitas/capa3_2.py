import random
import time
import os
import pygame
from tkinter import PhotoImage

class Capa3:
    def __init__(self, canvas, vidas, base_path, tiempo_vida):
        self.canvas = canvas
        self.base_path = base_path
        self.tiempo_vida = tiempo_vida
        self.velocidad_base = 2.5
        self.i_velocidad = 0
        self.vidas = vidas
        self.capas = []
        self.vida_perdida = False

        self.imagen = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/capa3.png'))
        self.imagen_pequena = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/capa3_small.png'))
        self.sonido_division = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/burbuja.wav'))

        self.cantidad = 1

    def crear_capas(self):
        """Crea una cantidad de capas con posiciones y velocidades aleatorias."""
        self.capas = []
        for _ in range(self.cantidad):
            capa = self.canvas.create_image(
                random.randint(50, 750), random.randint(50, 275), image=self.imagen
            )
            velocidad = random.uniform(
                self.velocidad_base + self.i_velocidad,
                self.velocidad_base + 2 + self.i_velocidad
            )
            direccion_x = random.choice([-1, 1])
            direccion_y = random.choice([-1, 1])
            tiempo_aparicion = time.time()
            tiempo_vida = self.tiempo_vida
            self.capas.append({
                "capa": capa,
                "velocidad": velocidad,
                "direccion_x": direccion_x,
                "direccion_y": direccion_y,
                "tiempo_aparicion": tiempo_aparicion,
                "tiempo_vida": tiempo_vida,
                "es_pequena": False
            })

    def dividir_capa(self, capa):
        """Divide una capa en 3 capas más pequeñas."""
        pos = self.canvas.coords(capa["capa"])
        self.eliminar_capa(capa)
        for _ in range(3):
            # Asegurarse de que las copias no se creen fuera del marco
            nueva_x = max(20, min(780, pos[0] + random.randint(-20, 20)))
            nueva_y = max(20, min(380, pos[1] + random.randint(-20, 20)))
            nueva_capa = self.canvas.create_image(
                nueva_x,
                nueva_y,
                image=self.imagen_pequena
            )
            velocidad = random.uniform(
                self.velocidad_base + self.i_velocidad,
                self.velocidad_base + 2 + self.i_velocidad
            )
            direccion_x = random.choice([-1, 1])
            direccion_y = random.choice([-1, 1])
            tiempo_aparicion = time.time()
            tiempo_vida = self.tiempo_vida
            self.capas.append({
                "capa": nueva_capa,
                "velocidad": velocidad,
                "direccion_x": direccion_x,
                "direccion_y": direccion_y,
                "tiempo_aparicion": tiempo_aparicion,
                "tiempo_vida": tiempo_vida,
                "es_pequena": True
            })

    def mover_capas(self):
        """Mueve las capas en el canvas y gestiona colisiones con los bordes."""
        for capa in self.capas[:]:
            pos = self.canvas.coords(capa["capa"])
            if pos:
                self.canvas.move(
                    capa["capa"],
                    capa["velocidad"] * capa["direccion_x"],
                    capa["velocidad"] * capa["direccion_y"]
                )
                # Rebotar en los bordes del canvas
                if pos[0] <= 20 or pos[0] >= 780:  # Ajustar límites para evitar quedarse atascados
                    capa["direccion_x"] *= -1
                if pos[1] <= 20 or pos[1] >= 380:  # Ajustar límites para evitar quedarse atascados
                    capa["direccion_y"] *= -1

    def eliminar_capa(self, capa):
        """Elimina una capa del canvas y de la lista."""
        self.capas.remove(capa)
        self.canvas.delete(capa["capa"])

    def verificar_colision(self, disparo_bbox):
        """Verifica si un disparo colisiona con alguna capa."""
        for capa in self.capas:
            capa_bbox = self.canvas.bbox(capa["capa"])
            if self.colision(disparo_bbox, capa_bbox):
                if not capa["es_pequena"]:
                    self.dividir_capa(capa)
                    self.sonido_division.play()
                else:
                    self.eliminar_capa(capa)
                return True
        return False

    def actualizar(self):
        """Actualiza el estado de las capas: movimiento y eliminación."""
        self.mover_capas()
        return self.eliminar_vida()

    def eliminar_vida(self):
        """Reduce las vidas si una capa ha excedido su tiempo de vida."""
        tiempo_actual = time.time()
        for capa in self.capas[:]:
            if tiempo_actual - capa["tiempo_aparicion"] > capa["tiempo_vida"]:
                self.eliminar_capa(capa)
                self.vida_perdida = True
        if self.vida_perdida:
            # Reproducir sonido al perder una vida
            self.sonido_division.play()
            self.vidas -= 1
            self.vida_perdida = False
        return self.vidas

    @staticmethod
    def colision(bbox1, bbox2):
        """Determina si dos bounding boxes colisionan."""
        return not (
            bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or
            bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3]
        )