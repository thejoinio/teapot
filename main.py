from starlette.applications import Starlette
from app.routes import email, telegram, discord

app = Starlette(debug=True)

app.add_route('/submit-email', email.submit_email, methods=['POST'])
app.add_route('/verify-telegram', telegram.verify_telegram, methods=['POST'])
app.add_route('/verify-discord', discord.verify_discord, methods=['POST'])
