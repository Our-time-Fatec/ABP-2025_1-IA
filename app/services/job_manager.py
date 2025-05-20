from typing import Dict

class JobManager:
    def __init__(self):
        self.jobs: Dict[str, Dict] = {}

    def create_job(self, job_id: str):
        self.jobs[job_id] = {
            "status": "processing",
            "result": None
        }

    def update_job(self, job_id: str, status: str, result: dict):
        if job_id in self.jobs:
            self.jobs[job_id]["status"] = status
            self.jobs[job_id]["result"] = result

    def get_job(self, job_id: str):
        return self.jobs.get(job_id)

job_manager = JobManager()
