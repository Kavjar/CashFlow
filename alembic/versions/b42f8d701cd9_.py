"""empty message

Revision ID: b42f8d701cd9
Revises: 
Create Date: 2021-04-26 23:22:43.395355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b42f8d701cd9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id_user', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('username', sa.VARCHAR(length=45), autoincrement=False, nullable=True),
                    sa.Column('firstname', sa.VARCHAR(length=45), autoincrement=False, nullable=True),
                    sa.Column('lastname', sa.VARCHAR(length=45), autoincrement=False, nullable=True),
                    sa.Column('email', sa.VARCHAR(length=45), autoincrement=False, nullable=True),
                    sa.Column('password', sa.VARCHAR(length=45), autoincrement=False, nullable=True),
                    sa.Column('phone', sa.VARCHAR(length=45), autoincrement=False, nullable=True),
                    sa.Column('account_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('family_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['account_id'], ['account.id_account'], name='user_account_id_fkey'),
                    sa.ForeignKeyConstraint(['family_id'], ['family.id_family'], name='user_family_id_fkey'),
                    sa.PrimaryKeyConstraint('id_user', name='user_pkey')
                    )
    op.create_table('account',
                    sa.Column('id_account', sa.INTEGER(),
                              server_default=sa.text("nextval('account_id_account_seq'::regclass)"), autoincrement=True,
                              nullable=False),
                    sa.Column('sum', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id_account', name='account_pkey'),
                    postgresql_ignore_search_path=False
                    )
    op.create_table('family',
                    sa.Column('id_family', sa.INTEGER(),
                              server_default=sa.text("nextval('family_id_family_seq'::regclass)"), autoincrement=True,
                              nullable=False),
                    sa.Column('surname', sa.VARCHAR(length=45), autoincrement=False, nullable=True),
                    sa.Column('budget', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id_family', name='family_pkey'),
                    postgresql_ignore_search_path=False
                    )
    op.create_table('finances',
                    sa.Column('id_fin', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('item', sa.VARCHAR(length=45), autoincrement=False, nullable=True),
                    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
                    sa.Column('account_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('status', sa.VARCHAR(length=45), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['account_id'], ['account.id_account'], name='finances_account_id_fkey'),
                    sa.PrimaryKeyConstraint('id_fin', name='finances_pkey')
                    )
    op.create_table('transactiondata',
                    sa.Column('id_transaction', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('money', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('direction', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('family_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('account_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['account_id'], ['account.id_account'],
                                            name='transactiondata_account_id_fkey'),
                    sa.ForeignKeyConstraint(['family_id'], ['family.id_family'], name='transactiondata_family_id_fkey'),
                    sa.PrimaryKeyConstraint('id_transaction', name='transactiondata_pkey')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactiondata')
    op.drop_table('finances')
    op.drop_table('family')
    op.drop_table('account')
    op.drop_table('user')
    # ### end Alembic commands ###
