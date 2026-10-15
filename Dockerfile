FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    redis-server \
    mariadb-server \
    mariadb-client \
    libmariadb-dev \
    pkg-config \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g yarn

WORKDIR /home/naveen/frappe-bench

# Copy bench files & snapshot
COPY . /home/naveen/frappe-bench

# Setup venv & bench requirements
RUN python3 -m venv env && \
    ./env/bin/pip install --upgrade pip && \
    ./env/bin/pip install frappe-bench

COPY render-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 10000

CMD ["/entrypoint.sh"]
