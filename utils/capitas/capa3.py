import random
import time
import pygame
import os
from tkinter import PhotoImage
from tkinter import Canvas

class Capa3:
    def __init__(self, canvas, vidas, base_path, tiempo_vida):
        self.canvas = canvas
        self.base_path = base_path
        self.tiempo_vida = tiempo_vida
        self.imagen = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/capa3.png'))
        self.velocidad_base = 3
        self.vidas = vidas
        self.capas = []
        self.vida_perdida = False
        self.i_velocidad = 0
        self.cantidad = 1

        self.imagen_pequena = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/capa3_small.png'))
        self.sonido_perder_vida = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/capa.wav'))
        self.sonido_division = pygame.mixer.Sound(os.path.join(self.base_path, "src/sounds/burbuja.wav"))

    def crear_capas(self):
        """Crea una cantidad de capas con posiciones y velocidades aleatorias."""
        self.capas = []
        for _ in range(self.cantidad):
            capa = self.canvas.create_image(
                random.randint(50, 750), random.randint(50, 275), image=self.imagen
            )
            velocidad = random.uniform(
                self.velocidad_base + self.i_velocidad,
                self.velocidad_base + 4 + self.i_velocidad
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
                "tiempo_vida": tiempo_vida
            })

    def dividir_capa(self, capa):
        """Divide una capa en 3 capas más pequeñas."""
        pos = self.canvas.coords(capa["capa"])
        
        self.eliminar_capa(capa)
        for _ in range(3):
            nueva_capa = self.canvas.create_image(
                pos[0] + random.randint(-20, 20),
                pos[1] + random.randint(-20, 20),
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
            self.canvas.move(
                capa["capa"],
                capa["velocidad"] * capa["direccion_x"],
                capa["velocidad"] * capa["direccion_y"]
            )
            pos = self.canvas.coords(capa["capa"])
            if pos[0] <= 0 or pos[0] >= 800:
                capa["direccion_x"] *= -1
            if pos[1] <= 0 or pos[1] >= 400:
                capa["direccion_y"] *= -1
            if time.time() - capa["tiempo_aparicion"] > capa["tiempo_vida"]:
                self.vida_perdida = True
                self.eliminar_capa(capa)

    def eliminar_capa(self, capa):
        """Elimina una capa del canvas y de la lista."""
        self.capas.remove(capa)
        self.canvas.delete(capa["capa"])

    def eliminar_vida(self):
        if self.vida_perdida:
            self.sonido_perder_vida.play()
            self.vidas -= 1
            self.vida_perdida = False
        return self.vidas

    def verificar_colision(self, disparo_bbox):
        """Verifica si un disparo colisiona con alguna capa."""
        for capa in self.capas:
            capa_bbox = self.canvas.bbox(capa["capa"])
            if self.colision(disparo_bbox, capa_bbox):
                if not capa.get("es_pequena", False):
                    self.dividir_capa(capa)
                    self.sonido_division.play()
                else:
                    self.eliminar_capa(capa)
                return True
        return False

    def actualizar(self):
        """Actualiza el estado de las capas: movimiento, eliminación y creación."""
        self.mover_capas()
        if not self.capas:
            self.i_velocidad += 0.5
        return self.eliminar_vida()

    @staticmethod
    def colision(bbox1, bbox2):
        """Determina si dos bounding boxes colisionan."""
        return not (
            bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or
            bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3]
        )