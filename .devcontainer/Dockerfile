FROM mcr.microsoft.com/vscode/devcontainers/python:3.12

# Install system dependencies including TA-Lib
RUN apt-get -y update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    curl make gcc g++ libfreetype6-dev libpng-dev libopenblas-dev liblapack-dev gfortran libhdf5-dev git \
    libta-lib0-dev
    # && apt-get clean

# Install Poetry
RUN pip install --upgrade --no-cache-dir pip \
    && pip install poetry

# Configure Poetry
RUN poetry config virtualenvs.create false

USER vscode

# Install TA-Lib Python wrapper
RUN pip install --user TA-Lib
