from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey,
    Float, Text, Date, DateTime
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()


# --------------------
# ENUMS
# --------------------
class UserRole(enum.Enum):
    AGENT = "AGENT"
    CONTRACTOR = "CONTRACTOR"


class JobStatus(enum.Enum):
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    COMPLETED = "COMPLETED"


class ApplicationStatus(enum.Enum):
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class WorkPlanStatus(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    COMPLETED = "COMPLETED"


class InvoiceStatus(enum.Enum):
    SUBMITTED = "SUBMITTED"
    PAID = "PAID"


# --------------------
# USERS
# --------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


# --------------------
# JOBS
# --------------------
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    budget = Column(Float)

    status = Column(Enum(JobStatus), default=JobStatus.OPEN)

    agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("Application", back_populates="job")
    work_plan = relationship("WorkPlan", back_populates="job", uselist=False)
    invoice = relationship("Invoice", back_populates="job", uselist=False)


# --------------------
# APPLICATIONS
# --------------------
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    contractor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    proposed_cost = Column(Float)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.SUBMITTED)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="applications")


# --------------------
# WORK PLANS
# --------------------
class WorkPlan(Base):
    __tablename__ = "work_plans"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), unique=True)

    plan_description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)

    status = Column(Enum(WorkPlanStatus), default=WorkPlanStatus.NOT_STARTED)

    job = relationship("Job", back_populates="work_plan")


# --------------------
# INVOICES
# --------------------
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), unique=True)

    amount = Column(Float, nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.SUBMITTED)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="invoice")
