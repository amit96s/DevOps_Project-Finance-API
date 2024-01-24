FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt .
RUN apk update && apk add --no-cache build-base  \
    && pip install --upgrade pip \
    && pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
