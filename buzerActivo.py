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

# Definir el pin donde está conectado el sensor KY-003
SENSOR_PIN = 17  # Cambia este número según tu conexión
sensor = Pin(SENSOR_PIN, Pin.IN)

# Definir el pin para el buzzer (Asegúrate de que esté conectado al pin correcto, por ejemplo, GPIO2)
buzzer_pin = Pin(2, Pin.OUT)  # Conecta el buzzer al pin GPIO 2

# Función para encender el buzzer
def buzzer_on():
    buzzer_pin.on()  # Enciende el buzzer (HIGH, 3.3V)
    print("El buzzer está sonando.")

# Función para apagar el buzzer
def buzzer_off():
    buzzer_pin.off()  # Apaga el buzzer (LOW, 0V)
    print("El buzzer está apagado.")

# Función principal para leer el sensor y comunicarte con el servidor
def main():
    while True:
        try:
            # Leer el estado del sensor (0 o 1)
            estado = sensor.value()

            # Si el estado es 1, encender el buzzer
            if estado == 1:
                buzzer_on()  # Enciende el buzzer si el estado es 1
            else:
                buzzer_off()  # Apaga el buzzer si el estado es 0

            # Crear la URL con el parámetro 'estado'
            url = f"{raspberry_pi_ip}?estado={estado}"

            # Enviar la solicitud GET con el estado
            response = urequests.get(url)
            
            # Mostrar la respuesta del servidor
            print("Respuesta del servidor:", response.text)

        except Exception as e:
            print("Error de conexión:", e)

        time.sleep(1)  # Retraso entre intentos

# Ejecutar el programa
main()
