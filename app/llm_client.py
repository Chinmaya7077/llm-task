import os
import httpx

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_llm(scraped_text: str, commodity_name: str):
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # optional but recommended by OpenRouter
        "HTTP-Referer": "http://localhost",
        "X-Title": "Commodity Extraction API"
    }

    system_prompt = """
    You are a commodity pricing extraction agent.

    You MUST extract numeric values if present.
    The data exists in tabular form.

    Rules:
    1. Extract ONLY the requested commodity.
    2. The webpage contains pricing tables.
    3. If a value is shown in the text, extract it.
    4. If a value is missing, use null.
    5. Return ONLY a JSON array.
    6. Do NOT say "Not Available" unless explicitly written.
    """

    user_prompt = f"""
    Commodity: {commodity_name}

    The following text contains pricing table rows.

    Each row corresponds to a delivery period.

    Extract rows with fields:
    delivery_period (e.g. "Dec 25", "Jan 26"),
    cash_price (number),
    futures_change (number),
    futures_price (number),
    basis (number),
    basis_month (string),
    status (string if present, else "Valid").

    Text:
    {scraped_text}
    """


    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0
    }

    response = httpx.post(
        OPENROUTER_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
