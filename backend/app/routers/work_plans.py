from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.dependencies.rbac import require_contractor
from app.models import WorkPlan, Job, JobStatus

router = APIRouter(prefix="/work-plans", tags=["WorkPlans"])

@router.post("/{job_id}")
def create_work_plan(
    job_id: int,
    plan_description: str,
    db: Session = Depends(get_db),
    user = Depends(require_contractor),
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job or job.status != JobStatus.ASSIGNED:
        raise HTTPException(status_code=400, detail="Job not assigned")

    work_plan = WorkPlan(
        job_id=job_id,
        plan_description=plan_description,
    )
    db.add(work_plan)
    db.commit()
    db.refresh(work_plan)
    return work_plan
