import os
import json
import time
import traceback
from typing import Dict, Any
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from fastapi.responses import JSONResponse

from models.request_models import PatientReportRequest, PatientReportResponse
from services.medical_report import MedicalReportService
from config.logging_info import setup_logger
from config.settings import config

# Set up logger using the centralized logging setup
logger = setup_logger("patient_report_api")

# Create router
router = APIRouter(
    prefix="/api/v1",
    tags=["Medical Report"],
    responses={404: {"description": "Not found"}},
)

# Cache for service instance to avoid creating it for every request
_service_instance = None

def get_report_service():
    """Get or create the medical report service instance"""
    global _service_instance
    if _service_instance is None:
        # Get API key from config
        api_key = config.openai_api_key
        if not api_key:
            error_msg = "OpenAI API key not found in configuration"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Initialize service
        logger.info("Initializing MedicalReportService")
        _service_instance = MedicalReportService(api_key=api_key)
    
    return _service_instance

def log_request_details(patient_data: Dict[str, Any]):
    """Log detailed request information with PII included (for demo purposes)"""
    logger.info(f"Processing patient report with data: {json.dumps(patient_data)}")

@router.post("/generate_report", response_model=PatientReportResponse)
async def generate_report(
    request: Request,
    patient_data: PatientReportRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate a medical report for a patient
    
    This endpoint processes patient data and produces a comprehensive
    medical report using LangGraph's structured output capability.
    
    Args:
        patient_data: Patient information including medical conditions,
                     demographics, allergies, etc.
    
    Returns:
        PatientReportResponse: Contains the structured medical report or error details
    """
    client_ip = request.client.host if request.client else "unknown"
    
    # Log request receipt
    logger.info(f"Received report generation request from {client_ip}")
    log_request_details(patient_data.model_dump())
    
    start_time = time.time()
    
    try:
        # Get service instance
        service = get_report_service()
        
        # Log processing start
        logger.info(f"Starting report generation for patient: {patient_data.name}")
        
        # Convert pydantic model to dict for the service
        patient_info = patient_data.model_dump()
        
        # Generate report
        report = service.generate_report(patient_info)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Convert report to dict for response
        report_dict = report.model_dump()
        
        # Log successful completion
        logger.info(f"Successfully generated report for {patient_data.name} in {processing_time:.2f}s")
        
        # Add background task to log detailed report info
        def log_report_details():
            # Log report for audit purposes (keeping PII for demo)
            logger.debug(f"Generated report content: {json.dumps(report_dict)}")
        
        background_tasks.add_task(log_report_details)
        
        # Return successful response
        return PatientReportResponse(
            success=True,
            message=f"Report successfully generated in {processing_time:.2f} seconds",
            report=report_dict
        )
        
    except Exception as e:
        # Log error with traceback
        error_message = str(e)
        logger.error(f"Error generating report: {error_message}")
        logger.error(f"Error traceback: {traceback.format_exc()}")
        
        # Return error response
        return PatientReportResponse(
            success=False,
            message="Failed to generate medical report",
            error=error_message
        )
