from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.dependencies.rbac import require_contractor, require_agent
from app.models import Application, Job, JobStatus, ApplicationStatus

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/apply/{job_id}")
def apply_to_job(
    job_id: int,
    proposed_cost: float,
    db: Session = Depends(get_db),
    user = Depends(require_contractor),
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job or job.status != JobStatus.OPEN:
        raise HTTPException(status_code=400, detail="Job not open")

    application = Application(
        job_id=job_id,
        contractor_id=user["id"],
        proposed_cost=proposed_cost,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


## approve application (agent)

@router.post("/approve/{application_id}")
def approve_application(
    application_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_agent),
):
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    application.status = ApplicationStatus.APPROVED
    application.job.status = JobStatus.ASSIGNED

    db.commit()
    return {"message": "Application approved"}
