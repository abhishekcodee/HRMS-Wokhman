import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='hrms', autocommit=True)
cur = conn.cursor()

def get_table_cols(table):
    cur.execute(f"DESCRIBE `{table}`")
    return {r[0] for r in cur.fetchall()}

def seed_safe(table, records):
    cols_in_table = get_table_cols(table)
    for rec in records:
        valid_data = {k: v for k, v in rec.items() if k in cols_in_table}
        cols = list(valid_data.keys())
        vals = list(valid_data.values())
        placeholders = ", ".join(["%s"] * len(cols))
        col_names = ", ".join([f"`{c}`" for c in cols])
        sql = f"REPLACE INTO `{table}` ({col_names}) VALUES ({placeholders})"
        cur.execute(sql, tuple(vals))
    print(f"Seeded {len(records)} records into {table}.")

seed_safe("tabLeave Type", [
    {"name": "Casual Leave", "leave_type_name": "Casual Leave", "is_carry_forward": 0},
    {"name": "Sick Leave", "leave_type_name": "Sick Leave", "is_carry_forward": 0},
    {"name": "Privilege Leave", "leave_type_name": "Privilege Leave", "is_carry_forward": 1},
    {"name": "Compensatory Off", "leave_type_name": "Compensatory Off", "is_carry_forward": 0},
])

seed_safe("tabExpense Claim Type", [
    {"name": "Travel"},
    {"name": "Food & Meals"},
    {"name": "Medical"},
    {"name": "Office Supplies"},
    {"name": "Telephone & Internet"},
])

seed_safe("tabShift Type", [
    {"name": "Day Shift", "start_time": "09:00:00", "end_time": "18:00:00", "enable_auto_attendance": 1},
    {"name": "Evening Shift", "start_time": "14:00:00", "end_time": "22:00:00", "enable_auto_attendance": 1},
    {"name": "Night Shift", "start_time": "22:00:00", "end_time": "06:00:00", "enable_auto_attendance": 1},
])

seed_safe("tabDepartment", [
    {"name": "Engineering", "department_name": "Engineering", "company": "My Company"},
    {"name": "Human Resources", "department_name": "Human Resources", "company": "My Company"},
    {"name": "Finance", "department_name": "Finance", "company": "My Company"},
    {"name": "Operations", "department_name": "Operations", "company": "My Company"},
])

seed_safe("tabDesignation", [
    {"name": "Software Engineer", "designation_name": "Software Engineer"},
    {"name": "HR Manager", "designation_name": "HR Manager"},
    {"name": "Financial Analyst", "designation_name": "Financial Analyst"},
    {"name": "Administrator", "designation_name": "Administrator"},
])

print("All master tables seeded successfully!")
