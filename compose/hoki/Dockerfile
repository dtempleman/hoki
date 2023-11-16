FROM python:3.10

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD Pipfile /Pipfile
ADD Pipfile.lock /Pipfile.lock

ENV PIPENV_VERBOSITY=-1
RUN pip install pipenv
RUN pipenv sync --dev

ADD . /app/hoki/

WORKDIR /app/hoki

ENV PYTHONPATH=/app/hoki
