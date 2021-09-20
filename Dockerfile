FROM node:14-buster AS builder

WORKDIR /frontend
COPY frontend .
RUN npm install 
RUN npm run build

#Stage 2
FROM python:3.9-buster
WORKDIR /flaskapp
COPY flaskapp .
RUN pip install -r requirements.txt
COPY --from=builder /frontend/build ./static

CMD ["python", "app.py"]

