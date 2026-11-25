from itertools import count
from typing import Any

jobs: list[dict[str, Any]] = [
    {
        "id": 1481,
        "title": "Senior Python Developer",
        "description": "We are looking for a Senior Python Developer to design and robust backend APIs using FastAPI and Pydantic. You will oversee database migrations and mentor junior engineers.",
        "location": "Remote, USA",
        "job_type": "Remote",
        "salary_min": 120000,
        "salary_max": 150000,
        "deadline": "2027-01-15",
        "skills": ["Python", "FastAPI", "Pydantic", "PostgreSQL", "Docker"],
        "created_at": "2026-10-27T17:15:00Z",
    },
    {
        "id": 1482,
        "title": "Data Analyst Intern",
        "description": "Join our data operations team to clean datasets, build interactive dashboards, and write optimized SQL queries for weekly business reports.",
        "location": "Chicago, IL",
        "job_type": "Hybrid",
        "salary_min": 45000,
        "salary_max": 60000,
        "deadline": "2026-01-01",
        "skills": ["Python", "SQL", "Tableau", "Pandas"],
        "created_at": "2026-10-27T16:30:22Z",
    },
    {
        "id": 1483,
        "title": "Frontend Engineer",
        "description": "Looking for a creative Frontend Engineer to build responsive user interfaces. You will collaborate closely with UI/UX designers to implement pixel-perfect components.",
        "location": "New York, NY",
        "job_type": "Onsite",
        "salary_min": 95000,
        "salary_max": 115000,
        "deadline": None,
        "skills": ["TypeScript", "React", "Tailwind CSS", "Next.js"],
        "created_at": "2026-10-27T12:05:11Z",
    },
]


_next_id = count(max(j["id"] for j in jobs) + 1)


def get_id():
    """Gives a unique id for a new job"""
    return next(_next_id)


def job_found(id: int):
    found = False
    for job in jobs:
        if id == job["id"]:
            found = True
            return job, found

    return None, False


def search_job(
    q: str | None = None,
    job_type: str | None = None,
    location: str | None = None,
    skip: int = 0,
    limit: int = 10,
):
    result = jobs

    if q and q.strip():
        term = q.strip().lower()
        result = [j for j in result if term in j["title"] or j["description"]]

    if location and location.strip():
        term = location.lower().strip()
        result = [j for j in result if term in j["location"]]

    if job_type:
        result = [j for j in result if j["job_type"] == job_type]

    return result[skip : skip + limit]