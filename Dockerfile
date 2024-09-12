# Utilise une image de base Airflow avec Python 3.12
FROM apache/airflow:latest-python3.12

# Copie le fichier requirements.txt dans le répertoire par défaut d'Airflow
COPY /requirements.txt /requirements.txt

# Installe les bibliothèques Python listées dans requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Optionnel : Si tu as des plugins ou d'autres fichiers, tu peux les copier
# COPY ./plugins /opt/airflow/plugins

# L'image officielle d'Airflow configure déjà l'entrypoint et d'autres paramètres
# Donc pas besoin de spécifier CMD ou ENTRYPOINT si tu utilises Docker Compose


# Set permissions for Airflow logs
RUN mkdir -p /opt/airflow/logs && \
    chown -R airflow: /opt/airflow/logs
