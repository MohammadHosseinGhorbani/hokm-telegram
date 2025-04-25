FROM python:3

WORKDIR /code

COPY . .

RUN touch groups.db
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py" ]

