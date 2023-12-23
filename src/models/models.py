from typing import List, Optional

from pydantic import BaseModel


class MainInfo(BaseModel):
    link: Optional[str]
    fullname: Optional[str]
    appearance: Optional[str]
    rank: Optional[str]
    precinct: Optional[str]
    units: list
    total_complaints: int
    total_allegations: int
    substantiated_allegations: int


class Complaint(BaseModel):
    date: str
    rank_at_time: str
    officer_details: str
    complaint_details: str
    allegations: str
    ccrb_conclusion: str


class Result(BaseModel):
    platform_id: str = 'nypd'
    # url: str
    info: MainInfo
    complaint: List[Complaint]
