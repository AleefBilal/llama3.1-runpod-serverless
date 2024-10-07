# Use the official CUDA 12.2 base image
FROM nvidia/cuda:12.2.0-base-ubuntu20.04

# Install Python 3.11 from the official Python image
FROM python:3.11-slim


# Set environment variables for non-interactive installations
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages and CUDA toolkit
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    curl \
    gnupg2 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Add CUDA repository key
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub

# Add CUDA repository to apt sources list
RUN echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /" \
    > /etc/apt/sources.list.d/cuda.list

# Install CUDA Toolkit 12.2
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-toolkit-12-2 \
    && rm -rf /var/lib/apt/lists/*

# Set the CUDA environment variables
ENV PATH /usr/local/cuda-12.2/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/cuda-12.2/lib64:${LD_LIBRARY_PATH}

# Verify the CUDA installation
RUN nvcc --version

WORKDIR /

## Copy the requirements file before installing dependencies
COPY requirements.txt .

## Install Python dependencies
RUN pip3 install --upgrade pip && \
    pip3 install llama-cpp-python==0.2.90 \
    --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu122 && \
    pip3 install -r requirements.txt

COPY model model

COPY src ./

CMD [ "python3", "-u", "/app.py" ]