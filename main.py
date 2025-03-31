from tkinter import *
import pygame
import os
from utils.capitas.capa1 import Capa1

class Main(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master

        self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.fondo = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/fondo.png'))
        self.canvas = Canvas(self.root, width=800, height=400)
        self.canvas.config(width=1920, height=678)
        self.canvas.pack()
        
        self.imagen_capa1 = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/capa1.png'))
        self.imagen_mira = PhotoImage(file=os.path.join(self.base_path, 'src/imgs/mira.png'))
                
        self.disparos = []
        self.score = 0
        self.lives = 3
        self.fallos = 0
        self.velocidad_base = 3
        self.rondas_superadas = 0
        
        self.canvas.bind("<Button-1>", self.disparar)
        self.canvas.config(cursor="none")
        self.canvas.bind("<Motion>", self.mover_mira)
        
        self.mostrar_pantalla_inicio()
        
        pygame.mixer.init()
        
        # Cargar sonidos
        self.sonido_disparo = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/disparo.wav'))
        self.sonido_explosion = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/explosion.wav'))
        self.sonido_perder_vida = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/capa.wav'))
        self.sonido_game_over = pygame.mixer.Sound(os.path.join(self.base_path, 'src/sounds/game_over.wav'))

        # Crear instancia de Capa1
        self.capa1 = Capa1(self.canvas, self.imagen_capa1, self.velocidad_base)
        
    def mostrar_pantalla_inicio(self):
        self.canvas.delete("all")
        self.canvas.create_image(400, 200, image=self.fondo)
        self.canvas.create_text(400, 150, text="Tiro al Capa", font=("Arial", 32), fill="white")
        self.canvas.create_text(400, 200, text="Haz clic para empezar", font=("Arial", 24), fill="white")
        self.canvas.bind("<Button-1>", self.iniciar_juego)
               
    def iniciar_juego(self, event):
        self.canvas.delete("all")
        self.score = 0
        self.lives = 3
        self.fallos = 0
        self.velocidad_base = 3
        self.rondas_superadas = 0
        self.canvas.create_image(400, 200, image=self.fondo)
        self.capa1.crear_capas()
        self.mira = self.canvas.create_image(0, 0, image=self.imagen_mira)
        self.canvas.bind("<Button-1>", self.disparar)
        self.actualizar_puntuacion()
        self.root.after(100, self.actualizar_objetos)
        
    def disparar(self, event):
        self.sonido_disparo.play()
        
        disparo = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill="red")
        self.disparos.append(disparo)
        disparo_bbox = self.canvas.bbox(disparo)
        if self.capa1.verificar_colision(disparo_bbox):
            self.canvas.delete(disparo)
            self.score += 10
            self.actualizar_puntuacion()
            self.sonido_explosion.play()
        else:
            self.fallos += 1
            self.actualizar_puntuacion()
        
    def mover_mira(self, event):
        self.canvas.coords(self.mira, event.x, event.y)
        
    def actualizar_objetos(self):
        self.capa1.mover_capas()
        if not self.capa1.capas:
            self.velocidad_base += 1
            self.rondas_superadas += 1
            self.capa1.crear_capas()
        self.root.after(100, self.actualizar_objetos)

    def actualizar_puntuacion(self):
        self.canvas.delete("score")
        self.canvas.create_text(50, 20, text=f"Puntuación: {self.score}", font=("Arial", 16), fill="white", tag="score")
        self.canvas.create_text(50, 40, text=f"Vidas: {self.lives}", font=("Arial", 16), fill="white", tag="score")
        self.canvas.create_text(50, 60, text=f"Fallos: {self.fallos}", font=("Arial", 16), fill="white", tag="score")

    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_image(400, 200, image=self.fondo)
        self.canvas.create_text(400, 150, text="¡Game Over!", font=("Arial", 32), fill="red")
        self.canvas.create_text(400, 200, text=f"Puntuación final: {self.score}", font=("Arial", 24), fill="white")
        self.canvas.create_text(400, 230, text=f"Fallos: {self.fallos}", font=("Arial", 24), fill="white")
        self.canvas.create_text(400, 260, text=f"Rondas superadas: {self.rondas_superadas}", font=("Arial", 24), fill="white")
        self.canvas.create_text(400, 300, text="Haz clic para volver a intentarlo", font=("Arial", 24), fill="white")
        self.canvas.bind("<Button-1>", self.iniciar_juego)
        self.sonido_game_over.play()
        
if __name__ == "__main__":
    root = Tk()
    root.title('Tiro al Capa')
    root.geometry('800x400')
    root.call('wm', 'iconphoto', root._w, PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/imgs/capa2.png')))    
    app = Main(root)
    root.resizable(False, False)
    app.mainloop()