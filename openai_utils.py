import time, random, openai
from openai import (
    OpenAIError,
    RateLimitError,
    APIConnectionError,
)


def chat_completion_with_retry(messages: list[dict],
                                model: str = "gpt-4o-mini",
                                temperature: float = 0.4,
                                max_retries: int = 5,
                                base_delay: float = 2.0):
    """
    Envuelve openai.chat.completions.create con reintentos exponenciales.
    Retorna el texto (content) de la primera choice.
    """
    attempt = 0
    while True:
        try:
            resp = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return resp.choices[0].message.content.strip()

        except (RateLimitError,
                APIConnectionError,
                ) as e:

            attempt += 1
            if attempt > max_retries:
                raise RuntimeError(f"⛔ API falló tras {max_retries} intentos: {e}") from e

            # demora exponencial + jitter
            delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1)
            print(f"⚠️  {e.__class__.__name__}: intento {attempt}/{max_retries}; "
                  f"reintentando en {delay:0.1f}s…")
            time.sleep(delay)

        except OpenAIError as e:
            # otros errores no recuperables -> abortar
            raise RuntimeError(f"⛔ OpenAIError no recuperable: {e}") from e