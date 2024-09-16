# Use an Airflow base image with Python 3.12
FROM apache/airflow:latest-python3.12

# Copy the requirements.txt file into Airflow's default directory
COPY /requirements.txt /requirements.txt

# Install the Python libraries listed in requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Optional: If you have plugins or other files, you can copy them
# COPY ./plugins /opt/airflow/plugins

# Set permissions for Airflow logs
RUN mkdir -p /opt/airflow/logs && \
    chown -R airflow: /opt/airflow/logs
