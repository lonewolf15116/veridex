"""
Billing endpoints for Founder Pack credit codes.

GET  /api/v1/billing/config    -> whether payments are on, test mode, pack details
POST /api/v1/billing/checkout  -> {"url": <Stripe Checkout URL>}
POST /api/v1/billing/claim     {"session_id"} -> {"code", "credits_remaining"} (idempotent)
POST /api/v1/billing/balance   {"code"} -> {"credits_remaining"}

The code is sent in request bodies or headers, never in URLs.
"""

from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services import billing

router = APIRouter()
log = logging.getLogger("veridex.billing")


def _require_enabled() -> billing.BillingSettings:
    settings = billing.load_settings()
    if not settings.payments_enabled:
        raise HTTPException(status_code=503, detail={"message": "Payments are not available yet."})
    return settings


def _stripe(settings: billing.BillingSettings):
    import stripe
    stripe.api_key = settings.stripe_key
    return stripe


@router.get("/billing/config")
def billing_config():
    s = billing.load_settings()
    return {
        "payments_enabled": s.payments_enabled,
        "test_mode": s.test_mode if s.payments_enabled else None,
        "pack": {
            "credits": billing.FOUNDER_PACK_CREDITS,
            "price_cents": billing.FOUNDER_PACK_PRICE_CENTS,
            "currency": billing.FOUNDER_PACK_CURRENCY,
        },
    }


@router.post("/billing/checkout")
async def create_checkout():
    settings = _require_enabled()
    stripe = _stripe(settings)
    try:
        session = await asyncio.to_thread(
            stripe.checkout.Session.create,
            mode="payment",
            line_items=[{
                "quantity": 1,
                "price_data": {
                    "currency": billing.FOUNDER_PACK_CURRENCY,
                    "unit_amount": billing.FOUNDER_PACK_PRICE_CENTS,
                    "product_data": {
                        "name": f"Veridex Founder Pack — {billing.FOUNDER_PACK_CREDITS} critiques",
                        "description": "One credit = one five-lens critique. Credits never expire.",
                    },
                },
            }],
            metadata={"product": billing.FOUNDER_PACK_PRODUCT, "credits": str(billing.FOUNDER_PACK_CREDITS)},
            success_url=f"{settings.site_url}/?checkout=success&session_id={{CHECKOUT_SESSION_ID}}#product",
            cancel_url=f"{settings.site_url}/?checkout=cancelled#pricing",
        )
    except Exception as e:  # noqa: BLE001
        log.exception("Stripe checkout creation failed")
        raise HTTPException(status_code=502, detail={"message": "Couldn't start checkout. Please try again."}) from e
    return {"url": session.url}


class ClaimRequest(BaseModel):
    session_id: str = Field(..., min_length=10, max_length=255, pattern=r"^cs_[A-Za-z0-9_]+$")


@router.post("/billing/claim")
async def claim(body: ClaimRequest):
    settings = _require_enabled()
    stripe = _stripe(settings)
    try:
        session = await asyncio.to_thread(stripe.checkout.Session.retrieve, body.session_id)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=404, detail={"message": "That checkout session wasn't found."}) from e

    metadata = dict(session.get("metadata") or {})
    if metadata.get("product") != billing.FOUNDER_PACK_PRODUCT:
        raise HTTPException(status_code=400, detail={"message": "That checkout isn't a Veridex Founder Pack."})
    if session.get("payment_status") != "paid":
        raise HTTPException(status_code=402, detail={"message": "Payment hasn't completed yet."})

    details = session.get("customer_details") or {}
    email = details.get("email") if hasattr(details, "get") else None
    credits = int(metadata.get("credits") or billing.FOUNDER_PACK_CREDITS)

    code, remaining = await asyncio.to_thread(
        billing.get_store().mint_for_session, body.session_id, email, credits
    )
    return {"code": code, "credits_remaining": remaining}


class BalanceRequest(BaseModel):
    code: str = Field(..., min_length=4, max_length=40)


@router.post("/billing/balance")
async def balance(body: BalanceRequest):
    _require_enabled()
    code = billing.normalise_code(body.code)
    remaining = None if code is None else await asyncio.to_thread(billing.get_store().balance, code)
    if remaining is None:
        raise HTTPException(status_code=404, detail={"message": "That code wasn't recognised."})
    return {"credits_remaining": remaining}
