import pytest
import httpx
from tenacity import RetryError
from app.api.image_generator import generate_image_with_fallback, generate_image_from_openai
from unittest.mock import AsyncMock, patch, MagicMock
from app.config import DEFAULT_FALLBACK_IMAGE


@pytest.mark.asyncio
async def test_generate_image_success():
    expected_url = "http://fakeimage.com/img.png"

    # Prepare a mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    mock_response.json = MagicMock(return_value={"data": [{"url": expected_url}]})

    # Patch httpx.AsyncClient to return the mock response
    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.post.return_value = mock_response

        result = await generate_image_with_fallback("a happy dog")

    assert result == expected_url


@pytest.mark.asyncio
async def test_generate_image_with_fallback_httpx_error():
    with patch("app.api.image_generator.generate_image_from_openai", new_callable=AsyncMock) as mock_generate:
        mock_generate.side_effect = httpx.RequestError("connection fail", request=None)

        with pytest.raises(Exception, match="Failed to generate image."):
            await generate_image_with_fallback("http fail")


@pytest.mark.asyncio
async def test_generate_image_with_fallback_retry_error():
    with patch("app.api.image_generator.generate_image_from_openai", new_callable=AsyncMock) as mock_generate:
        mock_generate.side_effect = RetryError("Retries exhausted")

        result = await generate_image_with_fallback("fails repeatedly")
        assert result == DEFAULT_FALLBACK_IMAGE
