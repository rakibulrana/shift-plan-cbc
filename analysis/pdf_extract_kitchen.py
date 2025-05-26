import pdfplumber
import pandas as pd

# Path to your uploaded PDF
pdf_path = "D:/Startup/Shift_plan_cbc/data/latest_schedule.pdf"

# Store results
kitchen_data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if "Wunschdienstplan CBC Bremen (Küche)" in text:
            lines = text.split('\n')
            start_extracting = False
            for line in lines:
                if line.startswith("Name BV"):
                    start_extracting = True
                    continue
                if start_extracting:
                    if not line.strip():
                        continue
                    if line.startswith("Wunschdienstplan"):
                        break
                    kitchen_data.append(line.strip())

# Preview result
#for entry in kitchen_data:
    #print(entry)


# After kitchen_data list is filled

# Define days
days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
columns = ["Name", "Contract"] + days

structured_data = []

for entry in kitchen_data:
    parts = entry.split()
    name_parts = []
    
    # Find where contract type (VZ, TZ...) starts
    for i, part in enumerate(parts):
        if part in ["VZ", "TZ", "AZB", "SAH", "AH"]:
            name = " ".join(parts[:i])
            contract = parts[i]
            rest = parts[i+1:]
            break
    else:
        continue  # skip if contract not found

    row = [name, contract] + rest[:7]
    structured_data.append(row)

# Create DataFrame
df = pd.DataFrame(structured_data, columns=columns)
print(df.head())

# Save to CSV for further analysis
df.to_csv("D:/Startup/Shift_plan_cbc/data/kitchen_availability.csv", index=False)
