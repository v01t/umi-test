FROM python:3.7

COPY app /app

RUN pip install --upgrade pip && \
  pip install -r /app/requirements.txt

ENV ES_HOST ""
ENV ES_USER ""
ENV ES_PWD ""
ENV ES_INDEX ""
ENV GITHUB_TOKEN ""
ENV GITHUB_REPO RockstarLang/rockstar

ENTRYPOINT ["python"]
WORKDIR /app
CMD ["app.py"]
