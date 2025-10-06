FROM python:3.12

WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install --timeout=300 --retries=5 -r requirements.txt
RUN apt-get install -y libgl1 libglx-mesa0
RUN python downloadModels.py
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]