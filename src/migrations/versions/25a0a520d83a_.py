"""empty message

Revision ID: 25a0a520d83a
Revises:
Create Date: 2021-11-12 11:45:29.153816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25a0a520d83a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('login_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_login_record_id'), 'login_record', ['id'], unique=False)
    op.create_index(op.f('ix_login_record_subject'), 'login_record', ['subject'], unique=False)
    op.create_table('token',
    sa.Column('opaque_token', sa.String(), nullable=False),
    sa.Column('internal_token', sa.String(), nullable=False),
    sa.Column('id_token', sa.String(), nullable=False),
    sa.Column('issued', sa.DateTime(timezone=True), nullable=False),
    sa.Column('expires', sa.DateTime(timezone=True), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.CheckConstraint('issued < expires'),
    sa.PrimaryKeyConstraint('opaque_token'),
    sa.UniqueConstraint('opaque_token')
    )
    op.create_index(op.f('ix_token_opaque_token'), 'token', ['opaque_token'], unique=False)
    op.create_index(op.f('ix_token_subject'), 'token', ['subject'], unique=False)
    op.create_table('user',
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('ssn', sa.String(), nullable=True),
    sa.Column('cvr', sa.String(), nullable=True),
    sa.CheckConstraint('ssn != NULL OR cvr != null'),
    sa.PrimaryKeyConstraint('subject'),
    sa.UniqueConstraint('ssn'),
    sa.UniqueConstraint('subject')
    )
    op.create_index(op.f('ix_user_cvr'), 'user', ['cvr'], unique=False)
    op.create_index(op.f('ix_user_ssn'), 'user', ['ssn'], unique=False)
    op.create_index(op.f('ix_user_subject'), 'user', ['subject'], unique=False)
    op.create_table('user_external',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('identity_provider', sa.String(), nullable=False),
    sa.Column('external_subject', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['subject'], ['user.subject'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('identity_provider', 'external_subject')
    )
    op.create_index(op.f('ix_user_external_external_subject'), 'user_external', ['external_subject'], unique=False)
    op.create_index(op.f('ix_user_external_id'), 'user_external', ['id'], unique=False)
    op.create_index(op.f('ix_user_external_identity_provider'), 'user_external', ['identity_provider'], unique=False)
    op.create_index(op.f('ix_user_external_subject'), 'user_external', ['subject'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_external_subject'), table_name='user_external')
    op.drop_index(op.f('ix_user_external_identity_provider'), table_name='user_external')
    op.drop_index(op.f('ix_user_external_id'), table_name='user_external')
    op.drop_index(op.f('ix_user_external_external_subject'), table_name='user_external')
    op.drop_table('user_external')
    op.drop_index(op.f('ix_user_subject'), table_name='user')
    op.drop_index(op.f('ix_user_ssn'), table_name='user')
    op.drop_index(op.f('ix_user_cvr'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_token_subject'), table_name='token')
    op.drop_index(op.f('ix_token_opaque_token'), table_name='token')
    op.drop_table('token')
    op.drop_index(op.f('ix_login_record_subject'), table_name='login_record')
    op.drop_index(op.f('ix_login_record_id'), table_name='login_record')
    op.drop_table('login_record')
    # ### end Alembic commands ###
