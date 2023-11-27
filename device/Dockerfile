#Dockerfile

#Docker Python Image
FROM python:3.9.18-slim-bullseye

ENV PYTHONUNBUFFERED=TRUE


# Add python files
ADD ./*.py .
ADD ./requirements.txt .

RUN pip install -r ./requirements.txt

CMD python ./main.py
