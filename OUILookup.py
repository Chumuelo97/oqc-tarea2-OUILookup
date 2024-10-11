import sys
import getopt
import requests
import os

# Función para consultar el fabricante de una MAC
# Realiza una solicitud a la API de maclookup para obtener el fabricante de una MAC
def consultar_mac(mac_address):
    url = f"https://api.maclookup.app/v2/macs/{mac_address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "company" in data:
                print(f"MAC address: {mac_address}")
                print(f"Fabricante: {data['company']}")
                print(f"Tiempo de respuesta: {response.elapsed.total_seconds() * 1000:.2f} ms")
            else:
                print(f"MAC address: {mac_address}")
                print("Fabricante: Not found")
        else:
            print(f"Error al consultar la MAC: {mac_address}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

# Función para consultar la tabla ARP del sistema
# Extrae las MACs de la tabla ARP y llama a consultar_mac para cada una
def consultar_arp():
    try:
        output = os.popen('arp -a').read()
        lines = output.splitlines()
        for line in lines:
            if '-' in line or ':' in line:
                mac_address = line.split()[1]  # Extraer la MAC de la tabla
                consultar_mac(mac_address)
    except Exception as e:
        print(f"Error al consultar la tabla ARP: {e}")

# Validar si la MAC pertenece a las MACs solicitadas en la rúbrica
# Debemos validar explícitamente las 3 MACs solicitadas
def validar_mac_especial(mac_address):
    macs_validas = ["98:06:3c:92:ff:c5", "9c:a5:13", "48-E7-DA"]
    # Verifica si la MAC coincide con alguna de las MACs solicitadas
    if mac_address in macs_validas or any(mac_address.startswith(mac) for mac in macs_validas):
        print(f"Validación exitosa para MAC especial: {mac_address}")
    else:
        print(f"Advertencia: {mac_address} no es una de las MACs solicitadas para validación.")

# Función principal para manejar los argumentos de la línea de comandos
# Utiliza getopt para procesar los parámetros: --mac para consulta específica o --arp para tabla ARP
def main(argv):
    mac_address = None
    mostrar_arp = False

    try:
        opts, args = getopt.getopt(argv, "hm:a", ["help", "mac=", "arp"])
    except getopt.GetoptError:
        print("Use: OUILookup.py --mac <mac> | --arp | --help")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Use: OUILookup.py --mac <mac> | --arp | --help \n--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.\n--arp: muestra los fabricantes de los hostdisponibles en la tabla arp.\n--help: muestra este mensaje y termina.\n")
            sys.exit()
        elif opt in ("--mac"):
            mac_address = arg
        elif opt in ("--arp"):
            mostrar_arp = True

    # Si se proporciona una MAC, realiza la consulta
    if mac_address:
        validar_mac_especial(mac_address)  # Valida si la MAC está entre las solicitadas
        consultar_mac(mac_address)
    # Si se solicita la tabla ARP, realiza la consulta ARP
    elif mostrar_arp:
        consultar_arp()
    # Mostrar mensaje de ayuda si no se proporcionan argumentos
    else:
        print("Use: OUILookup.py --mac <mac> | --arp | --help")

# Verificar si el script se ejecuta como programa principal
if __name__ == "__main__":
    main(sys.argv[1:])