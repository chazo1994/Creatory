"""create base schema

Revision ID: 20260206_0001
Revises:
Create Date: 2026-02-06 01:50:00
"""

from __future__ import annotations

from pathlib import Path

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260206_0001"
down_revision = None
branch_labels = None
depends_on = None


def _execute_sql_file(path: Path) -> None:
    bind = op.get_bind()
    sql_text = path.read_text(encoding="utf-8")

    statements = [statement.strip() for statement in sql_text.split(";") if statement.strip()]
    for statement in statements:
        bind.exec_driver_sql(statement)


def upgrade() -> None:
    project_root = Path(__file__).resolve().parents[2]
    sql_path = project_root / "sql" / "migrations" / "0001_base_schema.up.sql"
    _execute_sql_file(sql_path)


def downgrade() -> None:
    project_root = Path(__file__).resolve().parents[2]
    sql_path = project_root / "sql" / "migrations" / "0001_base_schema.down.sql"
    _execute_sql_file(sql_path)
