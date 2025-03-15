import urequests
import utime
import network

# Configurar WiFi
ssid = "VALERIA"
password = "CREAME"

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
if not sta_if.isconnected():
    print("Conectando a WiFi...")
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        utime.sleep(1)
print("Conectado a WiFi")

# URL del servidor Flask en la Raspberry Pi
url = "http://192.168.137.159:5008"

while True:
    try:
        # Simulación de lectura del sensor
        valor = 25 + sensor_id  # Reemplazar con la lectura real del sensor

        # Enviar datos al servidor
        response = urequests.post(url, json={"valor": valor})
        print(f"Sensor 8 - Respuesta: ", response.text)
        response.close()
    except Exception as e:
        print(f"Error en sensor 8: ", e)

    utime.sleep(10)  # Enviar datos cada 10 segundos
