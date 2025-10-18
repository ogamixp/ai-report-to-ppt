from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates
import os

app = FastAPI()

# Add session middleware for authentication
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "change-me"))

# Templates directory inside webui
templates = Jinja2Templates(directory="webui/templates")

# Password for login
PASSWORD = "onoue"

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # If user is authenticated, show main page
    if request.session.get("authenticated"):
        return templates.TemplateResponse("index.html", {"request": request, "message": None})
    # Otherwise show login page
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
async def login(request: Request, password: str = Form(...)):
    # Verify password
    if password == PASSWORD:
        request.session["authenticated"] = True
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    # Invalid password
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid password"})

@app.post("/logout")
async def logout(request: Request):
    # Clear session on logout
    request.session.clear()
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, topic: str = Form(""), report_text: str = Form("")):
    # Require authentication
    if not request.session.get("authenticated"):
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    # TODO: integrate with backend to generate PPT slides using topic/report_text
    # For now, return a placeholder message
    result_message = "Slides generation triggered."
    return templates.TemplateResponse("index.html", {"request": request, "message": result_message})
