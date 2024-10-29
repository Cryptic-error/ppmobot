import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define keywords for filtering
keywords = [
    "medical", "surgical", "hospital", "biomedical", "health", "equipment", "supplies",
    "hospital supplies", "medical devices", "biomedical engineering", "medical equipment",
    "diagnostic tests", "imaging equipment", "laboratory equipment", "medication",
    "surgical tools", "therapy equipment", "vaccinations", "hygiene products",
    "safety equipment", "surgical instruments", "mobility aids", "wound care products",
    "pain management devices", "disposable", "sterile", "reusable", "durable", "cleanable",
    "advanced", "innovative", "cutting-edge", "patient care", "comfort", "safety", "recovery"
]

def make_request(page_index):
    url = 'https://www.bolpatra.gov.np/egp/searchBidDashboardHomePage'
    headers = {
        'Host': 'www.bolpatra.gov.np',
        'Cookie': 'JSESSIONID=04D29E23F6312E36DEDA4CDB7B2B811C.node2',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-US',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.bolpatra.gov.np/egp/searchOpportunity',
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=1, i',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',  # Prevent caching
        'Pragma': 'no-cache'          # Prevent caching
    }

    params = {
        'bidSearchTO.title': '',
        'bidSearchTO.ifbNO': '',
        'bidSearchTO.procurementCategory': '-1',
        'bidSearchTO.procurementMethod': '-1',
        'bidSearchTO.publicEntityTitle': '',
        'bidSearchTO.publicEntity': '0',
        'parentPE': '0',
        'null_widget': '',
        'bidSearchTO.childPEId': '-1',
        'bidSearchTO.NoticePubDateText': '',
        'bidSearchTO.lastBidSubmissionDateText': '',
        'bidSearchTO.contractType': '-1',
        'currentPageIndexInput': (page_index + 1),
        'pageSizeInput': '30',
        'pageActionInput': 'goto',
        'tenderId': '',
        'addNewJV': 'false',
        'currentPageIndex': page_index,
        'pageSize': '30',
        'pageAction': '',
        'totalRecords': '133198',
        'startIndex': str((page_index - 1) * 30),
        'numberOfPages': '4440',
        'isNextAvailable': 'false',
        'isPreviousAvailable': 'false',
        '_': '1720077984558'
    }

    try:
        response = requests.get(url, headers=headers, params=params, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with the id 'dashBoardBidResult'
        table = soup.find('table', {'id': 'dashBoardBidResult'})
        
        if table:
            # Extract the table headers
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            
            # Extract the table rows
            rows = []
            for tr in table.find_all('tr')[1:]:  # Skip the header row
                cells = [cell.get_text(strip=True) for cell in tr.find_all(['td', 'th'])]
                rows.append(cells)
            
            return headers, rows
        else:
            print(f"No table found on page {page_index}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for page {page_index}: {e}")
        return None, None

def append_to_csv(headers, rows, output_csv, keywords):
    # Read existing data from CSV into a list of rows
    existing_data = []
    try:
        with open(output_csv, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            existing_data = list(reader)
    except FileNotFoundError:
        pass  # If file doesn't exist yet, continue with empty existing_data

    # Create a set of existing project titles and procurement types for quick lookup
    existing_titles = set(row[0] for row in existing_data[1:])  # Skip header row

    # Add new data to the top of existing data list
    new_data = []
    for row in rows:
        project_title, procurement_type = row[0], row[1]
        if project_title not in existing_titles and procurement_type not in existing_titles:
            new_data.append(row)

    # Append existing data after new data
    new_data.extend(existing_data)

    # Write updated data back to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)  # Write headers
        writer.writerows(new_data)  # Write all rows

# Example usage:
output_csv_filename = 'filtered_results.csv'

for page_index in range(0, 5):  # Adjust the range as needed
    print(f"Fetching data for page {page_index}...")
    headers, rows = make_request(page_index)
    if headers and rows:
        append_to_csv(headers, rows, output_csv_filename, keywords)

print(f"Filtered data has been appended to {output_csv_filename}")

# Display the updated CSV file
filtered_results = pd.read_csv(output_csv_filename)
print(filtered_results)
