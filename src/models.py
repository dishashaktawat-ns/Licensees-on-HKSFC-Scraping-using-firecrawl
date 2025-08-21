from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import date, datetime


class LicenseDetails(BaseModel):
    """Model for SFC license details from Webb-site with cleaning and normalization"""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # Basic company information
    rank: Optional[int] = Field(default=None, description="Ranking position of the firm")
    company_name: str = Field(description="Name of the licensed firm")
    company_url: str = Field(description="URL to company details page")
    
    # License counts
    responsible_officers: int = Field(description="Number of responsible officers")
    other_licensed_individuals: int = Field(description="Number of other licensed individuals")
    total_licensed_individuals: int = Field(description="Total licensed individuals")
    
    # Changes in license counts
    ro_change: int = Field(description="Change in responsible officers")
    oli_change: int = Field(description="Change in other licensed individuals")
    total_change: int = Field(description="Total change in licensed individuals")
    
    # Historical data
    historical_ro_change: Optional[int] = Field(default=0, description="Historical change in responsible officers")
    historical_oli_change: Optional[int] = Field(default=0, description="Historical change in other licensed individuals")
    historical_total_change: Optional[int] = Field(default=0, description="Historical total change")
    
    # Statistics
    ro_percentage: float = Field(description="Percentage of responsible officers")
    oli_percentage: Optional[float] = Field(default=None, description="Percentage of other licensed individuals")
    
    # Dates
    first_licensed_date: Optional[date] = Field(default=None, description="Date when first licensed")
    latest_licensed_date: Optional[date] = Field(default=None, description="Date of latest license")
    
    # Additional metadata
    sfc_id: Optional[str] = Field(default=None, description="SFC unique identifier")
    activities: Optional[List[str]] = Field(default_factory=list, description="Types of licensed activities")
    
    # Validators for cleaning and normalization
    @field_validator('company_name', mode='before')
    @classmethod
    def clean_company_name(cls, v):
        """Clean and normalize company name"""
        if not v:
            return ""
        return str(v).strip().title()
    
    @field_validator('responsible_officers', 'other_licensed_individuals', 'total_licensed_individuals',
               'ro_change', 'oli_change', 'total_change', 
               'historical_ro_change', 'historical_oli_change', 'historical_total_change', mode='before')
    @classmethod
    def clean_numeric_fields(cls, v):
        """Clean and convert numeric fields"""
        if v is None:
            return 0
        try:
            return int(v)
        except (ValueError, TypeError):
            return 0
    
    @field_validator('ro_percentage', 'oli_percentage', mode='before')
    @classmethod
    def clean_percentage_fields(cls, v):
        """Clean and convert percentage fields"""
        if v is None:
            return None
        try:
            return round(float(v), 2)
        except (ValueError, TypeError):
            return None
    
    @field_validator('first_licensed_date', 'latest_licensed_date', mode='before')
    @classmethod
    def parse_dates(cls, v):
        """Parse and validate date fields"""
        if not v:
            return None
        
        if isinstance(v, date):
            return v
        
        try:
            return datetime.strptime(str(v), '%Y-%m-%d').date()
        except ValueError:
            return None
    
    @field_validator('activities', mode='before')
    @classmethod
    def clean_activities(cls, v):
        """Clean and normalize activities list"""
        if not v:
            return []
        return [str(act).strip().title() for act in v if act]


class LicenseDetailsResponse(BaseModel):
    """Response model containing multiple license details with statistics"""
    companies: List[LicenseDetails]
    average_ro_count: float = Field(description="Average number of responsible officers")
    average_oli_count: float = Field(description="Average number of other licensed individuals")
    average_total_count: float = Field(description="Average total licensed individuals")
    average_ro_percentage: float = Field(description="Average percentage of responsible officers")
    total_companies: int = Field(description="Total number of companies in the list")