# scripts/download_github_data.py

import os
import requests
from datetime import datetime, timedelta

# Configura rango de fechas
start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 5, 2)  # hasta pero sin incluir este día

# Crea carpeta si no existe
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Descarga los archivos hora por hora
def download_file(date, hour):
    url = f"https://data.gharchive.org/{date}-{hour}.json.gz"
    local_path = os.path.join(DATA_DIR, f"{date}-{hour}.json.gz")
    
    if os.path.exists(local_path):
        print(f"Ya existe: {local_path}")
        return

    print(f"Descargando {url}...")
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"✅ Guardado en {local_path}")
    else:
        print(f"❌ Falló descarga: {url} (Status: {response.status_code})")

# Itera por día y hora
current = start_date
while current < end_date:
    date_str = current.strftime("%Y-%m-%d")
    for hour in range(24):
        download_file(date_str, hour)
    current += timedelta(days=1)
