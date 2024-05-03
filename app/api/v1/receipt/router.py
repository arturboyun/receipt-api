from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.api.v1.auth.utils import SecurityManager
from app.api.v1.receipt.schemes import ReceiptCreateSchema, ReceiptResponseSchema, ReceiptPaginateSchema
from app.api.v1.receipt.services import ReceiptService
from app.api.v1.user.models import User
from app.config import settings
from app.dependencies import get_session
from .dependencies import get_receipt_service
from .filters import ReceiptFilter
from .utils import ReceiptPrinter

router = APIRouter()
raw_router = APIRouter()


@router.post("/", response_model=ReceiptResponseSchema, status_code=201)
async def create_receipt(
    receipt: ReceiptCreateSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    receipt_service: Annotated[ReceiptService, Depends(get_receipt_service)],
    current_user: Annotated[User, Depends(SecurityManager.get_current_user)],
) -> ReceiptResponseSchema:
    """Create receipt"""
    return ReceiptResponseSchema.model_validate(await receipt_service.create(session, receipt, current_user.id))


@router.get("/{receipt_id}", response_model=ReceiptResponseSchema)
async def get_receipt(
    receipt_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    receipt_service: Annotated[ReceiptService, Depends(get_receipt_service)],
) -> ReceiptResponseSchema:
    """Get receipt by id"""
    result = await receipt_service.find(session, id=receipt_id)
    if not result:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return ReceiptResponseSchema.model_validate(result)


@router.get("/", response_model=ReceiptPaginateSchema)
async def get_my_receipts(
    session: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(SecurityManager.get_current_user)],
    receipt_service: Annotated[ReceiptService, Depends(get_receipt_service)],
    receipt_filter: Annotated[ReceiptFilter, FilterDepends(ReceiptFilter)],
    limit: Annotated[int, Query(ge=1, le=settings.LIMIT_MAX)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> ReceiptPaginateSchema:
    """Get my receipts"""
    receipts = await receipt_service.find_all(session, limit, offset, receipt_filter.filter, user_id=current_user.id)
    total = await receipt_service.total(session, limit, offset, receipt_filter.filter, user_id=current_user.id)
    return ReceiptPaginateSchema(
        total=total,
        limit=limit,
        offset=offset,
        items=[ReceiptResponseSchema.model_validate(receipt) for receipt in receipts],
    )


@router.get("/raw/{receipt_id}", response_class=PlainTextResponse)
async def get_receipt_raw(
    receipt_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    receipt_service: Annotated[ReceiptService, Depends(get_receipt_service)],
    width: Annotated[int, Query(ge=1, le=100)] = 40,
):
    """Get receipt in raw text format"""
    receipt = await receipt_service.find(session, id=receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return StreamingResponse(ReceiptPrinter.print_receipt(receipt, width), media_type="text/plain")
