# File upload endpoints
import os
from io import BytesIO
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from constants.constants import *

from services.transactions import extract_transactions_from_statement

router = APIRouter()

# Define directory to store uploaded files
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_statement(file: UploadFile) -> list:
    """
    Process the uploaded bank statement and extract transactions.
    """
    # Read the file content into memory
    content = await file.read()
    file_stream = BytesIO(content)

    # Call the service to extract transactions
    transactions = extract_transactions_from_statement(file_stream)

    return transactions

@router.post("/upload/statement")
async def upload_statement(files: list[UploadFile] = File(...)):
    """
    Handles the upload of PDF files via a POST request.
    Endpoint:
        POST /upload/statement
    Args:
        files (list[UploadFile]): A list of files to be uploaded. Each file must be a PDF.
    Returns:
        200 Success if all files are uploaded successfully.
        207 Partial Success if some files fail to upload.
        400 Bad Request if no files were uploaded successfully.
    Raises:
        Exception: If an error occurs while saving a file to the upload directory.
    Notes:
        - Files that are not PDFs will be rejected.
        - Duplicate files (files with the same name as an existing file in the upload directory) will be rejected.
        - Successfully uploaded files are saved to the specified upload directory.
    """
    # Clear the upload directory before processing new files
    clear_upload_dir()

    # Maintain the uploaded files
    uploaded_files = []
    failed_files = []
    
    for file in files:
        # Check if the file is a PDF
        if not file.filename.endswith(".pdf"):
            failed_files.append({"filename": file.filename, "error": "File must be a PDF"})
            continue
        
        # Check if the file already exists
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        if os.path.exists(file_path):
            failed_files.append({"filename": file.filename, "error": "Duplicate file. File already exists."})
            continue

        try:
            # Save the file to the upload directory
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Save the file content to memory or storage (if needed)
            # For now, we just append the filename to the uploaded list
            uploaded_files.append({"filename": file.filename, "status": "Uploaded successfully"})
        except Exception as e:
            failed_files.append({"filename": file.filename, "error": str(e)})

    # 400 Bad Request if no files were uploaded successfully
    if not uploaded_files: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status_code": status.HTTP_400_BAD_REQUEST,
                "status_desc": "Bad Request",
                "message": "No files were uploaded successfully",
                "failed_files_count": len(failed_files),
                "failed_files": failed_files,
            },
        )
        
    # 207 Partial Success
    if failed_files:
        return JSONResponse(
            status_code=status.HTTP_207_MULTI_STATUS,
            content={
                "status_code": status.HTTP_207_MULTI_STATUS,
                "status_desc": "Partial Success",
                "message": "Some files were not uploaded successfully",
                "total_files_count": len(uploaded_files),
                "failed_files_count": len(failed_files),
                "uploaded_files": uploaded_files,
                "failed_files": failed_files,
            },
        )
    
    # 200 OK if all files were uploaded successfully
    return {
        "status_code": status.HTTP_200_OK,
        "status_desc": "Success",
        "message": "Files uploaded successfully",
        "total_files_count": len(uploaded_files),
        "uploaded_files": uploaded_files,
    }


def clear_upload_dir():
    """
    Clears all files in the upload directory.
    """
    if not os.path.exists(UPLOAD_DIR):
        raise HTTPException(status_code=400, detail=f"Directory '{UPLOAD_DIR}' does not exist.")
    
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)