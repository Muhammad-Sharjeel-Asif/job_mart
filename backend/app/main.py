from fastapi import APIRouter, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.job_exceptions import JobClosed
from app.routers.jobs_router import job_router

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def get_health():
    return {"status": "ok"}


@app.exception_handler(JobClosed)
async def job_closed_exception_handler(request: Request, exc: JobClosed):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "job close",
            "message": f"Job {exc.job_id} is closed and no longer accepts changes...",
        },
    )


routers: list[APIRouter] = [job_router]

for router in routers:
    app.include_router(router)
