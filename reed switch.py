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

# Definir el pin donde está conectado el Reed Switch (usamos un pin digital, como GPIO17)
reed_switch_pin = Pin(17, Pin.IN, Pin.PULL_UP)  # Usamos un pin de entrada con resistencia pull-up

# Función principal para leer el estado del Reed Switch y comunicarte con el servidor
def main():
    while True:
        try:
            # Leer el estado del Reed Switch (0 = cerrado, 1 = abierto)
            estado_reed = reed_switch_pin.value()

            # Enviar el estado del Reed Switch al servidor Flask
            url = f"{raspberry_pi_ip}?estado={estado_reed}"

            # Enviar la solicitud GET con el estado
            response = urequests.get(url)
            
            # Mostrar la respuesta del servidor
            print("Estado del Reed Switch:", estado_reed)
            print("Respuesta del servidor:", response.text)

        except Exception as e:
            print("Error de conexión:", e)

        time.sleep(1)  # Retraso entre intentos

# Ejecutar el programa
main()