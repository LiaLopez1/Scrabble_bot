import tkinter as tk
import random

class ScrabbleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Scrabble-bot")
        self.master.geometry("900x1000")  # Dimensiones ajustadas para el atril y el contador de fichas

        self.bolsa_de_fichas = self.crear_bolsa_de_fichas()
        self.atril = [None] * 7
        self.ficha_seleccionada = None
        self.indice_ficha_seleccionada = None

        self.posicion_central = (7, 7)  # Posición de la casilla central
        self.tamano_celda = 40  # Ajusta esto según el tamaño exacto de las celdas
        self.etiquetas_especiales = {}

        self.crear_tablero()
        self.crear_atril()
        self.crear_contador_de_fichas()
        self.rellenar_atril()

    def crear_bolsa_de_fichas(self):
        fichas = {
            'a': 12, 'b': 2, 'c': 4, 'ch': 1, 'd': 5, 'e': 12, 'f': 1, 'g': 2, 'h': 2, 'i': 6,
            'j': 1, 'l': 4, 'll': 1, 'm': 2, 'n': 5, 'ñ': 1, 'o': 9, 'p': 2, 'q': 1, 'r': 5,
            'rr': 1, 's': 6, 't': 4, 'u': 5, 'v': 1, 'x': 1, 'y': 1, 'z': 1, 'comodín': 2
        }
        return [ficha for ficha, cantidad in fichas.items() for _ in range(cantidad)]

    def rellenar_atril(self):
        while len([ficha for ficha in self.atril if ficha is None]) > 0 and self.bolsa_de_fichas:
            for i in range(7):
                if not self.atril[i]:
                    self.atril[i] = self.bolsa_de_fichas.pop(random.randint(0, len(self.bolsa_de_fichas) - 1))
        self.actualizar_display_atril()

    def crear_tablero(self):
        self.marco_tablero = tk.Frame(self.master, bg='white')
        self.marco_tablero.pack(side=tk.TOP, pady=(20, 10), padx=(20, 20))

        self.botones_tablero = []
        colores = {'DL': "#b5f5f1", 'TL': "#29a6ff", 'DP': "#f2bc8a", 'TP': "#d4001c", 'normal': "#065238"}
        posiciones_especiales = {
            'DL': [(3,0), (11,0), (6,2), (8,2), (0,3), (7,3), (14,3), (2,6), (2,8), (6,6), (8,6), (12,6),
                   (3,7), (11,7), (3,14), (11,14), (6,12), (8,12), (0,11), (7,11), (14,11), (2,8), (6,8),
                   (8,8), (12,8)],
            'TL': [(5,1), (9,1), (1,5), (5,5), (9,5), (13,5), (5,13), (9,13), (1,9), (5,9), (9,9), (13,9)],
            'DP': [(1,1), (2,2), (3,3), (4,4), (13,1), (12,2), (11,3), (10,4), (1,13), (2,12), (3,11), (4,10),
                   (13,13), (12,12), (11,11), (10,10)],
            'TP': [(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)],
            'centro': [(7,7)]
        }
        etiquetas_especiales = {'DL': "DL", 'TL': "TL", 'DP': "DP", 'TP': "TP", 'centro': '★'}

        for i in range(15):
            fila = []
            for j in range(15):
                tipo_casilla = next((k for k, v in posiciones_especiales.items() if (i, j) in v), 'normal')
                color = colores['DP'] if tipo_casilla == 'centro' else colores[tipo_casilla]
                boton = tk.Button(self.marco_tablero, text='', font=('Arial', 12, 'bold'), bg=color, height=2, width=4)
                boton.grid(row=i, column=j)
                boton.bind("<Button-1>", lambda e, x=i, y=j: self.colocar_ficha(e, x, y))
                if tipo_casilla in etiquetas_especiales:
                    etiqueta = etiquetas_especiales[tipo_casilla]
                    color_texto = 'white' if tipo_casilla != 'centro' else 'black'
                    label = tk.Label(self.marco_tablero, text=etiqueta, font=('Arial', 12, 'bold'), bg=color, fg='white')
                    label.place(in_=boton, relx=0.5, rely=0.5, anchor="center")
                    self.etiquetas_especiales[(i, j)] = label
                fila.append(boton)
            self.botones_tablero.append(fila)

    def crear_atril(self):
        self.marco_atril = tk.Frame(self.master, bg='white')
        self.marco_atril.pack(side=tk.TOP, pady=(10, 20), padx=(20, 20))

        self.labels_atril = [tk.Label(self.marco_atril, text='', font=('Arial', 18), width=3, height=2, relief="groove") for _ in range(7)]
        for idx, label in enumerate(self.labels_atril):
            label.pack(side=tk.LEFT, padx=2)
            label.bind("<Button-1>", lambda e, idx=idx: self.seleccionar_ficha(e, idx))

    def actualizar_display_atril(self):
        for label, ficha in zip(self.labels_atril, self.atril):
            texto = '' if ficha == 'comodín' else ficha.upper()  # Mostrar en blanco para el comodín
            label.config(text=texto)

    def seleccionar_ficha(self, event, idx):
        if self.atril[idx]:
            self.ficha_seleccionada = self.atril[idx]
            self.indice_ficha_seleccionada = idx
            if self.ficha_seleccionada == 'comodín':
                self.manejar_comodin(event, idx)  # Manejo especial para el comodín

    def manejar_comodin(self, event, idx):
        """ Permite al jugador elegir qué letra representa el comodín. """
        top = tk.Toplevel(self.master)
        top.title("Elegir una letra para el comodín")
        mensaje = tk.Label(top, text="Ingrese una letra para representar este comodín:", font=("Arial", 14))
        mensaje.pack(pady=10)

        entrada = tk.Entry(top, font=("Arial", 14), width=4)
        entrada.pack(pady=10)

        def confirmar():
            letra = entrada.get().strip().lower()
            if len(letra) == 1 and letra.isalpha():
                self.atril[idx] = letra  # Establecer el comodín para representar la letra elegida
                self.actualizar_display_atril()
                top.destroy()

        boton_confirmar = tk.Button(top, text="Confirmar", command=confirmar)
        boton_confirmar.pack(pady=20)

    def colocar_ficha(self, event, x, y):
        if self.ficha_seleccionada and not self.botones_tablero[x][y]['text']:
            if (x, y) in self.etiquetas_especiales:
                self.etiquetas_especiales[(x, y)].destroy()  # Elimina la etiqueta especial
                del self.etiquetas_especiales[(x, y)]
            self.botones_tablero[x][y].config(text=self.ficha_seleccionada.upper(), fg='black', bg='#FFECC2')
            self.atril[self.indice_ficha_seleccionada] = None
            self.ficha_seleccionada = None
            self.rellenar_atril()

    def crear_contador_de_fichas(self):
        self.marco_contador_fichas = tk.Frame(self.master, bg='white')
        self.marco_contador_fichas.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 20))
        self.label_contador_fichas = tk.Label(self.marco_contador_fichas, text=f"Fichas restantes: {len(self.bolsa_de_fichas)}", font=('Arial', 18))
        self.label_contador_fichas.pack()

    def actualizar_contador_fichas(self):
        self.label_contador_fichas.config(text=f"Fichas restantes: {len(self.bolsa_de_fichas)}")

def main():
    root = tk.Tk()
    gui = ScrabbleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
