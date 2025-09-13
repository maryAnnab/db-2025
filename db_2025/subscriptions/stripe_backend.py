from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header, HTTPException
import stripe
import os
from loguru import logger

from db_2025.subscriptions.model import Payment
load_dotenv()
app = FastAPI()

# Stripe webhook secret (from Stripe dashboard)
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Replace these with your actual tax rate IDs
TAX_RATE_23 = "txr_23vat"
TAX_RATE_08 = "txr_8vat"


@app.post("/create-checkout-session")
async def create_checkout_session(payment: Payment):
    # todo: read from request what the client really wants to buy
    #   e.g. invoice_id
    logger.info(f"creating checkout session for {payment=}")
    try:

        # create Payment ('initated') and save to DB
        # make sure only one active Payment for a given invoice is present in DB

        session = stripe.checkout.Session.create(
            payment_method_types=["card", "blik"],
            mode="payment",
            currency="pln",
            line_items=[
                {
                    "price_data": {
                        "currency": "pln",
                        "unit_amount": 10000,  # 100 zł in grosze (net)
                        "product_data": {
                            "name": "Service 1"
                        }
                    },
                    "quantity": 1,
                    # "tax_rates": [TAX_RATE_23]
                },
                {
                    "price_data": {
                        "currency": "pln",
                        "unit_amount": 2000,  # 20 zł in grosze (net)
                        "product_data": {
                            "name": "Book 1"
                        }
                    },
                    "quantity": 1,
                    # "tax_rates": [TAX_RATE_08]
                }
            ],
            success_url="https://wsi.edu.pl/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://example.com/cancel",
        )

        # todo: update payment status in DB to "forwarded to stripe"
        logger.info(f"created checkout session: {session}")

        return {"sessionId": session.id}
    except Exception as e:
        return {"error": str(e)}


@app.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    logger.info(f"webhook called")

    try:
        # Verify signature
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        logger.warning("Invalid event signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        logger.warning("Invalid event payload")

    logger.info(f'registered event type: {event["type"]}')
    # Handle event types
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # ✅ Process order: e.g., update DB, send email, etc.
        handle_checkout_session(session)
    elif event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]
        logger.warning(f'session payment failed: {session.get("id")}')
    elif event["type"] == "checkout.session.expired":
        session = event["data"]["object"]
        logger.warning(f'session expired: {session.get("id")}')
    elif event["type"] == "payment_intent.payment_failed":
        session = event["data"]["object"]
        logger.warning(f'session expired: {session.get("id")}')
    else:
        logger.warning(f"Unhandled event type: {event['type']}")

    return {"status": "success"}


def handle_checkout_session(session):
    # todo: somehow update DB status of Payment
    # customer_email = session.get("customer_email")
    customer_email = session.get("client_reference_id")
    payment_status = session.get("payment_status")
    logger.warning(f'payment succeeded for session_id={session.get("id")}')
    meta = session.get("metadata")
    print(f'{meta=}')
    # Example: update order status in database
    print(f"Payment for {customer_email} succeeded: {payment_status}")


if __name__ == "__main__":
    import uvicorn
    print(STRIPE_WEBHOOK_SECRET)

    uvicorn.run(app, host="0.0.0.0", port=8090)
