"""empty message

Revision ID: 71f8bfd28386
Revises: None
Create Date: 2017-11-04 14:09:58.857670

"""

# revision identifiers, used by Alembic.
revision = '71f8bfd28386'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('twId', sa.String(), nullable=True),
    sa.Column('fbId', sa.String(), nullable=True),
    sa.Column('fbToken', sa.String(), nullable=True),
    sa.Column('twToken', sa.String(), nullable=True),
    sa.Column('positiveMessage', sa.String(), nullable=True),
    sa.Column('negativeMessage', sa.String(), nullable=True),
    sa.Column('triggerDate', sa.DateTime(), nullable=True),
    sa.Column('distFromPoll', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('fbId'),
    sa.UniqueConstraint('fbToken'),
    sa.UniqueConstraint('twId'),
    sa.UniqueConstraint('twToken')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###