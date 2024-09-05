import random

from fastapi import APIRouter, Depends
from app.schemas import QuoteRequest, QuoteResponse
from app.samples import EXCHANGE_OPTIONS

quote_router = APIRouter(tags=["Quotes"])


@quote_router.post("/quote")
async def new_service_quote(request: QuoteRequest) -> QuoteResponse:
    """
    Endpoint to request feasible exchanges that has capacity
    for a provided new service quote.
    It takes a list of JSON objects, with fields as described:
    * requested_data_rate_mbps: int, Requested Data Rate for the Quote, in Mbps
    * requested_access_rate_mbps: int, Requested Access Rate for the Quote, in Mbps
    * postcode: str, Requested postcode for the Quote
    * contract_length: int, Length of requested contract term in months
    * serving_exchange_code: str, Exchange code for exchange that traffic will be served from
    """
    options = random.sample(EXCHANGE_OPTIONS, 3)

    return QuoteResponse(postcode=request.postcode, preferred_exchange=options[0], exchange_options=options)