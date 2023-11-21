import subprocess
import time
from ast import main
from http import client
import os
from influxdb import InfluxDBClient

def wait_for_influxdb():
    while True:
        try:
            subprocess.check_output(['influx', '-execute', 'show databases'])
            print("InfluxDB está disponible.")
            break
        except subprocess.CalledProcessError:
            print("InfluxDB no está disponible todavía, esperando...")
            time.sleep(5)

def create_user():
    subprocess.check_output(['influx', '-execute', 'CREATE USER "nuevo_usuario" WITH PASSWORD \'nueva_contraseña\' WITH ALL PRIVILEGES'])
    print("Usuario creado exitosamente.")

def create_db(client):
  # Crear la base de datos 'logs' si no existe
  client.create_database(database)

  # Cambiar a la base de datos 'logs'
  client.switch_database(database)

  # Definir la configuración de la tabla 'clean'
  clean_table_config = {
      "measurement": "clean",
      "fields": {
          "value": "float"
      },
      "time": True,
  }

  # Crear la tabla 'clean' si no existe
  client.create_retention_policy("clean_policy", "INF", 1, database, default=True)
  client.create_continuous_query("clean_cq", f"SELECT * INTO clean FROM raw", database)
  client.write_points([], 'clean', clean_table_config)

  # Definir la configuración de la tabla 'raw'
  raw_table_config = {
      "measurement": "raw",
      "fields": {
          "value": "float"
      },
      "time": True,
  }

  # Crear la tabla 'raw' si no existe
  client.write_points([], 'raw', raw_table_config)

  print("Base de datos, tabla 'clean' y tabla 'raw' creadas con éxito.")

if __name__ == main:
  wait_for_influxdb()
  create_user()
      # Obtener valores de las variables de entorno
  host = os.getenv("INFLUXDB_HOST", "influx")
  port = int(os.getenv("INFLUXDB_PORT", 8086))
  user = os.getenv("INFLUXDB_USER", "admin")
  password = os.getenv("INFLUXDB_PASSWORD", "admin")
  database = os.getenv("INFLUXDB_DB", "logs")

  # Crear conexión al cliente de InfluxDB
  client = InfluxDBClient(host, port, user, password, database)
  create_db(client)
    