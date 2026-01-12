from pydantic import BaseModel
from typing import List, Dict, Any

class ExplainResponse(BaseModel):
    results: List[Dict[str, Any]]
