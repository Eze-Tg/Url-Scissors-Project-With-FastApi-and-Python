#Url-Scissors/main.py

import validators
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models, crud, schemas, utils
from database import SessionLocal, engine
from starlette.datastructures import URL
from starlette.staticfiles import StaticFiles
from config import get_settings
from typing import Optional
from fastapi.templating import Jinja2Templates
import qrcode
from io import BytesIO
from urllib.parse import quote
from starlette.responses import Response

app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)



@app.get('/home')
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@app.post("/url", response_model=schemas.URLInfo)
def cut_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    target_url = url.target_url  # Unpack the target_url attribute
    if not validators.url(target_url):
        raise_bad_request(message="Your provided URL is not valid")

    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@app.post("/url_to_qr", response_model=schemas.URLInfo)
def generate_qrcode(url: schemas.URLBase, db: Session = Depends(get_db)) -> bytes:
    '''
    Generate a QR code for the provided URL'''
    target = url.target_url
    info =  cut_url(url, db)
    
    #encode url to handle path segmeents
    encoded_url = quote(info.url, safe='')

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4)
    
    qr.add_data(encoded_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to BytesIO buffer
    img_bytes_io = BytesIO()
    img.save(img_bytes_io)
    img_bytes_io.seek(0)
    img_bytes = img_bytes_io.getvalue()

    response = Response(content=img_bytes, media_type="image/png")
    return response


@app.get(
    "/admin/{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo)
def get_url_info(
    secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise_not_found(request)

@app.delete("/admin/{secret_key}")
def delete_url(
    secret_key: str, request: Request, db: Session = Depends(get_db)
):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)




# @app.post("/shorten", response_model=schemas.URL_QRCODE)
# def shorten_and_generate_qrcode(url: schemas.URLBase, db: Session = Depends(get_db)) -> Response:
#     print('First Pass: shorten')
#     shortened_url = create_url(url, db)
#     print(f'++++++\n The shorturl is {shortened_url.url}\n++++++++++++')
#     print('Second Pass: generate qr code')
#     qr_code = generate_qrcode(shortened_url, db)
#     print('Third Pass: return response')

#     info = url_info(shortened_url)


#     response = Response(content=qr_code)
#     response.headers["Content-Disposition"] = "attachment; filename=qr_code.png"
#     return schemas.URL_QRCODE(qr_code=qr_code, **info.dict())

#     # response = Response(content=qr_code, media_type="image/png")
#     return schemas.URL_QRCode(qr_code=qr_code)


#     # Create response with shortened URL and QR code image

#     response.headers["Content-Disposition"] = f"attachment; filename=qr_code.png"
#     return response


