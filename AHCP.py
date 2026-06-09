"""
Endpoint signatures for clinical note and monthly report CRUD.
Bodies are intentionally empty — implementation goes in router.py.
"""
import datetime
from typing import Literal, Optional, Union

from alyf_models.common_fhir import Alyf_FHIR_Composition
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.auth.auth import token_auth

router = APIRouter()

ClinicalNoteType = Literal["CCM", "RPM"]


# ── Response models ──────────────────────────────────────────────────────────

class ClinicalNoteResponse(BaseModel):
    """Returned by create and read. Use id for update/delete."""
    id: str
    member_id: str
    composition_type: ClinicalNoteType
    service_month: datetime.date  # normalised to 1st of month
    note: Union[
        Alyf_FHIR_Composition.ClinicalNoteCCM,
        Alyf_FHIR_Composition.ClinicalNoteRPM,
    ]
    created_at: datetime.datetime


class MonthlyReportResponse(BaseModel):
    """Returned by monthly report create and read. Use id for update."""
    id: str
    provider_id: str
    composition_type: ClinicalNoteType
    service_month: datetime.date  # normalised to 1st of month
    report: dict  
    created_at: datetime.datetime


# ── Clinical Note endpoints ──────────────────────────────────────────────────

@router.post("/clinical_note/create", response_model=ClinicalNoteResponse)
async def create_clinical_note(
    member_id: str,
    composition_type: ClinicalNoteType,
    service_month: datetime.date,
    overwrite: bool = False,
    provider_id: str = Depends(token_auth),
) -> ClinicalNoteResponse:
    """
    Generate and persist a clinical note for one member.

    - member_id:        target member
    - composition_type: "CCM" or "RPM"
    - service_month:    any date in the target month; day is ignored (e.g. date(2026, 5, 1))
    - overwrite:        False → return cached if note already exists for this member/type/month.
                        True  → re-invoke medulla workflow and overwrite existing record.

    Returns the note with its fhir_compositions DB id — pass that id to update/delete.
    """
    ...


@router.get("/clinical_note/read", response_model=ClinicalNoteResponse)
async def read_clinical_note(
    member_id: str,
    composition_type: ClinicalNoteType,
    service_month: datetime.date,
    provider_id: str = Depends(token_auth),
) -> ClinicalNoteResponse:
    """
    Fetch an existing clinical note from fhir_compositions.

    - service_month: any date in the target month; day is ignored.

    Raises 404 if no note exists for this member/type/month.
    """
    ...


@router.put("/clinical_note/update", response_model=ClinicalNoteResponse)
async def update_clinical_note(
    composition_id: str,
    provider_id: str = Depends(token_auth),
) -> ClinicalNoteResponse:
    """
    Force-regenerate a clinical note by its DB id.

    Looks up member_id, composition_type, and month from the existing record,
    overwrites the row in fhir_compositions.
    Returns the refreshed note with the same id.
    """
    ...


@router.delete("/clinical_note/delete", status_code=204)
async def delete_clinical_note(
    composition_id: str,
    provider_id: str = Depends(token_auth),
) -> None:
    """
    Delete a clinical note from fhir_compositions by its DB id.
    """
    ...


# ── Monthly Report endpoints ─────────────────────────────────────────────────

@router.post("/monthly_report/create", response_model=MonthlyReportResponse)
async def create_monthly_report(
    composition_type: ClinicalNoteType,
    service_month: datetime.date,
    overwrite: bool = False,
    provider_id: str = Depends(token_auth),
) -> MonthlyReportResponse:
    """
    Generate and persist the monthly billing summary report for a practice.

    - composition_type: "CCM" or "RPM"
    - service_month:    any date in the target month; day is ignored
    - overwrite:        False → return cached if report already exists for this provider/type/month.
                        True  → re-aggregate qualifying members and regenerate.

    The auth'd provider_id determines the practice.
    Returns the report with its DB id — pass that id to update.
    """
    ...


@router.get("/monthly_report/read", response_model=MonthlyReportResponse)
async def read_monthly_report(
    composition_type: ClinicalNoteType,
    service_month: datetime.date,
    provider_id: str = Depends(token_auth),
) -> MonthlyReportResponse:
    """
    Fetch an existing monthly report.

    - service_month: any date in the target month; day is ignored.

    Raises 404 if no report exists for this provider/type/month.
    """
    ...


@router.put("/monthly_report/update", response_model=MonthlyReportResponse)
async def update_monthly_report(
    report_id: str,
    provider_id: str = Depends(token_auth),
) -> MonthlyReportResponse:
    """
    Refresh a monthly report by its DB id.

    Looks up provider_id, composition_type, and month from the existing record,
    Returns the updated report with the same id.
    """
    ...
