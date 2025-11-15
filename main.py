import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, Optional
from datetime import datetime

from database import db, create_document, get_documents
from schemas import (
    Client, Project, Task, Prompt, PromptSet, EngineBlueprint,
    CreativeBrief, ContentCalendarItem, WorkflowAudit, PersonaKit,
    SubscriptionTierPlan
)

app = FastAPI(title="AI Founder Command Console API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Founder Command Console API is running"}

# Generic create endpoint for any schema-backed collection
class CreatePayload(BaseModel):
    collection: str
    data: Dict[str, Any]

@app.post("/api/create")
def api_create(payload: CreatePayload):
    try:
        inserted_id = create_document(payload.collection, payload.data)
        return {"inserted_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/list/{collection}")
def api_list(collection: str, limit: Optional[int] = 100):
    try:
        items = get_documents(collection, limit=limit)
        # Convert ObjectId to str
        from bson import ObjectId
        for item in items:
            if item.get("_id"):
                item["_id"] = str(item["_id"])
            # stringify datetimes
            for k, v in list(item.items()):
                if hasattr(v, "isoformat"):
                    item[k] = v.isoformat()
        return {"items": items}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:20]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
