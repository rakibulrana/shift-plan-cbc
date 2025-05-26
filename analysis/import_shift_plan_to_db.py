import os
import sys
import django
import pandas as pd
from datetime import datetime

# ✅ Add the parent directory to PYTHONPATH so "backend" is found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Django project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from kitchen.models import Shift, Employee

# Load the generated CSV
df = pd.read_csv("D:/Startup/Shift_plan_cbc/data/auto_shift_plan.csv")

# Optional: clear previous shifts
Shift.objects.all().delete()

for _, row in df.iterrows():
    name = row['Name']
    if name == "UNASSIGNED":
        employee = None
    else:
        employee = Employee.objects.filter(name__iexact=name).first()
        if not employee:
            print(f"⚠️ Employee not found in DB: {name}")
            continue

    try:
        shift = Shift.objects.create(
            employee=employee,
            day=row['Day'],
            start_time=datetime.strptime(row['Start'], "%H:%M").time(),
            end_time=datetime.strptime(row['End'], "%H:%M").time(),
            role=row['Role']
        )
        print(f"✅ Saved: {shift}")
    except Exception as e:
        print(f"❌ Error saving shift for {name}: {e}")

print("\n🎉 All done.")
