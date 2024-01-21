FROM python:3.11-slim-bookworm
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV LD_LIBRARY_PATH="/usr/lib/libreoffice/lib:$LD_LIBRARY_PATH"

WORKDIR /app
COPY requirements.txt /app
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    libgirepository1.0-dev \
    pkg-config \
    dos2unix \
    libpq-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    default-libmysqlclient-dev \
    build-essential \
    gcc \
    graphviz \
    libgraphviz-dev \
    libreoffice \
    && apt-get clean
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["gunicorn", "hildaApp.wsgi:application", "--bind", "0.0.0.0:8000"]