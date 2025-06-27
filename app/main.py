import json

from fastapi import FastAPI, HTTPException
from httpx import HTTPStatusError, RequestError
from app.schema.image_generator import GenerateRequest, GenerateResponse
from app.api.image_generator import generate_image_with_fallback

app = FastAPI(title="Text-to-Image Microservice", docs_url="/docs")


@app.post("/text-to-img", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    try:
        image_url = await generate_image_with_fallback(req.text)
        return GenerateResponse(url=image_url)

    except HTTPStatusError as e:
        # Forward the status code from OpenAI (e.g. 400, 403)
        raise HTTPException(
            status_code=e.response.status_code,
            detail=json.loads(e.response.text)
        )

    except RequestError as e:
        # Network error, retry exhausted or timeout
        raise HTTPException(
            status_code=503,
            detail="Image generation service unavailable (network error)"
        )

    except Exception as e:
        # Unexpected errors
        raise HTTPException(status_code=500, detail="Internal server error")
