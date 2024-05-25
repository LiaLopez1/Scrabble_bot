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
        self.master.geometry("1200x1000")

        self.bolsa_de_fichas = self.crear_bolsa_de_fichas()
        self.atril = [None] * 7
        self.atril_ia = [None] * 7
        self.ficha_seleccionada = None
        self.indice_ficha_seleccionada = None
        self.fichas_colocadas = []

        self.posicion_central = (7, 7)
        self.tamano_celda = 40
        self.etiquetas_especiales = {}
        self.colores_originales = {}

        self.translator = Translator()

        self.puntos_por_letra = self.crear_diccionario_puntos()

        self.crear_tablero()
        self.crear_atril()
        self.crear_contador_de_fichas()
        self.crear_area_significado()
        self.crear_botones()
        self.rellenar_atril()
        self.rellenar_atril_ia()

    def crear_bolsa_de_fichas(self):
        fichas = {
            'a': 12, 'b': 2, 'c': 4, 'ch': 1, 'd': 5, 'e': 12, 'f': 1, 'g': 2, 'h': 2, 'i': 6,
            'j': 1, 'l': 4, 'll': 1, 'm': 2, 'n': 5, 'ñ': 1, 'o': 9, 'p': 2, 'q': 1, 'r': 5,
            'rr': 1, 's': 6, 't': 4, 'u': 5, 'v': 1, 'x': 1, 'y': 1, 'z': 1, 'comodín': 2
        }
        return [ficha for ficha, cantidad in fichas.items() for _ in range(cantidad)]
    
    def crear_diccionario_puntos(self):
        return {
            'a': 1, 'b': 3, 'c': 3, 'ch': 5, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
            'j': 8, 'l': 1, 'll': 8, 'm': 3, 'n': 1, 'ñ': 8, 'o': 1, 'p': 3, 'q': 5, 'r': 1,
            'rr': 8, 's': 1, 't': 1, 'u': 1, 'v': 4, 'x': 8, 'y': 4, 'z': 10, 'comodín': 0
        }

    def rellenar_atril(self):
        while len([ficha for ficha in self.atril if ficha is None]) > 0 and self.bolsa_de_fichas:
            for i in range(7):
                if not self.atril[i]:
                    self.atril[i] = self.bolsa_de_fichas.pop(random.randint(0, len(self.bolsa_de_fichas) - 1))
                    print(f"Atril jugador rellenado: {self.atril}")
                    print(f"Fichas restantes en la bolsa: {len(self.bolsa_de_fichas)}")
        self.actualizar_display_atril()
        self.actualizar_contador_fichas()
    
    def rellenar_atril_ia(self):
        while len([ficha for ficha in self.atril_ia if ficha is None]) > 0 and self.bolsa_de_fichas:
            for i in range(7):
                if not self.atril_ia[i]:
                    self.atril_ia[i] = self.bolsa_de_fichas.pop(random.randint(0, len(self.bolsa_de_fichas) - 1))
                    print(f"Atril IA rellenado: {self.atril_ia}")
                    print(f"Fichas restantes en la bolsa: {len(self.bolsa_de_fichas)}")
        self.actualizar_display_atril_ia()
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
                self.colores_originales[(i, j)] = color  
                boton = tk.Button(self.marco_tablero, text='', font=('Arial', 12, 'bold'), bg=color, height=2, width=4)
                boton.grid(row=i, column=j)
                boton.bind("<Button-1>", lambda e, x=i, y=j: self.colocar_ficha(e, x, y))
                if tipo_casilla in etiquetas_especiales:
                    etiqueta = etiquetas_especiales[tipo_casilla]
                    color_texto = 'white' if tipo_casilla != 'centro' else 'black'
                    label = tk.Label(self.marco_tablero, text=etiqueta, font=('Arial', 12, 'bold'), bg=color, fg=color_texto)
                    label.place(in_=boton, relx=0.5, rely=0.5, anchor="center")
                    self.etiquetas_especiales[(i, j)] = label
                fila.append(boton)
            self.botones_tablero.append(fila)

        self.marco_lateral = tk.Frame(self.marco_principal, bg='white')
        self.marco_lateral.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 20))

    def crear_atril(self):
        self.marco_atril = tk.Frame(self.master, bg='white')
        self.marco_atril.pack(side=tk.TOP, pady=(10, 5), padx=(20, 20))

        self.labels_atril = [self.crear_label_atril(self.marco_atril) for _ in range(7)]
        for idx, (label, puntaje) in enumerate(self.labels_atril):
            label.pack(side=tk.LEFT, padx=2)
            label.bind("<Button-1>", lambda e, idx=idx: self.seleccionar_ficha(e, idx))
            puntaje.pack(in_=label, anchor='se', padx=2, pady=2)

        # Crear el atril de la IA debajo del atril del usuario
        self.marco_atril_ia = tk.Frame(self.master, bg='white')
        self.marco_atril_ia.pack(side=tk.TOP, pady=(5, 20), padx=(20, 20))

        self.labels_atril_ia = [self.crear_label_atril(self.marco_atril_ia) for _ in range(7)]
        for idx, (label, puntaje) in enumerate(self.labels_atril_ia):
            label.pack(side=tk.LEFT, padx=2)
            puntaje.pack(in_=label, anchor='se', padx=2, pady=2)

    def crear_label_atril(self, marco):
        marco_label = tk.Frame(marco, width=50, height=50, bg='white', relief="groove", bd=2)
        letra = tk.Label(marco_label, text='', font=('Arial', 18), width=2, height=1, bg='white')
        puntaje = tk.Label(marco_label, text='', font=('Arial', 10), bg='white')
        letra.pack(side=tk.TOP, padx=(5, 15))
        return marco_label, puntaje

    def actualizar_display_atril(self):
        for (marco, puntaje), ficha in zip(self.labels_atril, self.atril):
            letra = marco.winfo_children()[0]
            if ficha is None:
                letra.config(text='')
                puntaje.config(text='')
            else:
                letra.config(text=ficha.upper())
                puntaje.config(text=(f'{self.puntos_por_letra[ficha]}'))

    def actualizar_display_atril_ia(self):
        for (marco, puntaje), ficha in zip(self.labels_atril_ia, self.atril_ia):
            letra = marco.winfo_children()[0]
            if ficha is None:
                letra.config(text='')
                puntaje.config(text='')
            else:
                letra.config(text=ficha.upper())
                puntaje.config(text=(f'{self.puntos_por_letra[ficha]}'))

    def seleccionar_ficha(self, event, idx):
        if self.atril[idx]:
            self.ficha_seleccionada = self.atril[idx]
            self.indice_ficha_seleccionada = idx
            if self.ficha_seleccionada == 'comodín':
                self.manejar_comodin(event, idx)

    def manejar_comodin(self, event, idx):
        top = tk.Toplevel(self.master)
        top.title("Elegir una letra para el comodín")
        mensaje = tk.Label(top, text="Ingrese una letra para representar este comodín:", font=("Arial", 14))
        mensaje.pack(pady=10)

        entrada = tk.Entry(top, font=("Arial", 14), width=4)
        entrada.pack(pady=10)

        def confirmar():
            letra = entrada.get().strip().lower()
            if len(letra) == 1 and letra.isalpha():
                self.atril[idx] = letra  
                self.actualizar_display_atril()
                top.destroy()

        boton_confirmar = tk.Button(top, text="Confirmar", command=confirmar)
        boton_confirmar.pack(pady=20)

    def colocar_ficha(self, event, x, y):
        if self.ficha_seleccionada and not self.botones_tablero[x][y]['text']:
            if (x, y) in self.etiquetas_especiales:
                self.etiquetas_especiales[(x, y)].destroy()
                del self.etiquetas_especiales[(x, y)]
            self.botones_tablero[x][y].config(text=self.ficha_seleccionada.upper(), fg='black', bg='#FFECC2')
            puntaje = self.puntos_por_letra[self.ficha_seleccionada]
            label_puntaje = tk.Label(self.master, text=str(puntaje), font=('Arial', 8), bg='#FFECC2', fg='black')
            label_puntaje.place(in_=self.botones_tablero[x][y], relx=0.99, rely=0.99, anchor="se")
            self.fichas_colocadas.append((x, y, self.ficha_seleccionada))
            self.atril[self.indice_ficha_seleccionada] = None
            self.ficha_seleccionada = None
            self.actualizar_display_atril()

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
        palabras = self.formar_palabras()
        puntos_totales = 0
        self.texto_significado.delete(1.0, tk.END)
        for palabra in palabras:
            significado = self.obtener_significado(palabra)
            puntos = self.calcular_puntos_palabra(palabra)
            puntos_totales += puntos
            if significado != "Palabra no válida.":
                self.texto_significado.insert(tk.END, f"Palabra: {palabra}\nSignificado: {significado}\nPuntos: {puntos}\n\n")
            else:
                self.texto_significado.insert(tk.END, f"La palabra '{palabra}' no es válida.\n\n")
                self.boton_colocar.config(state=tk.DISABLED)
                return
        self.boton_colocar.config(state=tk.NORMAL)

    def formar_palabras(self):
        palabras = []
        # Horizontal
        for x, y, _ in self.fichas_colocadas:
            palabra = self.formar_palabra_completa(x, y, horizontal=True)
            if palabra:
                palabras.append(palabra)
        # Vertical
        for x, y, _ in self.fichas_colocadas:
            palabra = self.formar_palabra_completa(x, y, horizontal=False)
            if palabra:
                palabras.append(palabra)
        return palabras

    def formar_palabra_completa(self, x, y, horizontal):
        palabra = []
        if horizontal:
            # Mover a la izquierda hasta encontrar el inicio de la palabra
            while y > 0 and self.botones_tablero[x][y-1]['text']:
                y -= 1
            # Formar palabra hacia la derecha
            while y < 15 and self.botones_tablero[x][y]['text']:
                palabra.append(self.botones_tablero[x][y]['text'].lower())
                y += 1
        else:
            # Mover hacia arriba hasta encontrar el inicio de la palabra
            while x > 0 and self.botones_tablero[x-1][y]['text']:
                x -= 1
            # Formar palabra hacia abajo
            while x < 15 and self.botones_tablero[x][y]['text']:
                palabra.append(self.botones_tablero[x][y]['text'].lower())
                x += 1
        return ''.join(palabra) if len(palabra) > 1 else None

    def calcular_puntos_palabra(self, palabra):
        return sum(self.puntos_por_letra.get(letra, 0) for letra in palabra)

    def obtener_significado(self, palabra):
        try:
            significados = wn.synsets(palabra, lang='spa')
            if significados:
                significado = significados[0].definition()
                traduccion = self.translator.translate(significado, src='en', dest='es')
                return traduccion.text
        except Exception as e:
            return f"Error obteniendo el significado: {e}"
        return "Palabra no válida."

    def colocar_palabra(self):
        self.fichas_colocadas.clear()
        self.boton_colocar.config(state=tk.DISABLED)
        self.rellenar_atril()  # Rellenar el atril del jugador después de colocar la palabra
        self.turno_ia()

    def devolver_todas_las_letras(self):
        for x, y, ficha in self.fichas_colocadas:
            self.botones_tablero[x][y].config(text='', bg=self.colores_originales[(x, y)])
            if (x, y) in self.etiquetas_especiales:
                self.etiquetas_especiales[(x, y)].place(in_=self.botones_tablero[x][y], relx=0.5, rely=0.5, anchor="center")
            for i in range(7):
                if self.atril[i] is None:
                    self.atril[i] = ficha
                    break
        self.fichas_colocadas.clear()
        self.actualizar_display_atril()
        self.boton_colocar.config(state=tk.DISABLED)

    def crear_contador_de_fichas(self):
        self.marco_contador_fichas = tk.Frame(self.master, bg='white')
        self.marco_contador_fichas.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 20))
        self.label_contador_fichas = tk.Label(self.marco_contador_fichas, text=f"Fichas restantes: {len(self.bolsa_de_fichas)}", font=('Arial', 18))
        self.label_contador_fichas.pack()

    def actualizar_contador_fichas(self):
        self.label_contador_fichas.config(text=f"Fichas restantes: {len(self.bolsa_de_fichas)}")

    def turno_ia(self):
        posibles_letras = self.encontrar_letras_existentes()
        for letra in posibles_letras:
            palabra_ia = self.generar_palabra_con_atril_ia(letra)
            if palabra_ia:
                posicion_valida = self.encontrar_posicion_valida(palabra_ia, letra)
                if posicion_valida:
                    self.colocar_palabra_ia(palabra_ia, posicion_valida)
                    self.texto_significado.insert(tk.END, f"\nIA colocó la palabra: {palabra_ia}\n")
                    self.rellenar_atril_ia()  # Asegurarse de rellenar el atril de la IA
                    return

    def generar_palabra_con_atril_ia(self, letra):
        x, y, letra_existente = letra
        posibles_palabras = self.obtener_posibles_palabras(self.atril_ia + [letra_existente.lower()])
        palabras_validas = [palabra for palabra in posibles_palabras if letra_existente.lower() in palabra]
        return random.choice(palabras_validas) if palabras_validas else None

    def obtener_posibles_palabras(self, letras):
        # Genera todas las combinaciones posibles de las letras en el atril de la IA
        from itertools import permutations
        palabras = set()
        for i in range(2, len(letras) + 1):
            for perm in permutations(letras, i):
                palabra = ''.join(perm)
                if self.es_palabra_valida(palabra):
                    palabras.add(palabra)
        return list(palabras)

    def es_palabra_valida(self, palabra):
        return bool(wn.synsets(palabra, lang='spa'))

    def encontrar_letras_existentes(self):
        letras_existentes = []
        for x in range(15):
            for y in range(15):
                letra = self.botones_tablero[x][y]['text']
                if letra:
                    letras_existentes.append((x, y, letra))
        return letras_existentes

    def encontrar_posicion_valida(self, palabra, letra):
        x, y, letra_existente = letra
        for i, l in enumerate(palabra):
            if l == letra_existente.lower():
                if self.es_posicion_valida(x, y - i, palabra, horizontal=True):
                    return (x, y - i, True)
                if self.es_posicion_valida(x - i, y, palabra, horizontal=False):
                    return (x - i, y, False)
        return None

    def es_posicion_valida(self, x, y, palabra, horizontal):
        if horizontal:
            if y < 0 or y + len(palabra) > 15:
                return False
            for i, letra in enumerate(palabra):
                if not (0 <= x < 15 and 0 <= y + i < 15):
                    return False
                if self.botones_tablero[x][y + i]['text'] not in ('', letra.upper()):
                    return False
        else:
            if x < 0 or x + len(palabra) > 15:
                return False
            for i, letra in enumerate(palabra):
                if not (0 <= x + i < 15 and 0 <= y < 15):
                    return False
                if self.botones_tablero[x + i][y]['text'] not in ('', letra.upper()):
                    return False
        return True

    def colocar_palabra_ia(self, palabra, posicion):
        x, y, horizontal = posicion
        letras_usadas = []
        if horizontal:
            for i, letra in enumerate(palabra):
                if self.botones_tablero[x][y + i]['text'] == '':
                    letras_usadas.append(letra)
                self.botones_tablero[x][y + i].config(text=letra.upper(), fg='black', bg='#FFECC2')
        else:
            for i, letra in enumerate(palabra):
                if self.botones_tablero[x + i][y]['text'] == '':
                    letras_usadas.append(letra)
                self.botones_tablero[x + i][y].config(text=letra.upper(), fg='black', bg='#FFECC2')

        # Remover las letras usadas del atril de la IA
        for letra in letras_usadas:
            self.atril_ia.remove(letra)
        self.actualizar_display_atril_ia()
        self.rellenar_atril_ia()  # Asegurarse de rellenar el atril de la IA después de colocar una palabra

def main():
    root = tk.Tk()
    gui = ScrabbleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
