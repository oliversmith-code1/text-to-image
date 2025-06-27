import httpx
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError, retry_if_exception_type
from app.config import OPENAI_API_KEY, OPENAI_API_URL, DEFAULT_FALLBACK_IMAGE

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=3),
       retry=retry_if_exception_type(httpx.RequestError))
async def generate_image_from_openai(prompt: str) -> str:
    payload = {
        "model": "gpt-image-1",
        "prompt": prompt
    }
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(OPENAI_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["data"][0]["url"]


async def generate_image_with_fallback(prompt: str) -> str:
    try:
        return await generate_image_from_openai(prompt)

    except RetryError:
        # Retry failed — return fallback image
        return DEFAULT_FALLBACK_IMAGE

    except httpx.HTTPStatusError as e:
        # Let FastAPI handle this with accurate status in endpoint
        raise e

    except Exception as e:
        print(f"error: {e}")
        raise Exception("internal issue")
