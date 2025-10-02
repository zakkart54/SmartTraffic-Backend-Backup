FROM python:3.12
WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip
RUN apt-get -y update
RUN apt-get install -y libgl1 and libglx-mesa0
RUN pip install --timeout=300 --retries=5 -r requirements.txt
RUN python downloadModels.py
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]