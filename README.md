# mazda_data_scraper
"""
ETL all data from a pdf file
- Extract data from each page. Data type:
    + text
    + table
    + detail small images
    + overview image
- Transform data:
    + table data from pdf --> dataframes
    + for readability: remove dot line in each index page, replace unicode text with icon

- Load add extracted data to JSON file: mazda_data.jsonl
    & all extracted images saved to images folder

---------- FOR NEXT VERSIONS:
 - Process thousands of pdf manual files
 - Reduce time processing
 - Rendering scraped data for presentation, providing insights using AI/ML
 - Develop an API

"""
STEPS
Step 1: Clone this project to your local computer

Step 2: Create new virtual environment, upgrade pip
        python -m venv mazda_venv
        python.exe -m pip install --upgrade pip

Step 3: Activate mazda_venv. then, install python packages
        pip install -r requirements.txt

Step 4: Run the main.py

Results:
 - all data scraped in mazda_data.jsonl
 - all images scraped in images folder
