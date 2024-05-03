"""initial

Revision ID: 7e2170ac3098
Revises: 
Create Date: 2024-05-03 21:22:14.561771

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7e2170ac3098"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "payment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            sa.Enum("cash", "card", name="paymenttypeenum"),
            nullable=False,
        ),
        sa.Column("amount", sa.Numeric(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("payment_pkey")),
    )
    op.create_index(op.f("payment_id_idx"), "payment", ["id"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("user_pkey")),
    )
    op.create_index(op.f("user_id_idx"), "user", ["id"], unique=False)
    op.create_index(op.f("user_name_idx"), "user", ["name"], unique=False)
    op.create_index(
        op.f("user_username_idx"), "user", ["username"], unique=True
    )
    op.create_table(
        "receipt",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("total", sa.Numeric(), nullable=False),
        sa.Column("rest", sa.Numeric(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("payment_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["payment_id"],
            ["payment.id"],
            name=op.f("receipt_payment_id_fkey"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("receipt_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("receipt_pkey")),
    )
    op.create_index(op.f("receipt_id_idx"), "receipt", ["id"], unique=False)
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("total", sa.Numeric(), nullable=False),
        sa.Column("receipt_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["receipt_id"],
            ["receipt.id"],
            name=op.f("product_receipt_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("product_pkey")),
    )
    op.create_index(op.f("product_id_idx"), "product", ["id"], unique=False)
    op.create_index(
        op.f("product_name_idx"), "product", ["name"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("product_name_idx"), table_name="product")
    op.drop_index(op.f("product_id_idx"), table_name="product")
    op.drop_table("product")
    op.drop_index(op.f("receipt_id_idx"), table_name="receipt")
    op.drop_table("receipt")
    op.drop_index(op.f("user_username_idx"), table_name="user")
    op.drop_index(op.f("user_name_idx"), table_name="user")
    op.drop_index(op.f("user_id_idx"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("payment_id_idx"), table_name="payment")
    op.drop_table("payment")
    # ### end Alembic commands ###
