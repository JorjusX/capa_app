from tkinter import *
import random
import time
import pygame
import os

class Main(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master

        # Obtener la ruta del directorio actual
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
        self.crear_objetos()
        self.mira = self.canvas.create_image(0, 0, image=self.imagen_mira)
        self.canvas.bind("<Button-1>", self.disparar)
        self.actualizar_puntuacion()
        self.root.after(100, self.actualizar_objetos)
        
    def crear_objetos(self):
        self.capas = []
        for _ in range(5):
            capa = self.canvas.create_image(random.randint(50, 750), random.randint(50, 275), image=self.imagen_capa1)
            velocidad = random.randint(self.velocidad_base, self.velocidad_base + 4)
            direccion_x = random.choice([-1, 1])
            direccion_y = random.choice([-1, 1])
            tiempo_aparicion = time.time()
            self.capas.append({"capa": capa, "velocidad": velocidad, "direccion_x": direccion_x, "direccion_y": direccion_y, "tiempo_aparicion": tiempo_aparicion})

    def disparar(self, event):
        # Reproducir sonido de disparo
        self.sonido_disparo.play()
        
        disparo = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill="red")
        self.disparos.append(disparo)
        if not self.verificar_colisiones(disparo):
            self.fallos += 1
            self.actualizar_puntuacion()
        
    def mover_mira(self, event):
        self.canvas.coords(self.mira, event.x, event.y)
        
    def actualizar_objetos(self):
        for capa in self.capas:
            self.canvas.move(capa["capa"], capa["velocidad"] * capa["direccion_x"], capa["velocidad"] * capa["direccion_y"])
            pos = self.canvas.coords(capa["capa"])
            if pos[0] <= 0 or pos[0] >= 800:
                capa["direccion_x"] *= -1
            if pos[1] <= 0 or pos[1] >= 400:
                capa["direccion_y"] *= -1
            if time.time() - capa["tiempo_aparicion"] > 7:
                self.capas.remove(capa)
                self.canvas.delete(capa["capa"])
                self.lives -= 1
                self.actualizar_puntuacion()
                # Reproducir sonido de perder vida
                self.sonido_perder_vida.play()
                if self.lives <= 0:
                    self.game_over()
                    return
        if not self.capas:
            self.velocidad_base += 1
            self.rondas_superadas += 1
            self.crear_objetos()
        self.root.after(100, self.actualizar_objetos)

    def verificar_colisiones(self, disparo):
        disparo_bbox = self.canvas.bbox(disparo)
        for capa in self.capas:
            capa_bbox = self.canvas.bbox(capa["capa"])
            if self.collision(disparo_bbox, capa_bbox):
                self.canvas.delete(capa["capa"])
                self.canvas.delete(disparo)
                self.capas.remove(capa)
                self.score += 10
                self.actualizar_puntuacion()
                # Reproducir sonido de explosión
                self.sonido_explosion.play()
                return True
        return False

    def collision(self, bbox1, bbox2):
        return not (bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or
                    bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3])

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
        # Reproducir sonido de game over
        self.sonido_game_over.play()
        
if __name__ == "__main__":
    root = Tk()
    root.title('Tiro al Capa')
    root.geometry('800x400')
    root.call('wm', 'iconphoto', root._w, PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src/imgs/capa2.png')))    
    app = Main(root)
    root.resizable(False, False)
    app.mainloop()