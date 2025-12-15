from pydantic import BaseModel
from typing import List, Optional

class CommodityRequest(BaseModel):
    web_url: str
    commodity_name: str


class CommodityData(BaseModel):
    delivery_period: Optional[str]   # 👈 FIX HERE
    cash_price: Optional[float]
    futures_change: Optional[float]
    futures_price: Optional[float]
    basis: Optional[float]
    basis_month: Optional[str]
    status: Optional[str]


class CommodityResponse(BaseModel):
    status: str
    request_url: str
    extracted_at: str
    data: List[CommodityData]
