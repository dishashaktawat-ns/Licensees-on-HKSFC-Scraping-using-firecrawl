from .models import LicenseDetails, LicenseDetailsResponse
from typing import List, Any


def extract_companies_from_firecrawl_response(result: Any) -> List[dict]:
    """Extract companies data from Firecrawl response"""
    try:
        # Check if result has json attribute with the data
        if hasattr(result, 'json') and result.json:
            json_data = result.json
            if isinstance(json_data, dict) and 'companies' in json_data:
                companies = json_data['companies']
                if isinstance(companies, list):
                    print(f"Found {len(companies)} companies in result.json")
                    return companies
        
        print("Could not find companies data in the expected location")
        return []
        
    except Exception as e:
        print(f"Error extracting companies: {e}")
        return []


def calculate_statistics(companies: List[LicenseDetails]) -> dict:
    """Calculate comprehensive statistics for the license data"""
    if not companies:
        return {
            'average_ro_count': 0.0,
            'average_oli_count': 0.0,
            'average_total_count': 0.0,
            'average_ro_percentage': 0.0,
            'total_companies': 0
        }
    
    total_ro = sum(company.responsible_officers for company in companies)
    total_oli = sum(company.other_licensed_individuals for company in companies)
    total_licensed = sum(company.total_licensed_individuals for company in companies)
    
    # Calculate averages
    avg_ro = total_ro / len(companies)
    avg_oli = total_oli / len(companies)
    avg_total = total_licensed / len(companies)
    
    # Calculate average percentage (weighted average)
    total_percentage = sum(
        company.ro_percentage * company.total_licensed_individuals 
        for company in companies if company.ro_percentage is not None
    )
    avg_percentage = total_percentage / total_licensed if total_licensed > 0 else 0
    
    return {
        'average_ro_count': round(avg_ro, 2),
        'average_oli_count': round(avg_oli, 2),
        'average_total_count': round(avg_total, 2),
        'average_ro_percentage': round(avg_percentage, 2),
        'total_companies': len(companies)
    }


def process_companies_data(companies_data: List[dict]) -> LicenseDetailsResponse:
    """Process and validate companies data"""
    cleaned_companies = []
    
    for i, company_data in enumerate(companies_data):
        try:
            cleaned_company = LicenseDetails(**company_data)
            cleaned_companies.append(cleaned_company)
        except Exception as e:
            print(f"Error processing company {i}: {e}")
            print(f"Problematic data: {company_data}")
            continue
    
    # Calculate statistics
    stats = calculate_statistics(cleaned_companies)
    
    return LicenseDetailsResponse(
        companies=cleaned_companies,
        **stats
    )



