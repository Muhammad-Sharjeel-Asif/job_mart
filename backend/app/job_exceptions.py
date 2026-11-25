class JobClosed(Exception):
    def __init__(self, job_id: int) -> None:
        self.job_id = job_id
