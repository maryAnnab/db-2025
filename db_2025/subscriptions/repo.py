from asyncio import run

import asyncpg
from dotenv import load_dotenv
from loguru import logger

from db_2025.common.db import get_db_connection_pool
from db_2025.subscriptions.model import *

"""
AI generated repository, using prompt:

Using pydantic 2, and asyncpg (python, postgres database) create repository class, taking pool in constructor arg,
and allowing for full CRUD operations on all relevant tables (which are just plurals of the class name);
relevant functions must return full objects,
and in the read operations select's should use * and not list columns; use python 3.12 
(and avoid importing from typing package, such as using Optional).
In the "get_all" method allow for pagination, while sorting by the natural parameters for each of the classes;
all id's in create operations should be created by the database. For all tables, create also
a count method, returning the number of rows in the table.

"""


class Repo:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    # User CRUD
    async def create_user(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO users (name) VALUES ($1) RETURNING *",
                user.name
            )
            return User(**row)

    async def get_user(self, id: int) -> User | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", id)
            return User(**row) if row else None

    async def get_all_users(self, limit: int = 10, offset: int = 0) -> list[User]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM users ORDER BY name LIMIT $1 OFFSET $2",
                limit, offset
            )
            return [User(**row) for row in rows]

    async def get_users_count(self) -> int:
        async with self.pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM users")

    async def update_user(self, user: User) -> User | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "UPDATE users SET name = $1 WHERE id = $2 RETURNING *",
                user.name, user.id
            )
            return User(**row) if row else None

    async def delete_user(self, id: int) -> bool:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "DELETE FROM users WHERE id = $1 RETURNING id",
                id
            )
            return bool(row)

    # Plan CRUD
    async def create_plan(self, plan: Plan) -> Plan:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO plans (name, price, payment_term_days, billing_interval) VALUES ($1, $2, $3, $4) RETURNING *",
                plan.name, plan.price, plan.payment_term_days, plan.billing_interval
            )
            return Plan(**row)

    async def get_plan(self, id: UUID) -> Plan | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM plans WHERE id = $1", id)
            return Plan(**row) if row else None

    async def get_all_plans(self, limit: int = 10, offset: int = 0) -> list[Plan]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM plans ORDER BY name LIMIT $1 OFFSET $2",
                limit, offset
            )
            return [Plan(**row) for row in rows]

    async def get_plans_count(self) -> int:
        async with self.pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM plans")

    async def update_plan(self, plan: Plan) -> Plan | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "UPDATE plans SET name = $1, price = $2, payment_term_days = $3, billing_interval = $4 WHERE id = $5 RETURNING *",
                plan.name, plan.price, plan.payment_term_days, plan.billing_interval, plan.id
            )
            return Plan(**row) if row else None

    async def delete_plan(self, id: UUID) -> bool:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "DELETE FROM plans WHERE id = $1 RETURNING id",
                id
            )
            return bool(row)

    # Invoice CRUD
    async def create_invoice(self, invoice: Invoice) -> Invoice:
        inv = invoice
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """INSERT INTO invoices (is_paid, due_date, issue_date, user_id,
                                         subscription_id, extra_service_id, amount)
                   VALUES ($1, $2, $3, $4, $5, $6, $7)
                   RETURNING *""",
                inv.is_paid, inv.due_date, inv.issue_date, inv.user_id,
                inv.subscription_id, inv.extra_service_id, inv.amount
            )
            return Invoice(**row)

    async def get_invoice(self, id: UUID) -> Invoice | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM invoices WHERE id = $1", id)
            return Invoice(**row) if row else None

    async def get_all_invoices(self, limit: int = 10, offset: int = 0) -> list[Invoice]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM invoices ORDER BY issue_date DESC LIMIT $1 OFFSET $2",
                limit, offset
            )
            return [Invoice(**row) for row in rows]

    async def get_invoices_count(self) -> int:
        async with self.pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM invoices")

    async def update_invoice(self, invoice: Invoice) -> Invoice | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "UPDATE invoices SET is_paid = $1, due_date = $2 WHERE id = $3 RETURNING *",
                invoice.is_paid, invoice.due_date, invoice.id
            )
            return Invoice(**row) if row else None

    async def delete_invoice(self, id: UUID) -> bool:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "DELETE FROM invoices WHERE id = $1 RETURNING id",
                id
            )
            return bool(row)

    # ExtraService CRUD
    async def create_extra_service(self, extra_service: ExtraService) -> ExtraService:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO extra_services (name, price, payment_term_days) VALUES ($1, $2, $3) RETURNING *",
                extra_service.name, extra_service.price, extra_service.payment_term_days
            )
            return ExtraService(**row)

    async def get_extra_service(self, id: UUID) -> ExtraService | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM extra_services WHERE id = $1", id)
            return ExtraService(**row) if row else None

    async def get_all_extra_services(self, limit: int = 10, offset: int = 0) -> list[ExtraService]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM extra_services ORDER BY name LIMIT $1 OFFSET $2",
                limit, offset
            )
            return [ExtraService(**row) for row in rows]

    async def get_extra_services_count(self) -> int:
        async with self.pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM extra_services")

    async def update_extra_service(self, extra_service: ExtraService) -> ExtraService | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """UPDATE extra_services
                   SET name              = $1,
                       price             = $2,
                       payment_term_days = $3
                   WHERE id = $4
                   RETURNING *""",
                extra_service.name, extra_service.price, extra_service.payment_term_days, extra_service.id
            )
            return ExtraService(**row) if row else None

    async def delete_extra_service(self, id: UUID) -> bool:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "DELETE FROM extra_services WHERE id = $1 RETURNING id",
                id
            )
            return bool(row)

    # Subscription CRUD
    async def create_subscription(self, subscription: Subscription) -> Subscription:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO subscriptions (user_id, plan_id, renewal_date, end_date) VALUES ($1, $2, $3, $4) RETURNING *",
                subscription.user_id, subscription.plan_id, subscription.renewal_date, subscription.end_date
            )
            return Subscription(**row)

    async def get_subscription(self, id: UUID) -> Subscription | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM subscriptions WHERE id = $1", id)
            return Subscription(**row) if row else None

    async def get_all_subscriptions(self, limit: int = 10, offset: int = 0) -> list[Subscription]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM subscriptions ORDER BY renewal_date DESC LIMIT $1 OFFSET $2",
                limit, offset
            )
            return [Subscription(**row) for row in rows]

    async def get_subscriptions_count(self) -> int:
        async with self.pool.acquire() as conn:
            return await conn.fetchval("SELECT COUNT(*) FROM subscriptions")

    async def update_subscription(self, subscription: Subscription) -> Subscription | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "UPDATE subscriptions SET user_id = $1, plan_id = $2, renewal_date = $3, end_date = $4 WHERE id = $5 RETURNING *",
                subscription.user_id, subscription.plan_id, subscription.renewal_date, subscription.end_date, subscription.id
            )
            return Subscription(**row) if row else None

    async def delete_subscription(self, id: UUID) -> bool:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "DELETE FROM subscriptions WHERE id = $1 RETURNING id",
                id
            )
            return bool(row)

    # Payment CRUD

    async def create_payment(self, payment: Payment) -> Payment:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                                      INSERT INTO "payments" (invoice_id, provider_session_id, status)
                                      VALUES ($1, $2, $3)
                                      RETURNING *;
                                      """, payment.invoice_id, payment.provider_session_id, payment.status)
            return Payment(**row)

    async def get_by_id_payment(self, payment_id: UUID) -> Payment | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                                      SELECT *
                                      FROM "payments"
                                      WHERE id = $1;
                                      """, payment_id)
            return Payment(**row) if row else None

    async def get_all_payment(self, limit: int = 10, offset: int = 0) -> list[Payment]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                                    SELECT *
                                    FROM "payments"
                                    ORDER BY created_at DESC
                                    LIMIT $1 OFFSET $2;
                                    """, limit, offset)
            return [Payment(**row) for row in rows]

    async def update_payment(self, payment: Payment) -> Payment | None:
        p = payment
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                                      UPDATE "payments"
                                      SET provider_session_id = $1,
                                          status      = $2
                                      WHERE id = $3
                                      RETURNING *;
                                      """, p.provider_session_id, p.status, p.id)
            return Payment(**row) if row else None

    async def delete_payment(self, payment_id: UUID) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute("""
                                        DELETE
                                        FROM "payments"
                                        WHERE id = $1;
                                        """, payment_id)
            # todo: check if this works
            return result.endswith("1")

    async def count_payment(self) -> int:
        async with self.pool.acquire() as conn:
            count = await conn.fetchval("""
                                        SELECT COUNT(*)
                                        FROM "payments";
                                        """)
            return count

    async def update_account_funds(self, user_id: int, amount: int) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute("""
                                        UPDATE money
                                        SET funds = funds + $1
                                        WHERE user_id = $2;
                                        """, amount, user_id)
            return result.endswith("1")

    async def transfer_money(self, source_user_id: int, target_user_id: int, amount: int) -> bool:
        logger.info('starting transfer money')
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                result = await conn.execute("""
                                            UPDATE money
                                            SET funds = funds + $1
                                            WHERE user_id = $2;""",
                                            amount, source_user_id)
                logger.info(f'money subtracted from {source_user_id}')
                # raise RuntimeError('test')
                result = await conn.execute("""
                                            UPDATE money
                                            SET funds = funds - $1
                                            WHERE user_id = $2;""",
                                            amount, target_user_id, timeout=15)
                logger.info(f'money added to {target_user_id}')

        logger.info('transfer money finished')

    async def transfer_money_simple(self, source_user_id: int, target_user_id: int, amount: int) -> bool:
        logger.info('starting transfer money')
        """
        Uwaga -- tak nie wolno pisać!!!!
        Ten kod w każdym callu do .update_account_funds otwiera nowe connections....
        które nie podlegają rollback-owi przy rollback-owaniu transakcji
        """

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await self.update_account_funds(source_user_id, -amount)
                logger.info(f'money subtracted from {source_user_id}')
                raise RuntimeError('test')
                await self.update_account_funds(target_user_id, amount)
                logger.info(f'money added to {target_user_id}')


        logger.info('transfer money finished')



async def main():
    load_dotenv()
    # ... napisac kod testujacy
    pool = await get_db_connection_pool()
    repo = Repo(pool)
    n_subscriptions = await repo.get_subscriptions_count()
    logger.info(f"Ilosc subskrypcji: {n_subscriptions}")
    # await repo.transfer_money(1, 3, 10)
    await repo.transfer_money_simple(1, 3, 11)

    await pool.close()


if __name__ == '__main__':
    run(main())
