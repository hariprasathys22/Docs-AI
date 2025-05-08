import tempfile
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends

from app.services.ingest import process
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/", summary="Upload a document for RAG implementation")
async def ingest_document(
    bg: BackgroundTasks, 
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    temp_dir = Path(tempfile.gettempdir()) / "rag_ingest"
    temp_dir.mkdir(exist_ok=True)

    file_path = temp_dir / file.filename

    try: 
        content = await file.read()
        file_path.write_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
    
    bg.add_task(process, file_path, user_id = user_id)
    return { "status": "queued", "filename": file.filename }