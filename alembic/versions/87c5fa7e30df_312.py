"""312

Revision ID: 87c5fa7e30df
Revises: 0ef4a98a660f
Create Date: 2023-02-02 12:03:51.257765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87c5fa7e30df'
down_revision = '0ef4a98a660f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_account_ref_id', table_name='account_ref')
    op.drop_table('account_ref')
    op.drop_index('ix_user_accounts_id', table_name='user_accounts')
    op.drop_table('user_accounts')
    op.drop_index('ix_customers_id', table_name='customers')
    op.drop_table('customers')
    op.drop_index('ix_account_balance_id', table_name='account_balance')
    op.drop_table('account_balance')
    op.drop_index('ix_Users_id', table_name='Users')
    op.drop_table('Users')
    op.drop_index('ix_banks_id', table_name='banks')
    op.drop_table('banks')
    op.drop_index('ix_data_transactions_id', table_name='data_transactions')
    op.drop_table('data_transactions')
    op.drop_index('ix_Blog_id', table_name='Blog')
    op.drop_table('Blog')
    op.drop_index('ix_userpin_id', table_name='userpin')
    op.drop_table('userpin')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userpin',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('pin', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_userpin_id', 'userpin', ['id'], unique=False)
    op.create_table('Blog',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=True),
    sa.Column('body', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_Blog_id', 'Blog', ['id'], unique=False)
    op.create_table('data_transactions',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('network', sa.INTEGER(), nullable=True),
    sa.Column('payment_medium', sa.VARCHAR(), nullable=True),
    sa.Column('mobile_number', sa.VARCHAR(), nullable=True),
    sa.Column('plan', sa.INTEGER(), nullable=True),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.Column('plan_network', sa.VARCHAR(), nullable=True),
    sa.Column('plan_name', sa.VARCHAR(), nullable=True),
    sa.Column('plan_amount', sa.VARCHAR(), nullable=True),
    sa.Column('date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_data_transactions_id', 'data_transactions', ['id'], unique=False)
    op.create_table('banks',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('bank_id', sa.INTEGER(), nullable=True),
    sa.Column('code', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_banks_id', 'banks', ['id'], unique=False)
    op.create_table('Users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('first_name', sa.VARCHAR(), nullable=True),
    sa.Column('last_name', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('phoneNumber', sa.VARCHAR(), nullable=True),
    sa.Column('password', sa.VARCHAR(), nullable=True),
    sa.Column('email_verifies', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index('ix_Users_id', 'Users', ['id'], unique=False)
    op.create_table('account_balance',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_account_balance_id', 'account_balance', ['id'], unique=False)
    op.create_table('customers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('customer_id', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_customers_id', 'customers', ['id'], unique=False)
    op.create_table('user_accounts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('bank_code', sa.VARCHAR(), nullable=True),
    sa.Column('bank_name', sa.VARCHAR(), nullable=True),
    sa.Column('AccountNumber', sa.VARCHAR(), nullable=True),
    sa.Column('AccountName', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_accounts_id', 'user_accounts', ['id'], unique=False)
    op.create_table('account_ref',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('accountReference', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_account_ref_id', 'account_ref', ['id'], unique=False)
    # ### end Alembic commands ###
