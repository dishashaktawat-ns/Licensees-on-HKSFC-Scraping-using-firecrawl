import json
from firecrawl import Firecrawl
from src.models import LicenseDetailsResponse
from src.utils import extract_companies_from_firecrawl_response, process_companies_data

# Initialize Firecrawl client
app = Firecrawl(api_key="fc-a585b9eb73b44c579df04557dda5e5b7")

try:
    print("Starting scrape...")
    
    # Scrape the target URL
    result = app.scrape(
        "https://webb-site.com/dbpub/SFClicount.asp",
        formats=[{
            "type": "json",
            "schema": LicenseDetailsResponse
        }]
    )
    
    print("Scrape completed successfully!")
    print(f"Result type: {type(result)}")
    
    # Extract companies data from the json attribute
    companies_data = extract_companies_from_firecrawl_response(result)
    print(f"Extracted {len(companies_data)} companies")
    
    if companies_data:
        # Process the data
        processed_data = process_companies_data(companies_data)
        
        # Convert to JSON for output
        output_data = processed_data.model_dump_json(indent=2)
        
        # Save to file
        with open('sfc_license_data_cleaned.json', 'w', encoding='utf-8') as f:
            f.write(output_data)
            
        print(f"\nSuccessfully processed {processed_data.total_companies} companies")
        print("Data saved to 'sfc_license_data_cleaned.json'")
        
        # Show sample of first few companies
        print("\nSample of first 5 companies:")
        for i, company in enumerate(processed_data.companies[:5]):
            print(f"{i+1}. {company.company_name} - {company.total_licensed_individuals} licensed individuals")
        
        # Show statistics
        print(f"\nStatistics:")
        print(f"Average ROs: {processed_data.average_ro_count}")
        print(f"Average OLIs: {processed_data.average_oli_count}")
        print(f"Average Total: {processed_data.average_total_count}")
        print(f"Average RO Percentage: {processed_data.average_ro_percentage}%")
            
    else:
        print("No companies data found in the response")
        
        # Debug: Check what's in the result
        if hasattr(result, 'json'):
            print(f"Result.json type: {type(result.json)}")
            if isinstance(result.json, dict):
                print(f"Result.json keys: {list(result.json.keys())}")
        
        # Save the raw response for inspection
        try:
            raw_data = {
                'result_type': str(type(result)),
                'result_attributes': [attr for attr in dir(result) if not attr.startswith('_')],
            }
            if hasattr(result, 'json'):
                raw_data['json_data'] = result.json
            
            with open('debug_response.json', 'w', encoding='utf-8') as f:
                json.dump(raw_data, f, indent=2, default=str)
            
            print("Debug information saved to 'debug_response.json'")
        except Exception as e:
            print(f"Could not save debug info: {e}")
    
except Exception as e:
    print(f"Error during scraping: {e}")
    import traceback
    traceback.print_exc()