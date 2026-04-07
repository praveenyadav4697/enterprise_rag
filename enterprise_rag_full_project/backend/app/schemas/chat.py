from pydantic import BaseModel, Field
from typing import List

class UploadResponse(BaseModel):
    document_id: int
    filename: str
    chunks_created: int

class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=4000)

class SourceItem(BaseModel):
    document_id: int
    filename: str
    chunk_index: int
    content: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
