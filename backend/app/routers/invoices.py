from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.dependencies.rbac import require_contractor
from app.models import Invoice, Job, JobStatus

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/{job_id}")
def submit_invoice(
    job_id: int,
    amount: float,
    db: Session = Depends(get_db),
    user = Depends(require_contractor),
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    invoice = Invoice(
        job_id=job_id,
        amount=amount,
    )
    db.add(invoice)
    job.status = JobStatus.COMPLETED
    db.commit()
    db.refresh(invoice)
    return invoice
