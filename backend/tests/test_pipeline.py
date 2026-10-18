"""
Test suite for Cascading Pipeline & Smart Cost Routing - TDD
"""
import pytest
from app.core.pipeline import VerificationPipeline, VerificationReport, LeadQuality


def test_pipeline_valid_mobile_lead():
    pipeline = VerificationPipeline()
    report = pipeline.verify_single("+212 661 123456", check_whatsapp=True, check_telegram=True)
    
    assert isinstance(report, VerificationReport)
    assert report.is_valid is True
    assert report.phone.e164 == "+212661123456"
    assert report.carrier.carrier_name is not None
    assert report.whatsapp is not None and report.whatsapp.is_registered is True
    assert report.reachability_score >= 80
    assert report.lead_quality in [LeadQuality.EXCELLENT, LeadQuality.HIGH]
    assert report.cost_savings_pct == 0  # Processed full stack for high-value mobile


def test_pipeline_smart_skips_invalid_numbers_to_save_cost():
    pipeline = VerificationPipeline()
    report = pipeline.verify_single("not-a-number", check_whatsapp=True)
    
    assert report.is_valid is False
    assert report.whatsapp is None  # Skipped! Cost saved
    assert report.reachability_score == 0
    assert report.lead_quality == LeadQuality.DEAD
    assert report.cost_savings_pct == 100  # Saved 100% of expensive downstream checks


def test_batch_processing_speed():
    pipeline = VerificationPipeline()
    batch = ["+212 661 111111", "+33 6 12 34 56 78", "+1 415 555 2671", "invalid_123"]
    
    results = pipeline.verify_batch(batch, check_whatsapp=True)
    assert len(results) == 4
    assert sum(1 for r in results if r.is_valid) == 3
    assert sum(1 for r in results if not r.is_valid) == 1
