import requests
from bs4 import BeautifulSoup
import csv

def make_request(params):
    url = 'https://www.bolpatra.gov.np/egp/searchBidDashboardHomePage'
    headers = {
        'Host': 'www.bolpatra.gov.np',
        'Cookie': 'JSESSIONID=C856B9EE4076590107D3D3AE20F408DB.node2',
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
        'Connection': 'keep-alive'
    }

    # Print the params value
    print(f"Params: {params}")

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
            print("No table found on the page")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None


# Example usage with new parameters
new_params = {
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
    'currentPageIndexInput': '3',
    'pageSizeInput': '30',
    'pageActionInput': 'goto',
    'tenderId': '',
    'addNewJV': 'false',
    'currentPageIndex': '2',
    'pageSize': '30',
    'pageAction': '',
    'totalRecords': '133020',
    'startIndex': '30',
    'numberOfPages': '4434',
    'isNextAvailable': 'false',
    'isPreviousAvailable': 'true',
    '_': '1719209343085'
}


print("\nFetching data with new parameters...")
headers, rows = make_request(new_params)
if headers and rows:
    print("Headers:", headers)
    print("Rows:", rows)
else:
    print("No data found with new parameters")


