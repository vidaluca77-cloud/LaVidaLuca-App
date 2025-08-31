"""
Contact management routes for contact form submissions and communications.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from ..database import get_db_session
from ..models.user import User
from ..models.contact import Contact
from ..schemas.contact import (
    ContactCreate,
    ContactUpdate,
    ContactResponse,
    ContactListResponse,
    ContactFilters,
)
from ..schemas.common import ApiResponse, PaginationParams, PaginatedResponse
from ..auth.dependencies import get_current_active_user, require_admin


router = APIRouter()


@router.post("/", response_model=ApiResponse[ContactResponse])
async def create_contact(
    contact_data: ContactCreate, db: AsyncSession = Depends(get_db_session)
):
    """
    Submit a new contact form (public endpoint).
    """
    new_contact = Contact(**contact_data.dict())

    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)

    # TODO: Send notification email to admin/support team

    return ApiResponse(
        success=True,
        data=ContactResponse.from_orm(new_contact),
        message="Contact request submitted successfully",
    )


@router.get("/", response_model=ApiResponse[PaginatedResponse[ContactListResponse]])
async def list_contacts(
    pagination: PaginationParams = Depends(),
    filters: ContactFilters = Depends(),
    db: AsyncSession = Depends(get_db_session),
    admin_user: User = Depends(require_admin),
):
    """
    List contact requests with filtering (admin only).
    """
    # Build query with filters
    query = select(Contact)

    if filters.contact_type:
        query = query.where(Contact.contact_type == filters.contact_type)

    if filters.status:
        query = query.where(Contact.status == filters.status)

    if filters.priority:
        query = query.where(Contact.priority == filters.priority)

    if filters.assigned_to:
        query = query.where(Contact.assigned_to == filters.assigned_to)

    if filters.is_responded is not None:
        query = query.where(Contact.is_responded == filters.is_responded)

    if filters.search:
        search_term = f"%{filters.search.lower()}%"
        query = query.where(
            or_(
                Contact.name.ilike(search_term),
                Contact.email.ilike(search_term),
                Contact.subject.ilike(search_term),
                Contact.message.ilike(search_term),
            )
        )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    count_result = await db.execute(count_query)
    total = count_result.scalar()

    # Get contacts with pagination
    contacts_result = await db.execute(
        query.offset(pagination.offset)
        .limit(pagination.size)
        .order_by(Contact.created_at.desc())
    )
    contacts = contacts_result.scalars().all()

    contact_responses = [ContactListResponse.from_orm(contact) for contact in contacts]
    paginated_data = PaginatedResponse.create(contact_responses, total, pagination)

    return ApiResponse(
        success=True, data=paginated_data, message="Contacts retrieved successfully"
    )


@router.get("/{contact_id}", response_model=ApiResponse[ContactResponse])
async def get_contact(
    contact_id: str,
    db: AsyncSession = Depends(get_db_session),
    admin_user: User = Depends(require_admin),
):
    """
    Get contact by ID (admin only).
    """
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return ApiResponse(
        success=True,
        data=ContactResponse.from_orm(contact),
        message="Contact retrieved successfully",
    )


@router.put("/{contact_id}", response_model=ApiResponse[ContactResponse])
async def update_contact(
    contact_id: str,
    contact_update: ContactUpdate,
    db: AsyncSession = Depends(get_db_session),
    admin_user: User = Depends(require_admin),
):
    """
    Update contact status and metadata (admin only).
    """
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    # Update contact fields
    update_data = contact_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)

    await db.commit()
    await db.refresh(contact)

    return ApiResponse(
        success=True,
        data=ContactResponse.from_orm(contact),
        message="Contact updated successfully",
    )


@router.delete("/{contact_id}", response_model=ApiResponse[dict])
async def delete_contact(
    contact_id: str,
    db: AsyncSession = Depends(get_db_session),
    admin_user: User = Depends(require_admin),
):
    """
    Delete contact (admin only).
    """
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    await db.delete(contact)
    await db.commit()

    return ApiResponse(
        success=True,
        data={"deleted_contact_id": contact_id},
        message="Contact deleted successfully",
    )
