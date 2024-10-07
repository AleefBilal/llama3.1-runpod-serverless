
# LLaMA 3.1 CPP on RunPod Serverless with Docker

This project hosts a LLaMA 3.1 CPP model on RunPod's serverless service using Docker. The model processes requests, handles inputs, and outputs responses. It uses Python 3.11, CUDA 12.2, and runs on Ubuntu 22.04.


## Features
- Dockerized environment
- Python 3.11
- CUDA 12.2
- Ubuntu 22.04
- LLaMA 3.1 8b CPP-based model for handling AI requests
- Serverless deployment using RunPod

## Docker Setup

### Building the Docker Image
To build the Docker image, run the following command:

```bash
sudo docker build -t <docker_name>:<docker_tag> .
```

### Running the Docker Container
To run the Docker container with GPU support, use the following command:

```bash
sudo docker run --rm -it --gpus all <docker_name>:<docker_tag>
```

Once the Docker is running, as it is a serverless Docker hosted on RunPod, it will process a predefined test input (`test_input.json`) and return a response.

## Main File: `app.py`
The core of the pipeline is implemented in `src/app.py`. It handles the model inference and input/output processing.

## Payload Format
The Docker processes a payload in the following format:

```json
{
    "input": {
        "llm_kwargs": {
            "n_batch": 2048,
            "max_tokens": 1000,
            "temperature": 0.8,
            "top_k": 40,
            "top_p": 0.9
        },
        "text": [
            {
                "role": "system",
                "content": "system_message here"
            },
            {
                "role": "user",
                "content": "user_query here"
            }
        ]
    }
}
```

### Key Parameters:
- **n_batch**: Batch size for processing (default: 2048)
- **max_tokens**: Maximum number of tokens to generate (default: 1000)
- **temperature**: Sampling temperature for randomness (default: 0.8)
- **top_k**: Top-k sampling for the model (default: 40)
- **top_p**: Nucleus sampling threshold (default: 0.9)


## Important Note
- Do not forget to update the path to your `llama-cpp` model in `src/app.py`
- you can check logs of your model loading to see if your model is utilizing cuda or not.
- If Nvidia GPU is available, docker is build successfully, but your llama model is still not utilizing GPU, most probably this issue would be with `llama-cpp` library, It is pretty unstable.
- In this case, experiment with different versions and stuff.
- Hope it gets fixed soon.