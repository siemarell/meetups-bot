FROM python

COPY . /app

RUN cd app && pip install -r requirements.txt

CMD cd app && python main.py