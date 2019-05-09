FROM python:3.7-alpine

WORKDIR /app

COPY ./requirements.txt /app/.

RUN pip install -U pip && pip install -r requirements.txt

COPY ./post_to_slack.py /app/.

ENTRYPOINT ["python", "post_to_slack.py"]
