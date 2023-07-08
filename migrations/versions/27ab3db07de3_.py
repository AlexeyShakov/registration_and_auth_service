"""empty message

Revision ID: 27ab3db07de3
Revises: b2d27c780513
Create Date: 2023-07-08 19:23:37.463137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27ab3db07de3'
down_revision = 'b2d27c780513'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('surname', sa.String(length=100), nullable=True))
    op.drop_column('user', 'patronymic')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('patronymic', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('user', 'surname')
    # ### end Alembic commands ###
