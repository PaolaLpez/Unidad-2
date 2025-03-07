import network
import urequests
import time
from machine import Pin

# Conexión a Wi-Fi
wifi_ssid = 'VALERIA'  # Tu SSID de Wi-Fi
wifi_password = '@Valeria-3211@*'  # Tu contraseña de Wi-Fi

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_password)

# Espera a que se conecte
while not wifi.isconnected():
    print("Conectando...")
    time.sleep(1)

print("Conectado")

# Dirección IP de la Raspberry Pi
raspberry_pi_ip = 'http://192.168.137.159:5000/sensor'  # Asegúrate de que sea la IP correcta

# Definir el pin donde está conectado el sensor KY-003
SENSOR_PIN = 15  # Cambia este número según tu conexión
sensor = Pin(SENSOR_PIN, Pin.IN)

while True:
    try:
        # Leer el estado del sensor (0 o 1)
        estado = sensor.value()

        # Crear la URL con el parámetro 'estado'
        url = f"{raspberry_pi_ip}?estado={estado}"

        # Enviar la solicitud GET con el estado
        response = urequests.get(url)
        
        # Mostrar la respuesta del servidor
        print("Respuesta del servidor:", response.text)
        
    except Exception as e:
        print("Error de conexión:", e)

    time.sleep(1)  # Retraso entre intentos
