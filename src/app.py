import logging

import runpod
from llama_cpp import Llama

logger = logging.getLogger()
logger.setLevel(logging.INFO)

MODEL_PATH = "your/path/to/llama-cpp/model" # I used llama-cpp 3 and 3.1 with this kind of set-up, you are free to experiment it further.


def generate_data(model_path, text, ctx, llm_kwargs={}, chat_completion_kwargs={}):
    try:
        llm = Llama(
            model_path=model_path,  # Download the model file first
            n_ctx=ctx,  # The max sequence length to use - note that longer sequence lengths require much more resources
            n_threads=8,  # The number of CPU threads to use, tailor to your system and the resulting performance
            n_gpu_layers=-1,  # The number of layers to offload to GPU, if available. -1 for offloading all layers.
            **llm_kwargs  # Pass keyword arguments specific to Llama
        )
        response = llm.create_chat_completion(
            messages=text,
            **chat_completion_kwargs  # Pass keyword arguments specific to create_chat_completion
        )
        return response['choices'][0]['message']['content']
    except FileNotFoundError as e:
        logger.error(f"Model file not found: {e}")
        return None
    except Exception as e:
        logger.error(f"Error generating data: {e}")
        return None


def handler(event):
    try:
        inputs = event.get('input', {})
        text = inputs.get('text', '')
        if not text:
            raise ValueError("Input 'text' is missing or empty")
        ctx = int(inputs.get('ctx', 32768))

        llm_kwargs = inputs.get('llm_kwargs', {})
        chat_completion_kwargs = inputs.get('chat_completion_kwargs', {})

        output = generate_data(
            model_path=MODEL_PATH,
            text=text,
            ctx=ctx,
            llm_kwargs=llm_kwargs,
            chat_completion_kwargs=chat_completion_kwargs
        )
        return {"output": output}
    except ValueError as ve:
        logger.error(f"Invalid input value: {ve}")
        return {"error": str(ve)}
    except Exception as e:
        logger.error(f"Error handling event: {e}")
        return {"error": str(e)}


runpod.serverless.start({
    "handler": handler
})
