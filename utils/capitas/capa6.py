import random
import time
import pygame
import os
from tkinter import PhotoImage

class Capa6:
    def __init__(self, canvas, vidas, base_path, tiempo_vida):
        self.canvas = canvas
        self.base_path = base_path
        self.tiempo_vida = tiempo_vida
        self.imagen = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/capa6.png'))
        self.velocidad_base = 13
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

    def mover_capas(self, puntero_x, puntero_y):
        for capa in self.capas:
            pos = self.canvas.coords(capa["capa"])
            x, y = pos[0], pos[1]

            distancia_x = puntero_x - x
            distancia_y = puntero_y - y
            distancia_total = max((distancia_x**2 + distancia_y**2)**0.5, 0.01)

            if distancia_total < 150:
                capa["direccion_x"] = -(distancia_x / distancia_total)
                capa["direccion_y"] = -(distancia_y / distancia_total)
            else:
                pass
            velocidad = random.uniform(
                self.velocidad_base + self.i_velocidad,
                self.velocidad_base + 4 + self.i_velocidad
            )

            dx = velocidad * capa["direccion_x"]
            dy = velocidad * capa["direccion_y"]

            margen = 40
            if x < margen:
                dx += 1
            elif x > 800 - margen:
                dx -= 1
            if y < margen:
                dy += 1
            elif y > 400 - margen:
                dy -= 1

            self.canvas.move(capa["capa"], dx, dy)

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

    def actualizar(self, puntero_x=None, puntero_y=None):
        if puntero_x is not None and puntero_y is not None:
            self.mover_capas(puntero_x, puntero_y)
        return self.eliminar_vida()


    @staticmethod
    def colision(bbox1, bbox2):
        return not (
            bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or
            bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3]
        )