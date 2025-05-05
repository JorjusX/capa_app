import random
import time
import pygame
import os
from tkinter import PhotoImage

class Capa5:
    def __init__(self, canvas, vidas, base_path, tiempo_vida):
        self.canvas = canvas
        self.base_path = base_path
        self.tiempo_vida = tiempo_vida
        self.imagen = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/capa5.png'))
        self.velocidad_base = 15
        self.vidas = vidas
        self.capas = []
        self.vida_perdida = False
        self.i_velocidad = 0
        self.cantidad = 1
        self.puntuacion = 35

        self.sonido_perder_vida = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/capa.wav'))

    def crear_capas(self):
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

    def mover_capas(self):
        for capa in self.capas[:]:
            self.canvas.move(
                capa["capa"],
                capa["velocidad"] * capa["direccion_x"],
                capa["velocidad"] * capa["direccion_y"]
            )
            
            pos = self.canvas.coords(capa["capa"])
            x, y = pos[0], pos[1]

            if x <= 0 or x >= 800:
                capa["direccion_x"] *= -1
            if y <= 0 or y >= 400:
                capa["direccion_y"] *= -1

            if random.random() < 0.2:
                capa["direccion_x"] = random.choice([-1, 1])
                capa["direccion_y"] = random.choice([-1, 1])

            if time.time() - capa["tiempo_aparicion"] > capa["tiempo_vida"]:
                self.vida_perdida = True
                self.eliminar_capa(capa)

    def eliminar_capa(self, capa):
        self.capas.remove(capa)
        self.canvas.delete(capa["capa"])

    def eliminar_vida(self):
        if self.vida_perdida:
            self.sonido_perder_vida.play()
            self.vidas -= 1
            self.vida_perdida = False
        return self.vidas

    def verificar_colision(self, disparo_bbox):
        for capa in self.capas:
            capa_bbox = self.canvas.bbox(capa["capa"])
            if self.colision(disparo_bbox, capa_bbox):
                self.eliminar_capa(capa)
                return True
        return False

    def actualizar(self):
        self.mover_capas()
        return self.eliminar_vida()

    @staticmethod
    def colision(bbox1, bbox2):
        return not (
            bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or
            bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3]
        )
