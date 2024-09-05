from fastapi import APIRouter, HTTPException
from app.schemas import OrderRequest, OrderResponse
from app.samples import FEASIBILITY_EXCHANGES

order_router = APIRouter(tags=["Orders"])


@order_router.post("/order")
async def new_service_order(request: OrderRequest) -> OrderResponse:
    """
    Endpoint to request a feasible exchanges for provided order
    It takes a list of JSON objects, with fields as described:
    * service: obj, containing information as described in WSEService
    * order_type: str, NEW, MODIFY, or CEASE
    * interface_type: str
    * partner: obj, see Partner object
    * order_id: id related to the order being requested
    * asset_id: Sky asset reference for the circuit
    """
    if request.service.serving_exchange_mdf_id in FEASIBILITY_EXCHANGES:
        return OrderResponse(lead_time_days=0)
    raise HTTPException(
            status_code=400,
            detail="Requested order exchange is not feasible please provide another exchange.",
        )