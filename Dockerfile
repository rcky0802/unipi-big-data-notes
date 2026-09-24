# Base image: TeX Live completo con latexmk e tutti i font
FROM texlive/texlive:latest

LABEL maintainer="University Notes Project"
LABEL description="All-in-one environment with TeX Live, Python 3 and data science dependencies for compiling university notes."

# Imposta variabili ambiente non interattive
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Installa Python 3, pip, latexmk, git e utility di sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    latexmk \
    git \
    bash \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copia i requisiti Python e installa le dipendenze scientifiche
COPY Data-Mining/playground/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Entrypoint default: shell interattiva bash
CMD ["/bin/bash"]
