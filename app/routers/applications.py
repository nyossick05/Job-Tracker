from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date, timedelta

from app.dependencies import get_db, get_current_user
from app.models import Application, User
from app.schemas import ApplicationCreate, ApplicationResponse

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(application: ApplicationCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_application = Application(
        company_name=application.company_name,
        position=application.position,
        status=application.status,
        owner_id =current_user.id,
        deadline=application.deadline,
        notes=application.notes,
    )
    db.add(new_application)
    await db.commit()
    await db.refresh(new_application)
    return new_application

@router.get("/upcoming", response_model=list[ApplicationResponse])
async def get_upcoming_applications(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = date.today()
    upcoming_date = today + timedelta(days=7)
    result = await db.execute(
        select(Application).where(
            Application.owner_id == current_user.id,
            Application.deadline >= today,
            Application.deadline <= upcoming_date
        )
    )
    applications = result.scalars().all()
    return applications

@router.get("/", response_model=list[ApplicationResponse])
async def get_applications(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Application).where(Application.owner_id == current_user.id))
    applications = result.scalars().all()
    return applications

@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(application_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Application).where(Application.id == application_id, Application.owner_id == current_user.id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(application_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Application).where(Application.id == application_id, Application.owner_id == current_user.id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    await db.delete(application)
    await db.commit()

@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(application_id: int, application_update: ApplicationCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Application).where(Application.id == application_id, Application.owner_id == current_user.id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    
    application.company_name = application_update.company_name
    application.position = application_update.position
    application.status = application_update.status
    application.deadline = application_update.deadline
    application.notes = application_update.notes
    
    await db.commit()
    await db.refresh(application)
    return application