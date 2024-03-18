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

@app.get("/")
def read_root():
    return "Welcome to the URL shortener API :)"

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
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@app.post("/custom/")
def create_custom_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    '''
    Create a custom URL, Remeber to change your url to YOUR URL!,
    right now, it is set as http://yourcustomdomain.com'''
    custom_alias = url.custom_alias

     # Check if Custom Alias is Provided
    if not custom_alias:
        raise HTTPException(status_code=400, detail="Custom Alias is required")
    


    short_url = utils.generate_short_url(long_url=url.target_url, custom_alias=url.custom_alias)

    print (f'++++Custom Url is {short_url}')

    db_url = crud.create_db_url(db=db, url=url)


    return {"short_url": short_url} 

 # Check if Custom Alias is Unique
    # if crud.get_db_url_by_custom_alias(db=db, custom_alias=custom_alias):
    #     raise HTTPException(status_code=400, detail="Custom Alias already exists")


@app.get("/{url_key}")
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
    ):
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
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


@app.get("/qrcode/{short_url}")
def generate_qrcode(short_url: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(short_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_bytes = img.get_image()
    response = Response(content=img_bytes, media_type="image/png")
    return response

