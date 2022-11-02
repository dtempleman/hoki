FROM python:3.10-slim

ADD Pipfile /Pipfile
ADD Pipfile.lock /Pipfile.lock

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PIPENV_VERBOSITY=-1
RUN pip install pipenv
RUN pipenv sync --dev

ADD ./hoki /app/hoki
ADD ./scripts /app/scripts

WORKDIR /app
ENV PYTHONPATH=/app
