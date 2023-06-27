FROM python:3

WORKDIR /app

COPY requirements.txt ./

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "--debug", "run", "--host=0.0.0.0"]
