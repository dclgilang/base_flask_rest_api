"""empty message

Revision ID: b92ec4669351
Revises: 24a8a5de2f32
Create Date: 2024-02-09 14:22:33.666765

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b92ec4669351'
down_revision = '24a8a5de2f32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', mysql.CHAR(length=36), nullable=False),
    sa.Column('nama', sa.String(length=50), nullable=True),
    sa.Column('alamat', sa.String(length=50), nullable=True),
    sa.Column('foto', sa.String(length=250), nullable=True),
    sa.Column('status_menikah', sa.String(length=50), nullable=True),
    sa.Column('usia', sa.String(length=50), nullable=True),
    sa.Column('telepon', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('updated_id', mysql.CHAR(), nullable=True),
    sa.Column('deleted_id', mysql.CHAR(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee')
    # ### end Alembic commands ###
