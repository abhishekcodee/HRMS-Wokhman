import datetime
import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="hrms",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

departments = [
    {"name": "All Departments", "department_name": "All Departments", "parent_department": None, "company": "My Company", "is_group": 1, "disabled": 0},
    {"name": "Accounts - W", "department_name": "Accounts", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Marketing - W", "department_name": "Marketing", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Sales - W", "department_name": "Sales", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Purchase - W", "department_name": "Purchase", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Operations - W", "department_name": "Operations", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Production - W", "department_name": "Production", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Dispatch - W", "department_name": "Dispatch", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Customer Service - W", "department_name": "Customer Service", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Human Resources - W", "department_name": "Human Resources", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Management - W", "department_name": "Management", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Quality Management - W", "department_name": "Quality Management", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Research & Development - W", "department_name": "Research & Development", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0},
    {"name": "Legal - W", "department_name": "Legal", "parent_department": "All Departments", "company": "My Company", "is_group": 0, "disabled": 0}
]

designations = [
    {"name": "Chief Executive Officer", "designation_name": "Chief Executive Officer", "description": "Top executive responsible for overall operations"},
    {"name": "Operations Manager", "designation_name": "Operations Manager", "description": "Oversees day-to-day operations and logistics"},
    {"name": "HR Manager", "designation_name": "HR Manager", "description": "Leads recruitment, culture, and employee welfare"},
    {"name": "Software Engineer", "designation_name": "Software Engineer", "description": "Develops and maintains core applications"},
    {"name": "Sales Lead", "designation_name": "Sales Lead", "description": "Drives client acquisition and revenue growth"},
    {"name": "Finance Specialist", "designation_name": "Finance Specialist", "description": "Manages payroll, invoices, and accounting audits"},
    {"name": "Quality Assurance Specialist", "designation_name": "Quality Assurance Specialist", "description": "Ensures product reliability and quality control"},
    {"name": "Research Analyst", "designation_name": "Research Analyst", "description": "Conducts competitive and domain research"}
]

branches = [
    {"name": "Headquarters", "branch": "Headquarters"},
    {"name": "West Coast Office", "branch": "West Coast Office"},
    {"name": "Regional Tech Hub", "branch": "Regional Tech Hub"}
]

holiday_lists = [
    {"name": "Standard Holidays 2026", "holiday_list_name": "Standard Holidays 2026", "from_date": "2026-01-01", "to_date": "2026-12-31", "weekly_off": "Sunday"}
]

with conn.cursor() as cur:
    for d in departments:
        cur.execute(
            """REPLACE INTO `tabDepartment` (name, creation, modified, modified_by, owner, docstatus, department_name, parent_department, company, is_group, disabled)
               VALUES (%s, %s, %s, 'Administrator', 'Administrator', 0, %s, %s, %s, %s, %s)""",
            (d["name"], now, now, d["department_name"], d["parent_department"], d["company"], d["is_group"], d["disabled"])
        )
    for d in designations:
        cur.execute(
            """REPLACE INTO `tabDesignation` (name, creation, modified, modified_by, owner, docstatus, designation_name, description)
               VALUES (%s, %s, %s, 'Administrator', 'Administrator', 0, %s, %s)""",
            (d["name"], now, now, d["designation_name"], d["description"])
        )
    for b in branches:
        try:
            cur.execute(
                """REPLACE INTO `tabBranch` (name, creation, modified, modified_by, owner, docstatus, branch)
                   VALUES (%s, %s, %s, 'Administrator', 'Administrator', 0, %s)""",
                (b["name"], now, now, b["branch"])
            )
        except Exception as e:
            pass
    for h in holiday_lists:
        try:
            cur.execute(
                """REPLACE INTO `tabHoliday List` (name, creation, modified, modified_by, owner, docstatus, holiday_list_name, from_date, to_date, weekly_off)
                   VALUES (%s, %s, %s, 'Administrator', 'Administrator', 0, %s, %s, %s, %s)""",
                (h["name"], now, now, h["holiday_list_name"], h["from_date"], h["to_date"], h["weekly_off"])
            )
        except Exception as e:
            pass

print("Successfully seeded departments, designations, branches, and holiday lists!")
conn.close()
