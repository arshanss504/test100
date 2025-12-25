from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.dependencies.rbac import require_agent, get_current_user
from app.models import Job, JobStatus

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/")
def create_job(
    title: str,
    description: str | None = None,
    budget: float | None = None,
    db: Session = Depends(get_db),
    user = Depends(require_agent),
):
    job = Job(
        title=title,
        description=description,
        budget=budget,
        agent_id=user["id"],
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("/")
def list_open_jobs(db: Session = Depends(get_db)):
    return db.query(Job).filter(Job.status == JobStatus.OPEN).all()
