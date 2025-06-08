from flask.cli import FlaskGroup
from app import create_app, db
from app.models.user import User
import bcrypt
import click

app = create_app()
cli = FlaskGroup(app)

@cli.command("seed_admin")
@click.option('--username', prompt=True)
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('--wallet', prompt='Pi Wallet Address')
def seed_admin(username, email, password, wallet):
    """Seed the first admin user."""
    with app.app_context():
        if User.query.filter((User.username == username) | (User.email == email)).first():
            click.echo("User with that username or email already exists.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        admin = User(
            username=username,
            email=email.lower(),
            password_hash=hashed_password,
            pi_wallet_address=wallet,
            is_active=True
        )

        db.session.add(admin)
        db.session.commit()
        click.echo("✅ Admin user seeded successfully.")