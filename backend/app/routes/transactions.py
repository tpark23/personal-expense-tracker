import os
from fastapi import APIRouter, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from constants.constants import *
from routes.upload import process_statement

router = APIRouter()

# Define directory to store uploaded files
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/extract/transactions")
async def extract_transactions_from_statements(directory: str = UPLOAD_DIR):
    """
    Extract transactions from all bank statements in the specified directory.
    Args:
        directory (str): The directory containing the uploaded statements. Defaults to UPLOAD_DIR.
    Returns:
        A JSON response with the extracted transactions and any errors encountered.
    """
    if not os.path.exists(directory):
        raise HTTPException(status_code=400, detail=f"Directory '{directory}' does not exist.")

    transactions = []
    failed_files = []
    
    total_files_count = len(os.listdir(directory))

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            # Open the file and call process_statement
            with open(file_path, "rb") as f:
                file_content = UploadFile(filename=filename, file=f)
                extracted_transactions = await process_statement(file_content)
                transactions.extend(extracted_transactions)
        except Exception as e:
            failed_files.append({"filename": filename, "error": str(e)})
            
    
    
    if failed_files:
        # If there are failed files, return a partial success response
        return JSONResponse(
            status_code=status.HTTP_207_MULTI_STATUS,
            content={
                "status_code": status.HTTP_207_MULTI_STATUS,
                "status_desc": "Partial Success",
                "message": "Some files were processed successfully, while others failed.",
                "total_files_count": total_files_count,
                "processed_files_count": total_files_count - len(failed_files),
                "failed_files_count": len(failed_files),
                "total_transactions": len(transactions),
                "transactions": transactions,
                "failed_files": failed_files,
            },
        )

    # Return the extracted transactions and any errors
    return {
        "status_code": status.HTTP_200_OK,
        "status_desc": "Success",
        "message": "All files were processed successfully",
        "total_files_count": total_files_count,
        "processed_files_count": total_files_count,
        "failed_files_count": 0,
        "total_transactions": len(transactions),
        "transactions": transactions,
    }