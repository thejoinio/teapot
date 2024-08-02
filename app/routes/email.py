from starlette.requests import Request
from starlette.responses import JSONResponse
from ..database import get_db
from ..models import Email

async def submit_email(request: Request):
    data = await request.json()
    email_address = data.get("email")

    if not email_address:
        return JSONResponse({"status": "error", "message": "Email is required"}, status_code=400)

    db = next(get_db())  # Using `next()` to get the generator's value
    new_email = Email(email=email_address)
    db.add(new_email)
    db.commit()

    return JSONResponse({"status": "success", "email": email_address})
