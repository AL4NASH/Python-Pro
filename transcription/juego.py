import time
import random
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr

duration = 5  # segundos de grabación
sample_rate = 44100

puntos_rival = 0
puntos_jugador = 0
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

dificultad = input("Selecciona la dificultad (fácil, intermedio, difícil): ").strip().lower()
print("Has seleccionado la dificultad:" + dificultad + "¡Buena suerte!")
time.sleep(2)
print("--------------------------------------------------------------")

if dificultad in ["facil", "fácil"]:
    palabras = list(facil.keys())
elif dificultad == "intermedio":
    palabras = list(intermedio.keys())
elif dificultad in ["dificil", "difícil"]:
    palabras = list(dificil.keys())
else:
    print("Dificultad no válida.")
    exit()

random.shuffle(palabras)

for i in range(5):
    palabra = palabras[i]
    if dificultad in ["facil", "fácil"]:
        traduccion = facil[palabra]
        probabilidad_rival = random.randint(0, 2)
        if probabilidad_rival == 0:  # 33% de probabilidad de que el rival gane un punto
            puntos_rival += 1
    elif dificultad == "intermedio":
        traduccion = intermedio[palabra]
        probabilidad_rival = random.randint(0, 1)
        if probabilidad_rival == 0:  # 50% de probabilidad de que el rival gane un punto
            puntos_rival += 1
    elif dificultad in ["dificil", "difícil"]:
        traduccion = dificil[palabra]
        puntos_rival += 1

    print("Tu palabra es:", palabra)
    time.sleep(1)
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
        texto = recognizer.recognize_google(audio, language="en-US")
        print("Has dicho:", texto)

        if traduccion.lower() in texto.lower():
            print("¡Correcto! Has ganado un punto.")
            time.sleep(1)
            puntos_jugador += 1
            print("Puntos del jugador:", puntos_jugador)
            print("Puntos del rival:", puntos_rival)
            time.sleep(1)
        else:
            print("Incorrecto. La traducción correcta es:", traduccion)
            time.sleep(1)
            print("Puntos del jugador:", puntos_jugador)
            print("Puntos del rival:", puntos_rival)
            time.sleep(1)
    except sr.UnknownValueError:
        print("No pude entender lo que dijiste.")

    except sr.RequestError:
        print("Error al conectar con el servicio de reconocimiento.")
    print("--------------------------------------------------------------")

print("--------------------------------------------------------------")
print("El juego ha terminado.")
print("Y el ganador es...")
time.sleep(2)
if puntos_jugador > puntos_rival:
    print("¡Tu, quien has ganado con", puntos_jugador, "puntos!")
elif puntos_jugador < puntos_rival:
    print("El rival, que ha ganado con", puntos_rival, "puntos.")
else:
    print("¡Nadie! Ambos tienen", puntos_jugador, "puntos.")