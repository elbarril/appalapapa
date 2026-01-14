"""
User management CLI commands.

Provides commands for creating and managing users.
"""

import click
from flask import current_app
from flask.cli import with_appcontext, AppGroup

user_cli = AppGroup("user", help="User management commands.")


@user_cli.command("create")
@click.option("--email", prompt=True, help="User email address")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="User password",
)
@click.option(
    "--role",
    default="therapist",
    type=click.Choice(["admin", "therapist", "viewer"]),
    help="User role",
)
@with_appcontext
def create_user(email, password, role):
    """Create a new user."""
    from app.extensions import db
    from app.models.user import User

    # Check if user exists
    if User.get_by_email(email):
        click.echo(f"Error: User with email {email} already exists.")
        return

    # Create user
    user = User.create_user(email, password, role)
    db.session.add(user)
    db.session.commit()

    click.echo(f"Created user: {email} with role: {role}")


@user_cli.command("list")
@with_appcontext
def list_users():
    """List all users."""
    from app.models.user import User

    users = User.query.all()

    if not users:
        click.echo("No users found.")
        return

    click.echo(f'{"ID":<5} {"Email":<30} {"Role":<12} {"Active":<8} {"Last Login"}')
    click.echo("-" * 80)

    for user in users:
        last_login = (
            user.last_login_at.strftime("%Y-%m-%d %H:%M")
            if user.last_login_at
            else "Never"
        )
        active = "Yes" if user.is_active else "No"
        click.echo(
            f"{user.id:<5} {user.email:<30} {user.role:<12} {active:<8} {last_login}"
        )


@user_cli.command("set-role")
@click.option("--email", prompt=True, help="User email address")
@click.option(
    "--role",
    prompt=True,
    type=click.Choice(["admin", "therapist", "viewer"]),
    help="New role",
)
@with_appcontext
def set_role(email, role):
    """Change a user's role."""
    from app.extensions import db
    from app.models.user import User

    user = User.get_by_email(email)
    if not user:
        click.echo(f"Error: User {email} not found.")
        return

    old_role = user.role
    user.role = role
    db.session.commit()

    click.echo(f"Changed role for {email}: {old_role} -> {role}")


@user_cli.command("reset-password")
@click.option("--email", prompt=True, help="User email address")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="New password",
)
@with_appcontext
def reset_password(email, password):
    """Reset a user's password."""
    from app.extensions import db
    from app.models.user import User

    user = User.get_by_email(email)
    if not user:
        click.echo(f"Error: User {email} not found.")
        return

    user.set_password(password)
    db.session.commit()

    click.echo(f"Password reset for {email}")


@user_cli.command("deactivate")
@click.option("--email", prompt=True, help="User email address")
@with_appcontext
def deactivate_user(email):
    """Deactivate a user account."""
    from app.extensions import db
    from app.models.user import User

    user = User.get_by_email(email)
    if not user:
        click.echo(f"Error: User {email} not found.")
        return

    user.is_active = False
    db.session.commit()

    click.echo(f"User {email} has been deactivated.")


@user_cli.command("activate")
@click.option("--email", prompt=True, help="User email address")
@with_appcontext
def activate_user(email):
    """Activate a user account."""
    from app.extensions import db
    from app.models.user import User

    user = User.get_by_email(email)
    if not user:
        click.echo(f"Error: User {email} not found.")
        return

    user.is_active = True
    db.session.commit()

    click.echo(f"User {email} has been activated.")
