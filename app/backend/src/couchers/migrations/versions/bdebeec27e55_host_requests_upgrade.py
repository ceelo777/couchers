"""Host requests upgrade

Revision ID: bdebeec27e55
Revises: 939e33415d86
Create Date: 2020-09-29 14:11:15.542057

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bdebeec27e55'
down_revision = '939e33415d86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('host_request_events')
    op.drop_constraint('host_requests_initial_message_id_fkey', 'host_requests', type_='foreignkey')
    op.drop_constraint('host_requests_conversation_id_fkey', 'host_requests', type_='foreignkey')
    op.create_foreign_key(None, 'host_requests', 'conversations', ['id'], ['id'])
    op.drop_column('host_requests', 'initial_message_id')
    op.drop_column('host_requests', 'conversation_id')
    op.add_column('messages', sa.Column('host_request_status_target', sa.Enum('pending', 'accepted', 'rejected', 'confirmed', 'cancelled', name='hostrequeststatus'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'host_request_status_target')
    op.add_column('host_requests', sa.Column('conversation_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('host_requests', sa.Column('initial_message_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'host_requests', type_='foreignkey')
    op.create_foreign_key('host_requests_conversation_id_fkey', 'host_requests', 'conversations', ['conversation_id'], ['id'])
    op.create_foreign_key('host_requests_initial_message_id_fkey', 'host_requests', 'messages', ['initial_message_id'], ['id'])
    op.create_table('host_request_events',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('host_request_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('event_type', postgresql.ENUM('created', 'status_change_accepted', 'status_change_rejected', 'status_change_confirmed', 'status_change_cancelled', name='hostrequesteventtype'), autoincrement=False, nullable=False),
    sa.Column('after_message_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('time', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['host_request_id'], ['host_requests.id'], name='host_request_events_host_request_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='host_request_events_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='host_request_events_pkey')
    )
    # ### end Alembic commands ###
