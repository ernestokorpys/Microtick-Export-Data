import json
import paramiko
import csv
import openpyxl
import socket

def conectar_microtik(ip, puerto, usuario, contraseña):
    try:
        # Crear una instancia del cliente SSH
        cliente_ssh = paramiko.SSHClient()
        # Agregar la clave del host automáticamente
        
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Conectarse al dispositivo
        cliente_ssh.connect(ip, port=puerto, username=usuario, password=contraseña, banner_timeout=120)
        
        # Ejecutar comando para obtener información de direcciones IP
        stdin, stdout, stderr = cliente_ssh.exec_command("ip address print")
        for line in stdout:
            print(line.strip('\n'))

        print("Conexión exitosa al dispositivo MikroTik.")
        
    except Exception as e:
        print("Error de conexión:", str(e))
    finally:
        # Cerrar la conexión SSH
        cliente_ssh.close()

# Cargar configuración desde el archivo JSON
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    host_port = config['host'].split(':')
    host = host_port[0]
    port = int(host_port[1]) if len(host_port) > 1 else 22
    username = config['username']
    password = config['password']
    export_filename = config['export_filename']
    rsc_file = f'{export_filename}.rsc'
    csv_file = config['csv_file']
    excel_file = config['excel_file']
    sheet_name = config['sheet_name']
except FileNotFoundError:
    print("Error: config.json file not found.")
except json.JSONDecodeError:
    print("Error parsing config.json.")

# Ejecución del proceso completo
# Llamar a la función para conectar y obtener información
print(host, int(port), username, password)
conectar_microtik(host, int(port), username, password)
