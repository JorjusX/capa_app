import random
import time
import pygame
import os
from tkinter import PhotoImage

class Capa2:
    def __init__(self, canvas, vidas, base_path):
        self.canvas = canvas
        self.base_path = base_path
        self.velocidad_base = 10
        self.vidas = vidas
        self.capas = []
        self.vida_perdida=False

        self.imagen = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/capa1.png'))
        self.sonido_perder_vida = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/capa.wav'))

        self.cantidad = 1

    def crear_capas(self):
        self.capas = []
        for _ in range(self.cantidad):
            capa = self.canvas.create_image(
                random.randint(50, 750), random.randint(50, 275), image=self.imagen
            )
            velocidad = random.randint(self.velocidad_base, self.velocidad_base + 10)
            direccion_x = random.choice([-1, 1])
            direccion_y = random.choice([-1, 1])
            tiempo_aparicion = time.time()
            tiempo_vida = 7
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
            if pos[0] <= 0 or pos[0] >= 800:
                capa["direccion_x"] *= -1
            if pos[1] <= 0 or pos[1] >= 400:
                capa["direccion_y"] *= -1
            if time.time() - capa["tiempo_aparicion"] > capa["tiempo_vida"]:
                self.vida_perdida=True
                self.eliminar_capa(capa)
                

    def eliminar_capa(self, capa):
        self.capas.remove(capa)
        self.canvas.delete(capa["capa"])

    def eliminar_vida(self):
        if self.vida_perdida==True:
            self.vidas-=1
        vidas = self.vidas
        self.vida_perdida=False
        return vidas
        

    def verificar_colision(self, disparo_bbox):
        for capa in self.capas:
            capa_bbox = self.canvas.bbox(capa["capa"])
            if self.colision(disparo_bbox, capa_bbox):
                self.eliminar_capa(capa)
                return True
        return False

    @staticmethod
    def colision(bbox1, bbox2):
        return not (
            bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or
            bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3]
        )