import machine
import time
import network
import socket

# Configuración del receptor IR
IR_PIN = 17  # Pin donde está conectado el receptor IR
ir_receiver = machine.Pin(IR_PIN, machine.Pin.IN)

# Configuración de la red WiFi
WIFI_SSID = 'VALERIA'
WIFI_PASSWORD = '@Valeria-3211@*'

# Dirección IP de la Raspberry Pi Zero
PI_IP = '192.168.137.159'  # Cambia esto con la IP de tu Raspberry Pi
PI_PORT = 5000  # Puerto en el que escuchará el servidor en la Raspberry Pi

# Función para conectar el ESP32 a WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    timeout = 10  # Intentos máximos para conectar
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print('✅ Conectado a WiFi:', wlan.ifconfig())
    else:
        print('❌ Error: No se pudo conectar a WiFi')
        machine.reset()  # Reiniciar el ESP32 si no se conecta

# Conectar al WiFi
connect_wifi()

# Función para recibir señales del receptor IR
def recibir_senal():
    tiempo_inicial = time.ticks_us()  # Obtener el tiempo inicial en microsegundos
    
    # Esperar hasta que la señal cambie de 0 a 1
    while ir_receiver.value() == 0:  # Esperar el pulso de inicio (0 -> 1)
        pass
    
    # Esperar hasta que el pulso termine (1 -> 0)
    while ir_receiver.value() == 1:  # Medir duración del pulso
        pass
    
    duracion = time.ticks_diff(time.ticks_us(), tiempo_inicial)  # Duración del pulso
    return duracion

# Función para conectar el ESP32 al servidor TCP (Raspberry Pi)
def conectar_socket():
    addr = socket.getaddrinfo(PI_IP, PI_PORT)[0][-1]
    s = socket.socket()
    s.connect(addr)
    return s

# Bucle principal
try:
    socket_cliente = conectar_socket()
    while True:
        # Leer la señal IR
        if ir_receiver.value() == 0:  # Si se recibe una señal (inicio de un pulso)
            duracion = recibir_senal()  # Medir duración del pulso
            mensaje = f"Señal IR recibida: {duracion} us"
            print(mensaje)

            # Enviar el mensaje al servidor (Raspberry Pi)
            socket_cliente.send(mensaje.encode())

            time.sleep(0.2)  # Pausa para evitar lecturas repetidas

except KeyboardInterrupt:
    print("Programa detenido por el usuario")
    socket_cliente.close()
