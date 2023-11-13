FROM python:3.9.12
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY requirements.txt /app
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    python3-dev \
    python3.9-dev \
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
	pkg-config \
    libreoffice \
    # snapd \
    && apt-get clean
# RUN systemctl start snapd.service
# RUN snap install core 
# RUN snap refresh core
# RUN snap install --classic certbot
# RUN ln -s /snap/bin/certbot /usr/bin/certbot
# RUN certbot --nginx     

RUN pip install -r requirements.txt
COPY . .
VOLUME ["/media"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:20001"]