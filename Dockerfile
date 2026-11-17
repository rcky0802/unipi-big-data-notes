# Base image: TeX Live completo con latexmk e tutti i font
FROM texlive/texlive:latest

LABEL maintainer="University Notes Project"
LABEL description="All-in-one environment with TeX Live, Python 3, Antigravity CLI and data science dependencies for compiling university notes."

# Imposta variabili ambiente non interattive
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Installa Python 3, pip, latexmk, git, ffmpeg, curl e utility di sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    latexmk \
    git \
    bash \
    procps \
    ffmpeg \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Installa Google Antigravity CLI (agy)
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash

# Aggiunge il binario di agy al PATH di sistema
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /workspace

# Copia configurazione globale latexmk (reindirizzamento artefatti in build/)
COPY .latexmkrc /etc/LatexMk

# Copia i requisiti Python e installa le dipendenze scientifiche
COPY Data-Mining/notebooks/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt

# Entrypoint default: shell interattiva bash
CMD ["/bin/bash"]
