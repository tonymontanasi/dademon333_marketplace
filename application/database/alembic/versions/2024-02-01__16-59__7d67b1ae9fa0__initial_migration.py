"""Initial migration

Revision ID: 7d67b1ae9fa0
Revises:
Create Date: 2024-02-01 16:59:10.777747

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "7d67b1ae9fa0"
down_revision: str | None = None
branch_labels: Sequence[str] | str | None = None
depends_on: Sequence[str] | str | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        "sku",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "base_price", sa.Float(), server_default="0.0", nullable=False
        ),
        sa.Column(
            "is_hidden", sa.VARCHAR(), server_default="t", nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "goods",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("sku_id", sa.UUID(), nullable=False),
        sa.Column("stock", sa.VARCHAR(), nullable=False),
        sa.Column(
            "discount_percentage",
            sa.Float(),
            server_default="0.0",
            nullable=False,
        ),
        sa.Column(
            "is_reserved", sa.VARCHAR(), server_default="f", nullable=False
        ),
        sa.Column("is_sold", sa.VARCHAR(), server_default="f", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["sku_id"], ["sku.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_goods_sku_id_is_sold", "goods", ["sku_id", "is_sold"], unique=False
    )

    op.create_table(
        "discounts",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("percentage", sa.Float(), nullable=False),
        sa.Column(
            "status", sa.VARCHAR(), nullable=False, server_default="active"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "discounts_and_skus",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("discount_id", sa.UUID(), nullable=False),
        sa.Column("sku_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["discount_id"],
            ["discounts.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["sku_id"], ["sku.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_discounts_and_skus_discount_id"),
        "discounts_and_skus",
        ["discount_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_discounts_and_skus_sku_id"),
        "discounts_and_skus",
        ["sku_id"],
        unique=False,
    )

    op.create_table(
        "postings",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.VARCHAR(),
            nullable=False,
            server_default="in_item_pick",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "posting_goods",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("posting_id", sa.UUID(), nullable=False),
        sa.Column("good_id", sa.UUID(), nullable=False),
        sa.Column("good_stock", sa.VARCHAR(), nullable=False),
        sa.Column("cost", sa.Float(), nullable=False),
        sa.Column(
            "is_canceled", sa.VARCHAR(), server_default="f", nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["good_id"], ["goods.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["posting_id"],
            ["postings.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_posting_goods_good_id"),
        "posting_goods",
        ["good_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_posting_goods_posting_id"),
        "posting_goods",
        ["posting_id"],
        unique=False,
    )

    op.create_table(
        "acceptances",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "status", sa.VARCHAR(), nullable=False, server_default="in_work"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "tasks",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("type", sa.VARCHAR(), nullable=False),
        sa.Column(
            "status", sa.VARCHAR(), nullable=False, server_default="in_work"
        ),
        sa.Column("sku_id", sa.UUID(), nullable=False),
        sa.Column("stock", sa.VARCHAR(), nullable=False),
        sa.Column("count", sa.BigInteger(), nullable=False),
        sa.Column("posting_id", sa.UUID(), nullable=True),
        sa.Column("acceptance_id", sa.UUID(), nullable=True),
        sa.Column("good_id", sa.UUID(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["acceptance_id"],
            ["acceptances.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["good_id"], ["goods.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["posting_id"],
            ["postings.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["sku_id"], ["sku.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_tasks_acceptance_id"),
        "tasks",
        ["acceptance_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_tasks_good_id"), "tasks", ["good_id"], unique=False
    )
    op.create_index(
        op.f("ix_tasks_posting_id"), "tasks", ["posting_id"], unique=False
    )
    op.create_index(op.f("ix_tasks_sku_id"), "tasks", ["sku_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tasks_sku_id"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_posting_id"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_good_id"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_acceptance_id"), table_name="tasks")
    op.drop_table("tasks")

    op.drop_table("acceptances")

    op.drop_index(
        op.f("ix_posting_goods_posting_id"), table_name="posting_goods"
    )
    op.drop_index(op.f("ix_posting_goods_good_id"), table_name="posting_goods")
    op.drop_table("posting_goods")

    op.drop_table("postings")

    op.drop_index(
        op.f("ix_discounts_and_skus_sku_id"), table_name="discounts_and_skus"
    )
    op.drop_index(
        op.f("ix_discounts_and_skus_discount_id"),
        table_name="discounts_and_skus",
    )
    op.drop_table("discounts_and_skus")
    op.drop_table("discounts")

    op.drop_index("ix_goods_sku_id_is_sold", table_name="goods")
    op.drop_table("goods")
    op.drop_table("sku")

    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
    # ### end Alembic commands ###
