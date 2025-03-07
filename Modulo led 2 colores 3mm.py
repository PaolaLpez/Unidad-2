import network
import urequests
import time
from machine import Pin

# Configuración de la red Wi-Fi
wifi_ssid = 'VALERIA'  # Tu SSID de Wi-Fi
wifi_password = '@Valeria-3211@*'  # Tu contraseña de Wi-Fi

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_password)

# Espera a que se conecte
while not wifi.isconnected():
    print("Conectando...")
    time.sleep(1)

print("Conectado a Wi-Fi")
print("Dirección IP:", wifi.ifconfig()[0])  # Mostrar la dirección IP

# Dirección IP del servidor Flask en la Raspberry Pi
raspberry_pi_ip = 'http://192.168.137.159:5000/sensor'  # Asegúrate de que sea la IP correcta

# Definir el pin donde está conectado el módulo de 2 colores
COLOR_PIN = 21  # Usamos GPIO21, ajústalo si es necesario
color_pin = Pin(COLOR_PIN, Pin.OUT)

# Función para cambiar el color
def cambiar_color(estado):
    if estado == 1:
        color_pin.value(1)  # Activa el color (enciende la señal)
        print("Color activado")
    else:
        color_pin.value(0)  # Desactiva el color (apaga la señal)
        print("Color desactivado")

# Función principal para leer el sensor y comunicarte con el servidor
def main():
    while True:
        try:
            # Realizar solicitud GET al servidor Flask en la Raspberry Pi
            response = urequests.get(raspberry_pi_ip)
            
            # Verificar la respuesta
            if response.status_code == 200:
                # Aquí asumimos que el servidor responde con el estado del sensor (0 o 1)
                estado = int(response.text)  # Asumiendo que el servidor devuelve 0 o 1

                # Cambiar el color en función del estado recibido
                cambiar_color(estado)
                
                print("Estado recibido:", estado)
            else:
                print("Error en la respuesta del servidor:", response.status_code)

        except Exception as e:
            print("Error de conexión:", e)

        time.sleep(1)  # Retraso entre intentos

# Ejecutar el programa
main()