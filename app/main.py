import logging
import sys
import time
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from prometheus_fastapi_instrumentator import Instrumentator
from app.routers import home, contact, about, projects

# -----------------
# LOGGING
# -----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("portfolio-fastapi")

app = FastAPI(title="Portfolio FastAPI")

# -----------------
# MIDDLEWARE LOGGING
# -----------------
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"latency={process_time:.3f}s"
    )
    return response

# -----------------
# PROMETHEUS METRICS
# -----------------
Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=["/metrics"],
).instrument(app).expose(app)

# -----------------
# CORS
# -----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------
# STATIC
# -----------------
static_path = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# -----------------
# ROUTERS
# -----------------
app.include_router(home.router)
app.include_router(contact.router)
app.include_router(about.router)
app.include_router(projects.router)


# -----------------
# RUN
# -----------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
