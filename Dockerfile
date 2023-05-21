FROM python:3.11-bullseye

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install --with-deps chromium

COPY app.py /

EXPOSE 5000

# Run the Flask application and make it listen on any interface
CMD ["flask", "run", "--host=0.0.0.0"]
