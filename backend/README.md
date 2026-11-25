# Job Board API

A FastAPI backend for posting and searching jobs.

> **Status:** Week 1 skeleton. Jobs are stored **in memory**, so all data resets when the server restarts. A PostgreSQL database replaces this in Week 2.

## Run locally

From the `backend/` folder:

```bash
fastapi dev app/main.py
```

- API base URL: `http://localhost:8000`
- Interactive docs (Swagger UI): `http://localhost:8000/docs`

Run the tests from the same folder:

```bash
pytest
```

## Endpoints

| Method | Path | Description | Success | Error codes |
|--------|------|-------------|---------|-------------|
| GET | `/health` | Health check | 200 | none |
| GET | `/jobs/` | List jobs with search, filters and pagination | 200 | 422 |
| GET | `/jobs/{id}` | Get one job | 200 | 404, 422 |
| POST | `/jobs/` | Create a job | 201 | 422 |
| PUT | `/jobs/{id}` | Replace a job (full update) | 200 | 400, 404, 422 |
| PATCH | `/jobs/{id}` | Update some fields of a job | 200 | 400, 404, 422 |
| DELETE | `/jobs/{id}` | Delete a job | 204 | 404, 422 |

> **Trailing slash:** the collection path is `/jobs/` (with a slash). A request to `/jobs` is redirected with `307` to `/jobs/`. Use the slash version in clients to avoid the extra redirect.

## Job object

Returned by every endpoint that responds with a job.

| Field | Type | Notes |
|-------|------|-------|
| `id` | integer | Assigned by the server |
| `title` | string | 3 to 100 characters |
| `description` | string | 3 to 500 characters |
| `location` | string | 3 to 50 characters |
| `job_type` | string | One of `Fulltime`, `Parttime`, `Hybrid`, `Onsite`, `Remote`. Default `Fulltime` |
| `salary_min` | integer or null | 0 or greater |
| `salary_max` | integer or null | 0 or greater |
| `deadline` | date or null | Format `YYYY-MM-DD`. After this date the job is **closed** |
| `skills` | list of strings | Default is an empty list |
| `created_at` | datetime | Set by the server (UTC) |

`id` and `created_at` are set by the server and cannot be sent in a request body.

---

## GET /health

Checks that the server is running.

**200 OK**
```json
{ "status": "ok" }
```

---

## GET /jobs/

Returns a list of jobs. All filters are optional and combine with **AND**. Filtering happens first, then pagination.

**Query parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | none | Case-insensitive search in `title` and `description` (1 to 100 characters) |
| `location` | string | none | Case-insensitive "contains" match on `location` (up to 50 characters) |
| `job_type` | enum | none | Exact match: `Fulltime`, `Parttime`, `Hybrid`, `Onsite`, `Remote` |
| `skip` | integer | 0 | Number of results to skip. Must be 0 or greater |
| `limit` | integer | 10 | Number of results to return. Maximum 100 |

**Responses**

| Code | Meaning |
|------|---------|
| 200 | List of jobs (empty list if nothing matches) |
| 422 | Invalid query parameter, e.g. `limit=500` or `job_type=banana` |

**Example**

```
GET /jobs/?q=python&job_type=Remote&skip=0&limit=5
```

---

## GET /jobs/{id}

Returns one job.

**Path parameter:** `id` (integer), the job id.

**Responses**

| Code | Meaning |
|------|---------|
| 200 | The job |
| 404 | No job with that id |
| 422 | `id` is not an integer |

**404 body**
```json
{ "detail": "Job with id #99999 not found" }
```

---

## POST /jobs/

Creates a job. The server assigns `id` and `created_at`.

**Request body**

Required: `title`, `description`, `location`. Everything else is optional.

```json
{
  "title": "Backend Developer",
  "description": "Build and maintain REST APIs.",
  "location": "Karachi, Pakistan",
  "job_type": "Hybrid",
  "salary_min": 80000,
  "salary_max": 120000,
  "deadline": "2027-03-01",
  "skills": ["Python", "FastAPI"]
}
```

**Responses**

| Code | Meaning |
|------|---------|
| 201 | Job created. Body is the new job |
| 422 | Missing required field or invalid value |

**201 body**
```json
{
  "title": "Backend Developer",
  "description": "Build and maintain REST APIs.",
  "location": "Karachi, Pakistan",
  "job_type": "Hybrid",
  "salary_min": 80000,
  "salary_max": 120000,
  "deadline": "2027-03-01",
  "skills": ["Python", "FastAPI"],
  "id": 1484,
  "created_at": "2026-11-25T10:14:29.585286Z"
}
```

---

## PUT /jobs/{id}

Replaces a job completely. The body has the same shape as `POST /jobs/`. Optional fields you leave out are **reset to their defaults** (`job_type` becomes `Fulltime`, the others become `null` or an empty list). To change only some fields, use `PATCH`.

A closed job (its `deadline` is before today) cannot be changed.

**Responses**

| Code | Meaning |
|------|---------|
| 200 | Updated job |
| 400 | The job is closed |
| 404 | No job with that id |
| 422 | Invalid `id` or invalid body |

**400 body**
```json
{
  "error": "job close",
  "message": "Job 1485 is closed and no longer accepts changes..."
}
```

---

## PATCH /jobs/{id}

Updates only the fields you send. Fields you leave out stay unchanged.

**Request body:** any subset of the job fields (`title`, `description`, `location`, `job_type`, `salary_min`, `salary_max`, `deadline`, `skills`).

```json
{ "title": "Senior Backend Developer" }
```

A closed job (its `deadline` is before today) cannot be changed.

**Responses**

| Code | Meaning |
|------|---------|
| 200 | Updated job |
| 400 | The job is closed (same body as `PUT`) |
| 404 | No job with that id |
| 422 | Invalid `id` or invalid body |

---

## DELETE /jobs/{id}

Deletes a job. Returns no body.

**Responses**

| Code | Meaning |
|------|---------|
| 204 | Deleted. Empty response |
| 404 | No job with that id |
| 422 | `id` is not an integer |

---

## Error formats

**404 Not Found**
```json
{ "detail": "Job with id #99999 not found" }
```

**400 Bad Request** (closed job)
```json
{
  "error": "job close",
  "message": "Job 1485 is closed and no longer accepts changes..."
}
```

**422 Unprocessable Entity** (validation error). FastAPI returns a list with one entry per invalid field. `loc` shows where the problem is.
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 3 characters",
      "input": "ab",
      "ctx": { "min_length": 3 }
    }
  ]
}
```