FROM mcr.microsoft.com/vscode/devcontainers/python:3.12

# Install system dependencies including TA-Lib
RUN apt-get -y update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    curl make gcc g++ libfreetype6-dev libpng-dev libopenblas-dev liblapack-dev gfortran libhdf5-dev git 
    # libta-lib0-dev
    # && apt-get clean

# Install TA-Lib C library
RUN wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib_0.6.4_amd64.deb \
    && dpkg -i ta-lib_0.6.4_amd64.deb

# Install Poetry
RUN pip install --upgrade --no-cache-dir pip \
    && pip install poetry

# Configure Poetry
RUN poetry config virtualenvs.create false

USER vscode
