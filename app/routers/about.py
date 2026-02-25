from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/about", response_class=HTMLResponse)
async def about_page():
    html_content = """
    <html>
        <head>
            <title>About</title>
        </head>
        <body>
            <h1>About Page</h1>
            <p>This is the about page for your portfolio FastAPI app.</p>
        </body>
    </html>
    """
    return html_content