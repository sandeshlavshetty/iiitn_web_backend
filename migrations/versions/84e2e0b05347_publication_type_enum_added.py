"""publication type enum added

Revision ID: 84e2e0b05347
Revises: 
Create Date: 2025-03-29 14:58:19.055510

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '84e2e0b05347'
down_revision = None
branch_labels = None
depends_on = None

# Define the new ENUM type
publication_type_enum = postgresql.ENUM('publication', 'project', 'consultancy', name='publication_type_enum', create_type=False)

def upgrade():
     # Create the ENUM type in the database
    publication_type_enum.create(op.get_bind(), checkfirst=True)
    
    # Alter the column with an explicit cast
    op.execute("ALTER TABLE publication ALTER COLUMN type TYPE publication_type_enum USING type::publication_type_enum")


def downgrade():
     # Revert the column type to TEXT
    op.execute("ALTER TABLE publication ALTER COLUMN type TYPE TEXT USING type::TEXT")

    # Drop the ENUM type
    publication_type_enum.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
