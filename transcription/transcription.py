import time
import random
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from deep_translator import GoogleTranslator

duration = 5  # segundos de grabación
sample_rate = 44100

facil = {"Casa": "House", "Perro": "Dog", "Gato": "Cat", "Agua": "Water", "Sol": "Sun", "Libro": "Book", "Mano": "Hand", "Mesa": "Table", "Escuela": "School", "Amigo": "Friend"}
intermedio = {"Ventana": "Window", "Montaña": "Mountain", "Desayuno": "Breakfast", "Biblioteca": "Library", "Jardín": "Garden", "Cuchara": "Spoon", "Espejo": "Mirror", "Vecino": "Neighbor", "Oficina": "Office", "Zapatero": "Shoemaker"}
dificil = {"Murciélago": "Bat", "Ardilla": "Squirrel", "Rompecabezas": "Puzzle", "Desarrollador": "Developer", "Aterrizaje": "Landing", "Relámpago": "Lightning", "Herramienta": "Tool", "Enciclopedia": "Encyclopedia", "Investigación": "Research", "Conocimiento": "Knowledge"}

print("Hola, bienvenido al juego de reconocimiento de voz y traducción. Estás son las reglas:")
time.sleep(2)
print("Al inicio del juego, podrás elegir una de tres dificultades.")
time.sleep(2)
print("- A lo largo del juego, se te presentarán cinco palabras en español y tendrás que traducirlas y pronunciarlas en inglés.")
time.sleep(2)
print("- Para ganar, consigue una cantidad mayor de puntos que tu rival.")
time.sleep(2)

dificultad = input("Selecciona la dificultad (fácil, intermedio, difícil): ")
print("Has seleccionado la dificultad:" + dificultad + "¡Buena suerte!")
time.sleep(2)

for i in range(5):
    if dificultad == "fácil":
        palabra = random.choice(list(facil.keys()))
        traduccion = facil[palabra]
    elif dificultad == "intermedio":
        palabra = random.choice(list(intermedio.keys()))
        traduccion = intermedio[palabra]
    elif dificultad == "difícil":
        palabra = random.choice(list(dificil.keys()))
        traduccion = dificil[palabra]
    else:
        print("Dificultad no válida. Por favor, selecciona fácil, intermedio o difícil.")
        break
    print("Tu palabra es:", palabra)
    print("Habla ahora...")
    recording = sd.rec(
    int(duration * sample_rate), # el número de muestras a grabar
    samplerate=sample_rate,      # tasa de muestreo
    channels=1,                  # 1 significa grabación mono
    dtype="int16")               # tipo de datos para las muestras grabadas
    sd.wait()  # esperando a que termine la grabació
    wav.write("output.wav", sample_rate, recording)
    print("Grabación completa, ahora reconociendo...")
    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="es")
        print("Dijiste:", text)

        idioma = input("Selecciona el idioma al que quieres traducir (ej ingles: en, español: es)")
        result = GoogleTranslator(source='es', target=idioma).translate(text)
        print("Traducción:", result)
        
    except sr.UnknownValueError:             # - si Google no pudo entender el habla debido a ruido o silencio
        print("No se pudo reconocer el habla.")
    except sr.RequestError as e:             # - si no hay conexión a Internet o la API no está disponible
        print(f"Error del servicio: {e}")