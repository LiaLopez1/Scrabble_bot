import tkinter as tk
from tkinter import scrolledtext
import string
import unicodedata
import nltk
from nltk.corpus import wordnet as wn
from googletrans import Translator

nltk.download('wordnet', quiet=True)

translator = Translator()

def procesar_palabra(palabra):
    palabra_sin_puntuacion = ''.join(c for c in palabra if c not in string.punctuation)
    palabra_minuscula = palabra_sin_puntuacion.lower()
    palabra_normalizada = ''.join(c for c in unicodedata.normalize('NFD', palabra_minuscula) if unicodedata.category(c) != 'Mn')
    letras_tokenizadas = [letra for letra in palabra_normalizada if letra.isalpha()]
    return letras_tokenizadas, palabra_normalizada

def verificar_y_traducir_palabra(palabra):
    palabra_ingles = translator.translate(palabra, src='es', dest='en').text
    synsets = wn.synsets(palabra_ingles)
    if synsets:
        definicion_ingles = synsets[0].definition()
        definicion_espanol = translator.translate(definicion_ingles, src='en', dest='es').text
        return definicion_espanol, True
    else:
        return "No se encontró un significado para esta palabra.", False

def vectorizar_ascii(letras):
    codigos_ascii = [ord(letra) for letra in letras]
    return codigos_ascii

def analizar_palabra():
    palabra_usuario = entry.get()
    if not palabra_usuario.strip():
        output_text.config(state='normal')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Por favor, introduce una palabra válida.\n")
        output_text.config(state='disabled')
        return
    
    letras_tokenizadas, palabra_normalizada = procesar_palabra(palabra_usuario)
    significado, es_valida = verificar_y_traducir_palabra(palabra_normalizada)
    
    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    if es_valida:
        codigos_ascii = vectorizar_ascii(letras_tokenizadas)
        output_text.insert(tk.END, f"Palabra Válida: Sí\nSignificado: {significado}\n")
        output_text.insert(tk.END, f"Letras Tokenizadas: {', '.join(letras_tokenizadas)}\n")
        output_text.insert(tk.END, f"Códigos ASCII: {codigos_ascii}\n")
    else:
        output_text.insert(tk.END, f"Palabra Válida: No\n{significado}\n")
    output_text.config(state='disabled')

# GUI setup
root = tk.Tk()
root.title("Analizador de Palabras")

entry_label = tk.Label(root, text="Introduce una palabra:")
entry_label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

analyze_button = tk.Button(root, text="Analizar", command=analizar_palabra)
analyze_button.pack()

output_text = scrolledtext.ScrolledText(root, width=60, height=10, state='disabled')
output_text.pack()

root.mainloop()
