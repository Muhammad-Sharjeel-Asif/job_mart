# from app.main import app
from app.main import app
from db.test_db import job_deadline, job_dict
from fastapi.testclient import TestClient

client = TestClient(app=app)


def post_job(job: dict):
    new_job = client.post("/jobs", json=job)
    assert new_job.status_code == 201
    return new_job.json()


def test_post_job():
    new_job = client.post("/jobs", json=job_dict)
    assert new_job.status_code == 201
    assert new_job.json()["title"] == job_dict["title"]
    assert "id" in new_job.json()


def test_get_job():
    job = post_job(job_dict)
    get = client.get(f"/jobs/{job['id']}")
    assert get.status_code == 200


def test_not_found():
    get = client.get("/jobs/14090")
    assert get.status_code == 404


def test_title_only_patch():
    new_job = post_job(job_dict)
    patch = client.patch(f"/jobs/{new_job['id']}", json={"title": "Javascript Dev"})
    assert patch.status_code == 200
    assert patch.json()["title"] == "Javascript Dev"
    assert patch.json()["description"] == job_dict["description"]


def test_put_successfull():
    new_job = post_job(job_dict)
    new_job["deadline"] = "2027-01-01"
    put = client.put(f"/jobs/{new_job['id']}", json=job_dict)
    assert put.status_code == 200


def test_job_closed_exception():
    new_job = post_job(job_deadline)
    put = client.put(f"/jobs/{new_job['id']}", json=job_deadline)
    assert put.status_code == 400


def test_job_type_filter():
    req = client.get("/jobs", params={"job_type": "Hybrid"})
    assert req.status_code == 200
    assert all(j["job_type"] == "Hybrid" for j in req.json())


def test_invalid_job_type():
    req = client.get("/jobs", params={"job_type": "Work from Home"})
    assert req.status_code == 422


def test_q_incase_sensitive():
    lower = client.get("/jobs", params={"q": "python"})
    upper = client.get("/jobs", params={"q": "PYTHON"})
    assert lower.json() == upper.json()


def test_limits():
    assert len(client.get("/jobs", params={"limit": 5}).json()) <= 5
