from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel

"""
Note: pydantic 2 per default allowe extra args in constructor, e.g.
User(**d), where 'email' is in d.keys()
"""


class User(BaseModel):
    id: int
    name: str


class Plan(BaseModel):
    id: UUID
    name: str
    price: float
    payment_term_days: int
    billing_interval: str  # 1M, 3M, 12M


class Invoice(BaseModel):
    id: UUID
    amount: float
    is_paid: bool
    due_date: date
    issue_date: date
    user_id: int
    subscription_id: UUID | None = None
    extra_service_id: UUID | None = None
    # either of the above 2 id's should be null


class Payment(BaseModel):
    id: UUID = uuid4()
    invoice_id: UUID = uuid4()
    status: str = 'initiated'
    provider_session_id: str | None  # e.g. session.id from stripe
    created_at: datetime | None = None


class ExtraService(BaseModel):
    id: UUID
    name: str
    price: float
    payment_term_days: int


class Subscription(BaseModel):
    # de facto User
    id: UUID
    user_id: int
    plan_id: UUID
    renewal_date: date  # on or after the next invoice issued
    end_date: date  # no renewals after this date


if __name__ == '__main__':
    d = {'id': 1, 'name': 'test', 'email': 'p@p.com'}
    u = User(**d)
