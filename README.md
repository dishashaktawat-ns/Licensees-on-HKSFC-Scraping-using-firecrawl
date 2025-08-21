# SFC Licensees Pipeline

A robust pipeline for extracting, transforming, and loading SFC licensees data from Webb-site.

## Features

- **Data Extraction**: Robust web scraping with retry logic and rate limiting
- **Data Validation**: Pydantic models for schema validation
- **Historical Tracking**: Time series data for the last 90 days
- **Error Handling**: Comprehensive logging and error tracking
- **Modular Design**: Separated extraction, transformation, and loading components

## Data Model

### Company Schema
```json
{
  "sfc_id": "123456",
  "name": "Company Name",
  "first_licensed_date": "2020-01-01",
  "latest_licensed_date": "2023-01-01"
}