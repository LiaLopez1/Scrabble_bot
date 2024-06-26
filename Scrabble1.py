import tkinter as tk
import random
import nltk
from nltk.corpus import wordnet as wn
from googletrans import Translator

nltk.download('wordnet')
nltk.download('omw-1.4')

class ScrabbleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Scrabble-bot")
        self.master.geometry("1200x1000")  # Dimensiones ajustadas para el atril y el contador de fichas

        self.bolsa_de_fichas = self.crear_bolsa_de_fichas()
        self.atril = [None] * 7
        self.ficha_seleccionada = None
        self.indice_ficha_seleccionada = None
        self.fichas_colocadas = []

        self.posicion_central = (7, 7)  # Posición de la casilla central
        self.tamano_celda = 40  # Ajusta esto según el tamaño exacto de las celdas
        self.etiquetas_especiales = {}
        self.colores_originales = {}

        self.translator = Translator()  # Inicializar el traductor

        self.crear_tablero()
        self.crear_atril()
        self.crear_contador_de_fichas()
        self.crear_area_significado()
        self.crear_botones()
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
        self.actualizar_contador_fichas()

    def crear_tablero(self):
        self.marco_principal = tk.Frame(self.master, bg='white')
        self.marco_principal.pack(side=tk.TOP, pady=(20, 10), padx=(20, 20))

        self.marco_tablero = tk.Frame(self.marco_principal, bg='white')
        self.marco_tablero.pack(side=tk.LEFT, pady=(20, 10), padx=(20, 20))

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
                self.colores_originales[(i, j)] = color  # Guardar el color original
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

        self.marco_lateral = tk.Frame(self.marco_principal, bg='white')
        self.marco_lateral.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 20))

    def crear_atril(self):
        self.marco_atril = tk.Frame(self.master, bg='white')
        self.marco_atril.pack(side=tk.TOP, pady=(10, 20), padx=(20, 20))

        self.labels_atril = [tk.Label(self.marco_atril, text='', font=('Arial', 18), width=3, height=2, relief="groove") for _ in range(7)]
        for idx, label in enumerate(self.labels_atril):
            label.pack(side=tk.LEFT, padx=2)
            label.bind("<Button-1>", lambda e, idx=idx: self.seleccionar_ficha(e, idx))

    def actualizar_display_atril(self):
        for label, ficha in zip(self.labels_atril, self.atril):
            texto = '' if ficha is None else ficha.upper()  # Mostrar en blanco si la ficha es None
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
            self.fichas_colocadas.append((x, y, self.ficha_seleccionada))
            self.atril[self.indice_ficha_seleccionada] = None  # Eliminar la ficha del atril
            self.ficha_seleccionada = None
            self.actualizar_display_atril()  # Actualizar el display del atril

    def crear_area_significado(self):
        self.texto_significado = tk.Text(self.marco_lateral, height=10, width=50, wrap=tk.WORD)
        self.texto_significado.pack(side=tk.TOP, pady=(10, 20))

    def crear_botones(self):
        self.boton_verificar = tk.Button(self.marco_lateral, text="Verificar palabra", font=('Arial', 18), command=self.validar_palabra)
        self.boton_verificar.pack(side=tk.TOP, pady=20)
        
        self.boton_colocar = tk.Button(self.marco_lateral, text="Colocar palabra", font=('Arial', 18), state=tk.DISABLED, command=self.colocar_palabra)
        self.boton_colocar.pack(side=tk.TOP, pady=20)

        self.boton_devolver = tk.Button(self.marco_lateral, text="Devolver todas las letras", font=('Arial', 18), command=self.devolver_todas_las_letras)
        self.boton_devolver.pack(side=tk.TOP, pady=20)

    def validar_palabra(self):
        palabra = ''.join([self.botones_tablero[x][y]['text'] for x, y, _ in self.fichas_colocadas]).lower()
        significado = self.obtener_significado(palabra)
        self.texto_significado.delete(1.0, tk.END)
        if significado != "Palabra no válida." and "Error" not in significado:
            self.texto_significado.insert(tk.END, f"Palabra: {palabra}\nSignificado: {significado}")
            self.boton_colocar.config(state=tk.NORMAL)  # Habilitar el botón "Colocar palabra" si es válida
        else:
            self.texto_significado.insert(tk.END, f"La palabra '{palabra}' no es válida.")
            self.boton_colocar.config(state=tk.DISABLED)  # Mantener deshabilitado el botón "Colocar palabra"

    def obtener_significado(self, palabra):
        try:
            # Primero verificamos si la palabra existe en español
            significados = wn.synsets(palabra, lang='spa')
            if significados:
                # Obtenemos la definición en inglés
                significado = significados[0].definition()
                # Traducimos la definición al español
                traduccion = self.translator.translate(significado, src='en', dest='es')
                return traduccion.text
        except Exception as e:
            return f"Error obteniendo el significado: {e}"
        return "Palabra no válida."

    def colocar_palabra(self):
        # Colocar las fichas en el tablero permanentemente
        self.fichas_colocadas.clear()
        self.boton_colocar.config(state=tk.DISABLED)  # Deshabilitar el botón "Colocar palabra"

    def devolver_todas_las_letras(self):
        for x, y, ficha in self.fichas_colocadas:
            self.botones_tablero[x][y].config(text='', bg=self.colores_originales[(x, y)])  # Restaurar el color original
            if (x, y) in self.etiquetas_especiales:
                self.etiquetas_especiales[(x, y)].place(in_=self.botones_tablero[x][y], relx=0.5, rely=0.5, anchor="center")
            for i in range(7):
                if self.atril[i] is None:
                    self.atril[i] = ficha
                    break
        self.fichas_colocadas.clear()
        self.actualizar_display_atril()
        self.boton_colocar.config(state=tk.DISABLED)  # Deshabilitar el botón "Colocar palabra"

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
