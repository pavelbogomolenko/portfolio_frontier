FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data/stock/overview

CMD [ "python", "./av_fetch_stock_overview.py" ]
