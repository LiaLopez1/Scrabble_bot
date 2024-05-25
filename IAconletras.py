import tkinter as tk
from tkinter import scrolledtext
import string
import unicodedata
import random
import nltk
from nltk.corpus import cess_esp, wordnet as wn
from googletrans import Translator
from itertools import permutations

# Descargar el corpus de palabras en español
nltk.download('cess_esp', quiet=True)
nltk.download('wordnet', quiet=True)

# Crear un conjunto de palabras válidas en español
palabras_validas = set(w.lower() for w in cess_esp.words() if w.isalpha())

translator = Translator()

def procesar_palabra(palabra):
    palabra_sin_puntuacion = ''.join(c for c in palabra if c not in string.punctuation)
    palabra_minuscula = palabra_sin_puntuacion.lower()
    palabra_normalizada = ''.join(c for c in unicodedata.normalize('NFD', palabra_minuscula) if unicodedata.category(c) != 'Mn')
    letras_tokenizadas = [letra for letra in palabra_normalizada if letra.isalpha()]
    return letras_tokenizadas, palabra_normalizada

def verificar_palabra(palabra):
    return palabra in palabras_validas

def obtener_significado(palabra):
    try:
        palabra_ingles = translator.translate(palabra, src='es', dest='en').text
        synsets = wn.synsets(palabra_ingles)
        if synsets:
            definicion_ingles = synsets[0].definition()
            definicion_espanol = translator.translate(definicion_ingles, src='en', dest='es').text
            return definicion_espanol
        else:
            return "No se encontró un significado para esta palabra."
    except Exception as e:
        return f"Error obteniendo el significado: {e}"

def generar_letras():
    letras = random.choices(string.ascii_lowercase, k=7)
    return letras

def analizar_palabra():
    palabra_usuario = entry.get()
    if not palabra_usuario.strip():
        output_text.config(state='normal')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Por favor, introduce una palabra válida.\n")
        output_text.config(state='disabled')
        return
    
    letras_tokenizadas, palabra_normalizada = procesar_palabra(palabra_usuario)
    if not all(letra in letras_disponibles for letra in letras_tokenizadas):
        output_text.config(state='normal')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "La palabra contiene letras no disponibles.\n")
        output_text.config(state='disabled')
        return

    es_valida = verificar_palabra(palabra_normalizada)
    
    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    if es_valida:
        significado = obtener_significado(palabra_normalizada)
        output_text.insert(tk.END, f"Palabra Válida: Sí\nSignificado: {significado}\n")
    else:
        output_text.insert(tk.END, f"Palabra Válida: No\n")
    output_text.config(state='disabled')

def actualizar_letras():
    global letras_disponibles
    letras_disponibles = generar_letras()
    letras_label.config(text=f"Letras disponibles: {', '.join(letras_disponibles)}")

def generar_palabra_ia(letras):
    palabras_validas_ia = []
    for i in range(1, len(letras) + 1):
        for perm in permutations(letras, i):
            palabra = ''.join(perm)
            _, palabra_normalizada = procesar_palabra(palabra)
            if verificar_palabra(palabra_normalizada):
                palabras_validas_ia.append(palabra_normalizada)
    if palabras_validas_ia:
        return max(palabras_validas_ia, key=len)
    else:
        return None

def jugar_ia():
    letras_ia = generar_letras()
    palabra_ia = generar_palabra_ia(letras_ia)
    output_text.config(state='normal')
    output_text.insert(tk.END, f"\nLetras de la IA: {', '.join(letras_ia)}\n")
    if palabra_ia:
        significado = obtener_significado(palabra_ia)
        output_text.insert(tk.END, f"Palabra de la IA: {palabra_ia}\nSignificado: {significado}\n")
    else:
        output_text.insert(tk.END, "La IA no pudo formar una palabra válida.\n")
    output_text.config(state='disabled')

# GUI setup
root = tk.Tk()
root.title("Generador de Palabras")

# Letras del jugador
letras_label = tk.Label(root, text="")
letras_label.pack()

update_button = tk.Button(root, text="Generar Letras", command=actualizar_letras)
update_button.pack()

entry_label = tk.Label(root, text="Introduce una palabra:")
entry_label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

analyze_button = tk.Button(root, text="Analizar", command=analizar_palabra)
analyze_button.pack()

output_text = scrolledtext.ScrolledText(root, width=60, height=10, state='disabled')
output_text.pack()

# Botón para que la IA juegue
ia_button = tk.Button(root, text="Jugar IA", command=jugar_ia)
ia_button.pack()

# Inicializa las letras disponibles para el jugador
actualizar_letras()

root.mainloop()
