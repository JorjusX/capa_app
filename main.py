from tkinter import *
import pygame
import os
import pandas as pd
from utils.capitas.capa1 import Capa1
from utils.capitas.capa2 import Capa2
from utils.capitas.capa3 import Capa3
import csv
from datetime import datetime
import random

class Main(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master

        self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.fondo = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/fondo.png'))
        self.canvas = Canvas(self.root, width=800, height=400)
        self.canvas.config(width=1920, height=678)
        self.canvas.pack()
        
        self.imagen_mira = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/mira.png'))
        self.puntuaciones = open("puntuaciones.csv")
                
        self.disparos = []
        self.score = 0
        self.vidas = int(3)
        self.fallos = 0
        self.rondas_superadas = 0
        self.tiempo_vida = 7
        self.hight_score = self.mejor_puntuacion()
        
        self.juego_iniciado = False
        self.sonido_activo = True
        self.root.bind("s", self.toggle_sonido)
        
        self.canvas.bind("<Button-1>", self.disparar)
        self.canvas.bind("<Motion>", self.mover_mira)
        self.canvas.bind("<Button-1>", self.dibujar_mira)
        
        self.mostrar_pantalla_inicio()
        
        pygame.mixer.init()
        
        self.sonido_disparo = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/disparo.wav'))
        self.sonido_explosion = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/explosion.wav'))
        self.sonido_game_over = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/game_over.wav'))

        self.capa1 = Capa1(self.canvas, self.vidas, self.base_path, self.tiempo_vida)
        self.capa2 = Capa2(self.canvas, self.vidas, self.base_path, self.tiempo_vida)
        self.capa3 = Capa3(self.canvas, self.vidas, self.base_path, self.tiempo_vida)

        self.capas = [self.capa1, self.capa2, self.capa3]
        
    def mostrar_pantalla_inicio(self):
        self.juego_iniciado = False
        self.canvas.delete("all")
        self.canvas.unbind("<Button-1>")
        self.canvas.create_image(400, 200, image=self.fondo)
        self.canvas.create_text(400, 150, text="Tiro al Capa", font=("Arial", 32), fill="white")
        self.canvas.create_text(400, 200, text="Haz clic para empezar", font=("Arial", 24), fill="white")
        
        self.canvas.create_rectangle(50, 350, 250, 250, fill="skyblue", tags=("inicio",))
        self.canvas.create_text(150, 300, text="Modo normal", font=("Arial", 24), fill="purple", tags=("inicio",))
        self.canvas.create_text(150, 325, text=f"Puntuacion maxima: {self.hight_score}", font=("Arial", 10), fill="purple", tags=("inicio",))

        self.canvas.create_rectangle(550, 350, 750, 250, fill="skyblue", tags=("inicio2",))
        self.canvas.create_text(650, 300, text="Modo durisimo", font=("Arial", 20), fill="white", tags=("inicio2",))

        self.canvas.tag_bind("inicio", "<Button-1>", lambda event: self.iniciar_juego(event, modo_durisimo=False))
        self.canvas.tag_bind("inicio2", "<Button-1>", lambda event: self.iniciar_juego(event, modo_durisimo=True))
               
    def iniciar_juego(self, event, modo_durisimo=False):
        self.juego_iniciado = True
        self.modo_durisimo = modo_durisimo
        self.canvas.config(cursor="none")
        self.canvas.delete("all")
        self.root.unbind("<Button-1>")
        self.root.after(100, lambda: self.root.bind("<Button-1>", self.disparar))
        self.score = 0
        self.vidas = 1 if modo_durisimo else 3
        self.fallos = 0
        self.rondas_superadas = 0 if not modo_durisimo else None
        self.canvas.create_image(400, 200, image=self.fondo)

        self.mira = self.canvas.create_image(0, 0, image=self.imagen_mira)
        self.actualizar_puntuacion()
        self.canvas.bind("<Motion>", self.mover_mira)

        if modo_durisimo:
            self.capa1.vidas=1
            self.capa2.vidas=1
            self.capa3.vidas=1
            self.capa1.cantidad = 5
            self.capa1.crear_capas()
            self.capa2.cantidad = 1
            self.capa2.crear_capas()
            self.capa3.cantidad = 1
            self.capa3.crear_capas()

        self.root.after(100, self.actualizar_objetos)
        
    def toggle_sonido(self, event):
        self.sonido_activo = not self.sonido_activo
        estado = "activado" if self.sonido_activo else "desactivado"
        print(f"Sonido {estado}")
        
    def disparar(self, event):
        if not self.juego_iniciado:
            return

        if self.sonido_activo:
            self.sonido_disparo.play()

        disparo = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill="red")
        self.disparos.append(disparo)
        disparo_bbox = self.canvas.bbox(disparo)

        for capa in self.capas:
            if capa.verificar_colision(disparo_bbox):
                self.canvas.delete(disparo)
                self.score += 10 if capa == self.capa1 else 20 if capa == self.capa2 else 30
                self.actualizar_puntuacion()
                if self.sonido_activo:
                    self.sonido_explosion.play()
                return

        self.fallos += 1
        self.actualizar_puntuacion()
    
    def dibujar_mira(self, event):
        self.canvas.delete(self.mira)
        self.mira = self.canvas.create_image(event.x,event.y,image=self.imagen_mira)
        
    def mover_mira(self, event):
        self.canvas.coords(self.mira, event.x, event.y)
        
    def actualizar_objetos(self):
        nueva_ronda = True

        for capa in self.capas:
            if not capa.capas:
                continue
            nueva_ronda = False
            vidas_capa = capa.actualizar()
            self.vidas = min(self.vidas, vidas_capa)

        if self.vidas <= 0:
            self.game_over()
            return

        if nueva_ronda:
            if self.modo_durisimo:
                self.capa1.crear_capas()
                self.capa2.cantidad = 1
                self.capa2.crear_capas()
                self.capa3.cantidad = 1
                self.capa3.crear_capas()
            else:
                self.rondas_superadas += 1
                print(f"Ronda {self.rondas_superadas} iniciada")
                self.dificultar()

        self.actualizar_puntuacion()
        self.root.after(100, self.actualizar_objetos)
        
    def dificultar(self):
        self.capa1.cantidad=5
        
        self.capa1.i_velocidad += 0.5

        if self.rondas_superadas >= 5 and random.random() <= 0.5:
            self.capa2.cantidad = 1
            self.capa1.cantidad-=1
            self.capa2.crear_capas()

        if self.rondas_superadas >= 7 and random.random() <= 1/3:
            self.capa3.cantidad = 1
            self.capa1.cantidad-=1
            self.capa3.crear_capas()
        self.capa1.crear_capas()
        self.capa3.i_velocidad = self.capa1.i_velocidad

    def actualizar_puntuacion(self):
        self.canvas.delete("score")
        self.canvas.create_text(70, 20, text=f"Puntuación: {self.score}", font=("Arial", 16), fill="white", tag="score")
        self.canvas.create_text(50, 40, text=f"Vidas: {self.vidas}", font=("Arial", 16), fill="white", tag="score")
        self.canvas.create_text(50, 60, text=f"Fallos: {self.fallos}", font=("Arial", 16), fill="white", tag="score")
        if not self.modo_durisimo:
            self.canvas.create_text(50, 80, text=f"Ronda: {self.rondas_superadas}", font=("Arial", 16), fill="white", tag="score")

    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_image(400, 200, image=self.fondo)
        if self.sonido_activo:
            self.sonido_game_over.play()
        self.canvas.create_text(400, 150, text="¡Game Over!", font=("Arial", 32), fill="red")
        self.canvas.create_text(400, 200, text=f"Puntuación final: {self.score}", font=("Arial", 24), fill="white")
        self.canvas.create_text(400, 230, text=f"Fallos: {self.fallos}", font=("Arial", 24), fill="white")
        self.canvas.create_text(400, 260, text=f"Rondas superadas: {self.rondas_superadas}", font=("Arial", 24), fill="white")
        self.canvas.create_text(400, 300, text="Haz clic para volver al menú", font=("Arial", 24), fill="white")        
        with open(os.path.join(self.base_path, "puntuaciones.csv"), mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.score, self.fallos, self.rondas_superadas])        
        self.juego_iniciado = False
        self.disparos.clear()        
        self.canvas.config(cursor="arrow")        
        self.canvas.bind("<Button-1>", lambda event: self.mostrar_pantalla_inicio())

    def mejor_puntuacion(self):
        try:
            with open(os.path.join(self.base_path, "puntuaciones.csv"), mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                puntuaciones = [int(row[1]) for row in reader if row]
                return max(puntuaciones) if puntuaciones else 0
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0
        
if __name__ == "__main__":
    root = Tk()
    root.title('Tiro al Capa')
    root.geometry('800x400')
    root.call('wm', 'iconphoto', root._w, PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/imgs/capa_icon.png')))
    app = Main(root)
    root.resizable(False, False)
    app.mainloop()