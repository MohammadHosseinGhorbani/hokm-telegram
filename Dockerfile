FROM pypy:3

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "pypy3", "main.py" ]

