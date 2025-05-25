from datetime import datetime, timedelta
from pydantic import BaseModel, HttpUrl
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.shortener import UrlShortner
from app.database import MySQLDatabase, get_db


templates = Jinja2Templates(directory='app/templates')

router = APIRouter()
shortner = UrlShortner()


class URLRequest(BaseModel):
    url: str
    ttl: int = 0

def set_ttl(ttl):
    if ttl == 0:
        ttl = timedelta(days=365 * 50)
    else:
        ttl = timedelta(hours=ttl)

    expires_at = datetime.now() + ttl
    return expires_at

@router.post('/create_code')
async def create_code(request: URLRequest, db: MySQLDatabase = Depends(get_db)):
    url = request.url
    ttl = request.ttl
    print(f"!!!!!!!!!!  TTL: {ttl}  !!!!!!!!!!")
    if db.url_exists(url):
        short_code = db.get_short_code_by_url(url)
        response = JSONResponse(
            content=f'http://localhost/{short_code}',
            status_code=200
        )
        return response
    
    short_code = shortner.generate_short(url)

    expires_at = set_ttl(ttl)

    db.add_url(short_code, url, expires_at=expires_at)

    response = JSONResponse(
        content=f'http://localhost/{short_code}',
        status_code=200
    )
    return response


@router.get("/{code}")
async def get_url(code: str, request: Request, db: MySQLDatabase = Depends(get_db)):
    try:
        result = db.get_url_by_short_code(code)

        if not result:
            return templates.TemplateResponse("index.html", {"request": request})
        
        print(result.expires_at)
        print(datetime.utcnow())
        if result.expires_at and result.expires_at < datetime.utcnow():
            db.delete_url(code)
            return templates.TemplateResponse("index.html", {"request": request})
        
        full_url = result.original_url

        return RedirectResponse(full_url)
    except:
        return templates.TemplateResponse("index.html", {"request": request})


@router.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})