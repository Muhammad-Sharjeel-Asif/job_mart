from datetime import date

from fastapi import APIRouter, HTTPException, Query, status

from app.database.jobs import get_id, job_found, jobs, search_job
from app.dependencies import PaginationDep
from app.job_exceptions import JobClosed
from app.schemas import JobCreate, JobResponse, JobType, JobUpdate

job_router = APIRouter(prefix="/jobs", tags=["Job Routes"])


@job_router.get("/", response_model=list[JobResponse])
def get_all_jobs(
    page: PaginationDep,
    q: str | None = Query(default=None, min_length=1, max_length=25),
    location: str | None = Query(default=None, min_length=1, max_length=25),
    job_type: JobType | None = None,
):
    return search_job(
        q=q,
        location=location,
        job_type=job_type.value if job_type else None,
        skip=page["skip"],
        limit=page["limit"],
    )


# path parameters
@job_router.get("/{id}", response_model=JobResponse)
def get_jobs(id: int):
    job, found = job_found(id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id #{id} not found",
        )
    if job is not None:
        return job


@job_router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def post_job(job_body: JobCreate):
    id = get_id()
    new_job = JobResponse(id=id, **job_body.model_dump())
    jobs.append(new_job.model_dump(mode="json"))
    return new_job


@job_router.put("/{id}", response_model=JobResponse)
def put_job(id: int, job_body: JobCreate):
    job, found = job_found(id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id #{id} not found",
        )
    if job and job.get("deadline") and job["deadline"] < date.today().isoformat():
        raise JobClosed(id)

    if job is not None:
        job.update(job_body.model_dump(mode="json"))
        return job


@job_router.patch("/{id}", response_model=JobResponse)
def patch_job(id: int, job_body: JobUpdate):
    job, found = job_found(id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id #{id} not found",
        )
    if job and job.get("deadline") and job["deadline"] < date.today().isoformat():
        raise JobClosed(id)

    if job:
        job.update(job_body.model_dump(exclude_unset=True, mode="json"))
    return job


@job_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_jobs(id: int):
    job, found = job_found(id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id #{id} not found",
        )
    if job is not None:
        jobs.remove(job)
