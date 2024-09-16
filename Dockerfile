# # Temel imaj olarak Apache Airflow kullanın
# FROM apache/airflow:2.10.1

# # Airflow kullanıcısına geçiş yapın
# USER airflow

# # Python için gerekli paketleri yükleyin
# RUN pip install --no-cache-dir beautifulsoup4 lxml

# # Airflow DAG dosyalarınızı kopyalayın
# COPY ./dags /opt/airflow/dags


# Use Apache Airflow as the base image
FROM apache/airflow:2.10.1

# Switch to the airflow user
USER airflow

# Install additional Python packages
RUN pip install --no-cache-dir beautifulsoup4 lxml

# Copy your DAG files to the Airflow container
COPY ./dags /opt/airflow/dags

# Copy your utils directory (parallel to dags) to the container
COPY ./utils /opt/airflow/utils

# Set the PYTHONPATH environment variable to include the utils directory
ENV PYTHONPATH="/opt/airflow/utils:${PYTHONPATH}"
