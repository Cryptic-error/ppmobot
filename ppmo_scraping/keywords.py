import pandas as pd

# Load the CSV file
file_path = 'bid_results.csv'
bid_results = pd.read_csv(file_path)

# Define keywords for filtering
keywords = [
    "medical", "surgical", "hospital", "biomedical", "health", "equipment", "supplies", 
    "hospital supplies", "medical devices", "biomedical engineering", "medical equipment", 
    "diagnostic tests", "imaging equipment", "laboratory equipment", "medication", 
    "surgical tools", "therapy equipment", "vaccinations", "hygiene products", 
    "safety equipment", "surgical instruments", "mobility aids", "wound care products", 
    "pain management devices", "disposable", "sterile", "reusable", "durable", "cleanable", 
    "advanced", "innovative", "cutting-edge",  "patient care", "comfort", "safety", "recovery"
]

# Filter rows where Project Title or ProcurementType contains any of the keywords
filtered_results = bid_results[
    bid_results["Project Title"].str.contains('|'.join(keywords), case=False, na=False) |
    bid_results["ProcurementType"].str.contains('|'.join(keywords), case=False, na=False)
]


output_file_path = 'filtered_results.csv'
filtered_results.to_csv(output_file_path, index=False)

# Display the filtered results
print(filtered_results)
# Display the filtered results

