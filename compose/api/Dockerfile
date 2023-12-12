FROM python:3.10

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1


RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/9995b721327eac7a88f0dce314ea074d5169634f/wait-for-it.sh > /wait-for-it.sh
ADD compose/api/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh && \
    chmod a+x /wait-for-it.sh

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD Pipfile /Pipfile
ADD Pipfile.lock /Pipfile.lock

ENV PIPENV_VERBOSITY=-1
RUN pip install pipenv
RUN pipenv sync --dev

ADD . /app/api/

WORKDIR /app/api

ENTRYPOINT ["/entrypoint.sh"]