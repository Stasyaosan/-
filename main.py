from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext

import db
from db import *
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.mount('/static', StaticFiles(directory='static'))
app.add_middleware(SessionMiddleware, secret_key="lasmfklwejfl25l23klrjsgkl")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    water_limit = 0
    if 'login' in request.session:
        water_limit = get_water_limit(request.session['login'])

    return templates.TemplateResponse('index.html', {'request': request, 'water_limit': water_limit})


@app.post('/get_count_water', response_class=HTMLResponse)
def get_count_water(request: Request):
    count_water = 0
    if 'login' in request.session:
        count_water = get_water_count(request.session['login'])

    return JSONResponse(str(count_water))


@app.post('/get_water_all', response_class=HTMLResponse)
def get_water_all(request: Request):
    if 'login' in request.session:
        all_water = get_all_water(request.session['login'])
        a = {'water_limit': all_water[3], 'count_water': all_water[4]}
    return JSONResponse(a)


@app.post('/set_count_water', response_class=HTMLResponse)
def set_count_water(request: Request, count_water: str = Form(...)):
    if 'login' in request.session:
        set_water_count(request.session['login'], count_water)

    return JSONResponse(1)


@app.get('/reg', response_class=HTMLResponse)
def reg(request: Request):
    return templates.TemplateResponse('user/reg.html', {'request': request})


@app.post('/reg', response_class=HTMLResponse)
def register(request: Request, login: str = Form(...), password: str = Form(...), password_rep: str = Form(...)):
    p = pwd_context.hash(password)
    message = ''
    if password == password_rep:
        if not check_login(login):
            reg(login, p)
            message += 'Вы успешно зарегистрированы'
        else:
            message += 'Такой логин существует'
    else:
        message += 'Пароли не совпадают'
    return templates.TemplateResponse('user/reg.html', {'request': request, 'message': message})


@app.get('/auth', response_class=HTMLResponse)
def auth(request: Request):
    return templates.TemplateResponse('user/auth.html', {'request': request})


@app.post('/auth', response_class=HTMLResponse)
async def auth(request: Request, login: str = Form(...), password: str = Form(...)):
    # print(login)
    user = get_user(login)
    if not user or not pwd_context.verify(password, user[2]):
        return templates.TemplateResponse('user/auth.html',
                                          {'request': request, 'message': 'Invalid login or password'})
    request.session['login'] = login

    return RedirectResponse(url='/panel', status_code=303)


@app.get('/logout')
def logout(request: Request):
    if 'login' in request.session:
        del request.session['login']

    return RedirectResponse(url='/')


@app.get('/panel', response_class=HTMLResponse)
def panel(request: Request):
    return templates.TemplateResponse('user/panel.html', {'request': request})


@app.post('/panel', response_class=HTMLResponse)
def panel(request: Request, old_password: str = Form(...), new_password: str = Form(...)):
    user = get_user(request.session['login'])
    errors = ''
    if not pwd_context.verify(old_password, user[2]):
        errors += 'Неправильный старый пароль'
    else:
        p = pwd_context.hash(new_password)
        db.update_password(p, request.session['login'])

    return templates.TemplateResponse('user/panel.html', {'request': request, 'errors': errors})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8001)
