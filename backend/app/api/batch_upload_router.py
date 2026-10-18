"""
Batch Upload Router: Multipart file upload (.csv, .txt) processing, contact enrichment, and CSV export.
"""
import io
import csv
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.core.pipeline import VerificationPipeline
from app.core.auth import AuthService

router = APIRouter(prefix="/v1/batch", tags=["Batch File Processing"])
pipeline = VerificationPipeline()
auth_service = AuthService()


@router.post("/upload-file")
async def upload_and_process_batch_file(
    file: UploadFile = File(...),
    user_id: Optional[int] = Form(None),
    default_country: Optional[str] = Form("MA"),
    check_whatsapp: bool = Form(True),
    check_telegram: bool = Form(False),
    check_imessage: bool = Form(False),
):
    """
    Upload a .csv or .txt file containing contacts, verify each in batch,
    deduct credits, and generate an enriched downloadable CSV file.
    """
    filename = file.filename or "contacts.csv"
    if not (filename.endswith(".csv") or filename.endswith(".txt")):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a .csv or .txt file.",
        )

    # Read content
    content_bytes = await file.read()
    try:
        content_text = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        content_text = content_bytes.decode("latin-1")

    # Extract target numbers from lines or first column of CSV
    lines = [line.strip() for line in content_text.splitlines() if line.strip()]
    if not lines:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    extracted_numbers = []
    # Check if first line is a header
    start_idx = 0
    header_candidates = ["phone", "number", "tel", "contact", "mobile", "msisdn"]
    if any(h in lines[0].lower() for h in header_candidates):
        start_idx = 1

    for line in lines[start_idx:]:
        # If comma-separated, take first token
        parts = line.split(",")
        raw_val = parts[0].strip(' "\'')
        if raw_val:
            extracted_numbers.append(raw_val)

    if not extracted_numbers:
        raise HTTPException(status_code=400, detail="No valid telephone numbers found in file.")

    if len(extracted_numbers) > 1000:
        extracted_numbers = extracted_numbers[:1000]

    # Deduct credits
    if user_id:
        try:
            auth_service.deduct_credits(user_id, amount=len(extracted_numbers))
        except ValueError as ve:
            if str(ve) == "INSUFFICIENT_CREDITS":
                raise HTTPException(
                    status_code=402,
                    detail=f"Insufficient wallet credits. Required: {len(extracted_numbers)} credits.",
                )
            raise HTTPException(status_code=400, detail=str(ve))

    # Execute verification pipeline
    reports = pipeline.verify_batch(
        numbers=extracted_numbers,
        default_country=default_country,
        check_whatsapp=check_whatsapp,
        check_telegram=check_telegram,
        check_imessage=check_imessage,
    )

    # Record tasks
    if user_id:
        for r in reports:
            auth_service.record_task(
                user_id=user_id,
                phone=r.phone.e164 or r.raw_input,
                reachability_score=r.reachability_score,
                lead_quality=r.lead_quality.value,
                carrier=r.carrier.carrier_name if r.carrier else None,
                credits_used=1,
            )

    # Build enriched CSV output
    output_stream = io.StringIO()
    writer = csv.writer(output_stream)
    writer.writerow([
        "Raw_Input",
        "Normalized_E164",
        "Country_ISO",
        "Carrier_Network",
        "Line_Type",
        "Is_VoIP",
        "WhatsApp_Active",
        "iMessage_Active",
        "Reachability_Score",
        "Lead_Quality",
        "Verification_Status",
    ])

    for r in reports:
        carrier_name = r.carrier.carrier_name if r.carrier else "Unknown"
        is_voip = r.carrier.is_voip if r.carrier else False
        line_type = r.phone.line_type.value if r.phone else "unknown"
        country = r.phone.country_iso if r.phone else "N/A"
        wa_status = r.whatsapp.is_registered if r.whatsapp else False
        im_status = r.imessage.is_registered if r.imessage else False

        writer.writerow([
            r.raw_input,
            r.phone.e164 if r.phone else "",
            country,
            carrier_name,
            line_type,
            "YES" if is_voip else "NO",
            "ACTIVE" if wa_status else "INACTIVE",
            "ACTIVE" if im_status else "INACTIVE",
            f"{r.reachability_score}%",
            r.lead_quality.value,
            "VALID" if r.is_valid else "INVALID",
        ])

    csv_content = output_stream.getvalue()
    valid_count = sum(1 for r in reports if r.is_valid)

    return {
        "success": True,
        "filename": filename,
        "total_processed": len(reports),
        "valid_count": valid_count,
        "invalid_count": len(reports) - valid_count,
        "credits_deducted": len(reports) if user_id else 0,
        "csv_export_content": csv_content,
        "results": [r.model_dump() for r in reports],
        "preview_results": [
            {
                "input": r.raw_input,
                "e164": r.phone.e164 if r.phone else "",
                "carrier": r.carrier.carrier_name if r.carrier else None,
                "score": r.reachability_score,
                "quality": r.lead_quality.value,
            }
            for r in reports[:10]
        ],
    }
