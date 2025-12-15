from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone

from app.schemas import CommodityRequest, CommodityResponse
from app.scraper import scrape_visible_text
from app.llm_client import call_llm
from app.extractor import parse_llm_response

app = FastAPI(title="Commodity Scraper API")


@app.post("/extract", response_model=CommodityResponse)
def extract_commodity(payload: CommodityRequest):

    try:
        scraped_text = scrape_visible_text(payload.web_url)

        llm_output = call_llm(
            scraped_text,
            payload.commodity_name
        )

        data = parse_llm_response(llm_output)

        return {
            "status": "success",
            "request_url": payload.web_url,
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
