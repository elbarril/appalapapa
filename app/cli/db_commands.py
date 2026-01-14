"""
Database CLI commands.

Provides commands for database management and maintenance.
"""

import click
from flask import current_app
from flask.cli import with_appcontext, AppGroup

db_cli = AppGroup("db-utils", help="Database utility commands.")


@db_cli.command("init")
@with_appcontext
def init_db():
    """Initialize the database with all tables."""
    from app.extensions import db

    click.echo("Creating all database tables...")
    db.create_all()
    click.echo("Database initialized successfully!")


@db_cli.command("drop")
@click.option("--yes", is_flag=True, help="Confirm the action")
@with_appcontext
def drop_db(yes):
    """Drop all database tables. Use with caution!"""
    if not yes:
        click.confirm("This will delete ALL data. Are you sure?", abort=True)

    from app.extensions import db

    click.echo("Dropping all database tables...")
    db.drop_all()
    click.echo("All tables dropped.")


@db_cli.command("seed")
@with_appcontext
def seed_db():
    """Seed the database with sample data for development."""
    from app.extensions import db
    from app.models.user import User
    from app.models.person import Person
    from app.models.session import TherapySession
    from datetime import date, timedelta

    click.echo("Seeding database...")

    # Create test user
    if not User.get_by_email("test@example.com"):
        user = User.create_user("test@example.com", "test123", "admin")
        db.session.add(user)
        click.echo("  Created test user: test@example.com / test123")

    # Create sample patients
    sample_patients = ["Juan García", "María López", "Carlos Rodríguez"]
    for name in sample_patients:
        if not Person.get_by_name(name):
            person = Person(name=name)
            db.session.add(person)
            click.echo(f"  Created patient: {name}")

    db.session.commit()

    # Create sample sessions
    persons = Person.query.all()
    for person in persons:
        if person.therapy_sessions.count() == 0:
            for i in range(3):
                session = TherapySession(
                    person_id=person.id,
                    session_date=date.today() - timedelta(days=i * 7),
                    session_price=100.00 + (i * 10),
                    pending=(i % 2 == 0),
                )
                db.session.add(session)
            click.echo(f"  Created 3 sessions for {person.name}")

    db.session.commit()
    click.echo("Database seeded successfully!")


@db_cli.command("backup")
@click.option("--output", "-o", default="backup.sql", help="Output file name")
@with_appcontext
def backup_db(output):
    """Create a backup of the SQLite database."""
    import shutil
    from pathlib import Path

    # Get database path from config
    db_uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")

    if "sqlite" not in db_uri:
        click.echo("Backup only supported for SQLite databases.")
        return

    # Extract file path from URI
    db_path = db_uri.replace("sqlite:///", "")

    if not Path(db_path).exists():
        click.echo(f"Database file not found: {db_path}")
        return

    # Create backup
    shutil.copy2(db_path, output)
    click.echo(f"Database backed up to: {output}")


@db_cli.command("cleanup-audit")
@click.option("--days", default=365, help="Delete logs older than this many days")
@with_appcontext
def cleanup_audit(days):
    """Clean up old audit log entries."""
    from app.services.audit_service import AuditService

    deleted = AuditService.cleanup_old_logs(days)
    click.echo(f"Deleted {deleted} audit log entries older than {days} days.")
