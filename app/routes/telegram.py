from starlette.requests import Request
from starlette.responses import JSONResponse
from telethon import TelegramClient
from ..config import API_ID, API_HASH, CHANNEL

telegram_client = TelegramClient('session_name', API_ID, API_HASH)

async def verify_telegram(request: Request):
    data = await request.json()
    user_identifier = data.get('identifier')

    if not user_identifier:
        return JSONResponse({'status': 'error', 'message': 'Telegram username or phone number is required'}, status_code=400)

    await telegram_client.start()

    try:
        participant = await telegram_client.get_participant(CHANNEL, user_identifier)
        if participant:
            return JSONResponse({'status': 'success', 'message': 'User is part of the channel'})
    except Exception as e:
        return JSONResponse({'status': 'error', 'message': str(e)}, status_code=400)

    return JSONResponse({'status': 'error', 'message': 'User is not part of the channel'}, status_code=404)
