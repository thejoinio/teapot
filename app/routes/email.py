from starlette.requests import Request
from starlette.responses import JSONResponse
from ..models import Email
from ..database import get_db

async def submit_email(request: Request):
    data = await request.json()
    email = data.get('email')
    db = next(get_db())
    
    if email:
        new_email = Email(email=email)
        db.add(new_email)
        db.commit()
        db.refresh(new_email)
        return JSONResponse({'status': 'success', 'email': new_email.email})
    return JSONResponse({'status': 'error', 'message': 'email is required'}, status_code=400)
