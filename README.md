# Sales Analytics System

A comprehensive Python-based sales data analytics platform that processes raw sales transactions, enriches data with product information from APIs, and generates detailed analytics reports.

## Overview

The Sales Analytics System is designed to:
- Parse and clean raw sales data from text files
- Validate and filter sales transactions
- Perform comprehensive data analysis (revenue, trends, regional performance)
- Enrich sales data with product details from external APIs
- Generate detailed sales analytics reports

## Features

### Data Processing
- **Data Parsing & Cleaning**: Automatically parses pipe-delimited sales data with validation rules
- **Format Support**: Handles multiple encodings (UTF-8, Latin-1, CP1252) for robust file reading
- **Data Validation**: Validates transaction IDs, product IDs, customer information, and regional data
- **Data Filtering**: Provides filtering options for refined analysis

### Analytics Capabilities
- **Revenue Analysis**: Calculate total revenue and revenue breakdowns
- **Regional Performance**: Analyze sales performance across different regions
- **Product Insights**: Identify top-selling products and low-performing items
- **Customer Analysis**: Understand customer purchasing patterns
- **Trend Analysis**: Track daily sales trends and identify peak sales days

### Data Enrichment
- **API Integration**: Fetches product details from DummyJSON Products API
- **Product Mapping**: Links sales data with product categories, brands, and ratings
- **Data Enhancement**: Enriches original sales records with API-retrieved information

### Report Generation
- **Comprehensive Reports**: Generates detailed sales analytics reports
- **Enriched Output**: Includes API-matched product information
- **File Export**: Saves processed data and reports to output files

## Project Structure

```
sales-analytics-system/
├── main.py                          # Main application controller
├── requirements.txt                 # Project dependencies
├── README.md                        # This file
├── data/
│   ├── sales_data.txt              # Raw sales transaction data
│   └── enriched_sales_data.txt      # Processed data with API enrichment
├── output/
│   └── sales_report.txt            # Generated analytics report
└── utils/
    ├── file_handler.py              # File reading utilities
    ├── data_processor.py            # Data processing and analysis functions
    └── api_handler.py               # External API integration
```

## Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Setup

1. Clone or download the project:
   ```bash
   cd sales-analytics-system
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- `requests`: For making HTTP requests to external APIs

See `requirements.txt` for version specifications.

## Usage

### Running the Application

Execute the main script to run the complete analytics pipeline:

```bash
python main.py
```

### Workflow Steps

The application follows a 10-step process:

1. **Read Sales Data** - Loads raw sales transactions from `data/sales_data.txt`
2. **Parse & Clean Data** - Validates and structures raw records
3. **Apply Filters** - Provides data filtering options
4. **Validate Records** - Confirms data integrity
5. **Analyze Data** - Performs statistical analysis
6. **Fetch API Data** - Retrieves product information from DummyJSON API
7. **Enrich Data** - Merges API details with sales data
8. **Save Enriched Data** - Exports enriched data to `data/enriched_sales_data.txt`
9. **Generate Report** - Creates analytics report to `output/sales_report.txt`
10. **Complete** - Finishes processing and displays summary

### Data Format

#### Input Data (`data/sales_data.txt`)

Pipe-delimited format with the following fields:
```
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
```

Example:
```
T001|2024-01-15|P101|Widget A|5|29.99|C001|North
T002|2024-01-15|P102|Widget B|3|49.99|C002|South
```

#### Output Data (`data/enriched_sales_data.txt`)

Enhanced format including API-matched product information:
```
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
```

## Key Modules

### `file_handler.py`
- `read_sales_data(filename)` - Reads sales data with multi-encoding support

### `data_processor.py`
Provides comprehensive data processing functions:
- `parse_and_clean_data()` - Parses and validates sales records
- `validate_and_filter_sales()` - Applies filtering logic
- `calculate_total_revenue()` - Computes total revenue
- `region_wise_sales()` - Analyzes sales by region
- `top_selling_products()` - Identifies best-performing products
- `customer_analysis()` - Analyzes customer patterns
- `daily_sales_trend()` - Tracks daily sales trends
- `find_peak_sales_day()` - Identifies highest sales day
- `low_performing_products()` - Identifies underperforming items
- `enrich_sales_data()` - Enriches data with API information
- `generate_sales_report()` - Creates final analytics report

### `api_handler.py`
- `fetch_all_products()` - Fetches products from DummyJSON API
- `create_product_mapping()` - Creates product ID to details mapping

## Error Handling

The system includes robust error handling:
- **File Not Found**: Gracefully handles missing data files
- **Encoding Issues**: Tries multiple encodings when reading files
- **API Failures**: Handles network errors and API unavailability
- **Data Validation**: Skips invalid or malformed records
- **Format Errors**: Validates all required fields and data types

## Output Files

### `output/sales_report.txt`
Comprehensive analytics report containing:
- Total revenue summary
- Regional sales breakdown
- Top-performing products
- Customer analysis
- Daily sales trends
- Peak sales information
- Low-performing products analysis

### `data/enriched_sales_data.txt`
Processed sales data with:
- Cleaned and validated transactions
- API-matched product categories
- Product brands and ratings
- Match status (whether API data was found)

## Configuration

Currently, the system fetches up to 100 products from the DummyJSON API. To modify this limit, edit the API URL in `utils/api_handler.py`:

```python
url = "https://dummyjson.com/products?limit=100"
```

## Example Output

When running the application, you'll see progress output:

```
========================================
SALES ANALYTICS SYSTEM
========================================
[1/10] Reading sales data...
Successfully read 1234 transactions
[2/10] Parsing and cleaning data...
Parsed records: 1200
Invalid records removed: 34
[3/10] Filter Options Available:
...
[10/10] Process Complete!
========================================
```

## Troubleshooting

### Issue: "File not found" error
- Ensure `data/sales_data.txt` exists in the correct location
- Check file permissions

### Issue: API Connection Errors
- Verify internet connection
- Check if DummyJSON API is accessible
- Ensure no firewall blocking API requests

### Issue: Encoding Errors
- System automatically tries UTF-8, Latin-1, and CP1252 encodings
- If still failing, ensure source file encoding is supported

## Future Enhancements

Potential improvements for future versions:
- Database integration for larger datasets
- Web UI for interactive analysis
- Real-time data streaming support
- Advanced visualization dashboards
- Machine learning-based forecasting
- Custom report templates

## License

This project is provided as-is for sales analytics purposes.

## Support

For issues or questions regarding the Sales Analytics System, review the error messages in the console output or check the data files for format compliance.

---

**Version**: 1.0  
**Last Updated**: January 2026
