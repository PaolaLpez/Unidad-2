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

# Definir el pin donde está conectado el sensor de llama (DO) - por ejemplo GPIO17
llama_pin = Pin(17, Pin.IN, Pin.PULL_UP)  # Configurar como entrada con resistencia pull-up
lla_in = Pin(34, Pin.IN, Pin.PULL_UP)
# Función principal para leer el estado del sensor de llama y comunicarte con el servidor
def main():
    while True:
        try:
            # Leer el estado del sensor de llama (0 = no llama, 1 = llama detectada)
            estado_llama = llama_pin.value()
            estado_llamaA = lla_in.value()
            print ("Estado:", estado_llamaA)

            # Verificar si se detectó llama o no
            if estado_llama == 0:  # Si el valor es 0, significa que hay llama
                print("¡Llama detectada!")
                # Enviar el estado del sensor de llama al servidor Flask
                url = f"{raspberry_pi_ip}?estado=1"  # Enviar "1" cuando hay llama
            else:  # Si el valor es 1, significa que no hay llama
                print("No hay llama")
                # Enviar el estado del sensor de llama al servidor Flask
                url = f"{raspberry_pi_ip}?estado=0"  # Enviar "0" cuando no hay llama

            # Intentar realizar la solicitud GET al servidor
            try:
                response = urequests.get(url)
                print("Respuesta del servidor:", response.text)
            except Exception as e:
                print(f"Error al conectar con el servidor: {e}")

        except Exception as e:
            print(f"Error al leer el sensor: {e}")

        time.sleep(1)  # Retraso entre intentos

# Ejecutar el programa
main()
