"""empty message

Revision ID: 367c55a3fd32
Revises: 
Create Date: 2024-04-28 22:33:21.335619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '367c55a3fd32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_password'), ['password'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_surname'), ['surname'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_surname'))
        batch_op.drop_index(batch_op.f('ix_users_password'))
        batch_op.drop_index(batch_op.f('ix_users_name'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    # ### end Alembic commands ###