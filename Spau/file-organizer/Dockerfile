FROM python:3.11-slim
LABEL maintainer="it-malago86"
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# Copia solo i file necessari
COPY organizer.py config.json requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "organizer.py"]
CMD ["--help"]
