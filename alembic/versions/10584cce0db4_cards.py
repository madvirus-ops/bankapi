"""cards

Revision ID: 10584cce0db4
Revises: b147af7928fa
Create Date: 2023-05-11 09:39:52.056445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10584cce0db4'
down_revision = 'b147af7928fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_virtual cards_id', table_name='virtual cards')
    op.drop_table('virtual cards')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('virtual cards',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"virtual cards_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('card_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('card_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('masked_pan', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('expiry', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cvv', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('card_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('issuer', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('currency', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('balance', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('street', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('postal_code', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('country', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('updated_at', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], name='virtual cards_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='virtual cards_pkey')
    )
    op.create_index('ix_virtual cards_id', 'virtual cards', ['id'], unique=False)
    # ### end Alembic commands ###
