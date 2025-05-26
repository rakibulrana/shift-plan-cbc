import pandas as pd
from datetime import time

# Load extracted availability
df = pd.read_csv("D:/Startup/Shift_plan_cbc/data/kitchen_availability.csv")

# Define contract limits
contract_limits = {
    'VZ': (5, 6),     # min 5, max 6 days
    'TZ': (3, 4),
    'SAH': (2, 3),
    'AH': (1, 1),
}

# Define daily shift needs
shift_times = [time(7), time(9), time(11), time(14), time(16), time(17), time(18)]
days = ["Mo", "Di", "Mi", "Do", "Fr"]

# Create empty plan structure
assignments = []

# Track how many days each person is assigned
employee_workdays = {name: 0 for name in df['Name']}

# Loop through each day and each shift
for day in days:
    for shift in shift_times:
        # Find available employees for this time slot
        available_today = df[df[day].str.contains("Individuell|Egal|07:|09:|Früh|Spät", na=False)]
        assigned = False
        for _, row in available_today.iterrows():
            name = row['Name']
            contract = row['Contract']
            min_days, max_days = contract_limits.get(contract, (0, 0))

            if employee_workdays[name] < max_days:
                # Assign this employee
                assignments.append({
                    "Name": name,
                    "Day": day,
                    "Start": shift.strftime("%H:%M"),
                    "End": (shift.replace(hour=shift.hour+2) if shift.hour < 17 else time(22)).strftime("%H:%M"),
                    "Role": "Küche"
                })
                employee_workdays[name] += 1
                assigned = True
                break  # Move to next shift

        if not assigned:
            assignments.append({
                "Name": "UNASSIGNED",
                "Day": day,
                "Start": shift.strftime("%H:%M"),
                "End": (shift.replace(hour=shift.hour+2) if shift.hour < 17 else time(22)).strftime("%H:%M"),
                "Role": "Küche"
            })

# Save output
assigned_df = pd.DataFrame(assignments)
assigned_df.to_csv("D:/Startup/Shift_plan_cbc/data/auto_shift_plan.csv", index=False)

print("✅ Shift plan generated: /data/auto_shift_plan.csv")
