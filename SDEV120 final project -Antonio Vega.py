import pandas as pd

employee_db = pd.read_excel("Payroll_Template_Updated.xlsx", sheet_name="Employee Demographics")

hours_worked = pd.read_excel("Payroll_Template_Updated.xlsx", sheet_name="Hours Worked")


payroll = pd.merge(hours_worked, employee_db, on="Employee ID")


def calculate_gross(hours, rate):
    if hours <= 40:
        return hours * rate
    else:
        return 40 * rate + (hours - 40) * rate * 1.5


payroll["Gross Pay"] = payroll.apply(lambda row: calculate_gross(row["Regular Hours"], row["Hourly Rate"]), axis=1)
payroll["State Tax (5.6%)"] = payroll["Gross Pay"] * 0.056
payroll["Federal Tax (7.9%)"] = payroll["Gross Pay"] * 0.079
payroll["Pre-Tax Amount"] = payroll["Gross Pay"]
payroll["Net Pay"] = payroll["Gross Pay"] - payroll["State Tax (5.6%)"] - payroll["Federal Tax (7.9%)"]

results = payroll[[
    "Employee ID", "First Name", "Last Name", "Dependents",
    "Regular Hours", "Hourly Rate", "Gross Pay",
    "State Tax (5.6%)", "Federal Tax (7.9%)", "Pre-Tax Amount", "Net Pay"
]]

with pd.ExcelWriter("Payroll_Results.xlsx", engine="openpyxl") as writer:
    results.to_excel(writer, sheet_name="Payroll Calculations", index=False)

print("Payroll calculations completed and saved to 'Payroll_Results.xlsx'")
