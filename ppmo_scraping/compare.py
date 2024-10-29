import requests
from bs4 import BeautifulSoup
import csv

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
            headers = []
            for th in table.find_all('th'):
                headers.append(th.get_text(strip=True))
            
            # Extract the table rows
            rows = []
            for tr in table.find_all('tr')[1:]:  # Skip the header row
                cells = tr.find_all(['td', 'th'])
                row = [cell.get_text(strip=True) for cell in cells]
                rows.append(row)
            
            return headers, rows
        else:
            print(f"No table found on page {page_index}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for page {page_index}: {e}")
        return None, None

# Example usage: Fetch data for pages 1 to 5 and save to CSV
all_headers = []
all_rows = []

for page_index in range(0, 100):
    print(f"Fetching data for page {page_index}...")
    headers, rows = make_request(page_index)
    if headers and rows:
        if not all_headers:
            all_headers = headers  # Use headers from the first page
        all_rows.extend(rows)

# Write data to CSV file
csv_filename = 'bid_results.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(all_headers)  # Write headers
    writer.writerows(all_rows)  # Write rows

print(f"Data has been written to {csv_filename}")
