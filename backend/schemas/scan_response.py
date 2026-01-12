from pydantic import BaseModel
from typing import List, Dict, Any

class ScanResponse(BaseModel):
    scan_metadata: Dict[str, Any]
    roles: List[Dict[str, Any]]
