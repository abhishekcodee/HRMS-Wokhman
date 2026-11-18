import json
import os
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='hrms')
cur = conn.cursor()

FIELD_MAP = {
    'Data': 'varchar(140)', 'Select': 'varchar(140)', 'Link': 'varchar(140)',
    'Dynamic Link': 'varchar(140)', 'Date': 'date', 'Datetime': 'datetime(6)',
    'Time': 'time(6)', 'Int': 'int(11)', 'Check': 'tinyint(4)',
    'Float': 'decimal(21,9)', 'Currency': 'decimal(21,9)', 'Percent': 'decimal(21,9)',
    'Rating': 'decimal(3,2)', 'Duration': 'decimal(21,9)', 'Small Text': 'text',
    'Long Text': 'longtext', 'Text Editor': 'longtext', 'Code': 'longtext',
    'Attach': 'text', 'Attach Image': 'text', 'Text': 'text', 'Read Only': 'varchar(255)',
    'Password': 'text', 'Signature': 'longtext', 'Color': 'varchar(255)',
    'Barcode': 'text', 'Geolocation': 'text', 'JSON': 'json', 'Phone': 'varchar(255)',
    'Autocomplete': 'varchar(255)'
}

doctypes_to_create = [
    r'c:\HRMS-1\erpnext\erpnext\setup\doctype\employee\employee.json',
    r'c:\HRMS-1\erpnext\erpnext\setup\doctype\company\company.json',
    r'c:\HRMS-1\erpnext\erpnext\setup\doctype\department\department.json',
    r'c:\HRMS-1\erpnext\erpnext\setup\doctype\designation\designation.json',
    r'c:\HRMS-1\erpnext\erpnext\setup\doctype\holiday_list\holiday_list.json',
    r'c:\HRMS-1\erpnext\erpnext\setup\doctype\holiday_list\holiday.json',
    r'c:\HRMS-1\frappe\frappe\core\doctype\user\user.json',
    r'c:\HRMS-1\frappe\frappe\core\doctype\role\role.json',
    r'c:\HRMS-1\frappe\frappe\core\doctype\has_role\has_role.json',
    r'c:\HRMS-1\frappe\frappe\core\doctype\system_settings\system_settings.json',
]

for doc_path in doctypes_to_create:
    if not os.path.exists(doc_path):
        print(f"Skipping not found: {doc_path}")
        continue
    with open(doc_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    dt_name = meta.get('name')
    tbl_name = f'tab{dt_name}'
    fields = meta.get('fields', [])
    cols = [
        '`name` varchar(255) NOT NULL',
        '`creation` datetime(6) DEFAULT CURRENT_TIMESTAMP(6)',
        '`modified` datetime(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)',
        '`modified_by` varchar(255) DEFAULT "Administrator"',
        '`owner` varchar(255) DEFAULT "Administrator"',
        '`docstatus` tinyint(4) NOT NULL DEFAULT 0',
        '`parent` varchar(255) DEFAULT NULL',
        '`parentfield` varchar(255) DEFAULT NULL',
        '`parenttype` varchar(255) DEFAULT NULL',
        '`idx` int(11) NOT NULL DEFAULT 0'
    ]
    for fld in fields:
        fname = fld.get('fieldname')
        ftype = fld.get('fieldtype')
        if not fname or ftype in ['Section Break', 'Column Break', 'Tab Break', 'HTML', 'Table', 'Table MultiSelect']:
            continue
        col_type = FIELD_MAP.get(ftype, 'varchar(255)')
        cols.append(f'`{fname}` {col_type} DEFAULT NULL')
    cols.append('PRIMARY KEY (`name`)')
    sql = f'CREATE TABLE IF NOT EXISTS `{tbl_name}` (\n  ' + ',\n  '.join(cols) + '\n) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;'
    try:
        cur.execute(sql)
        print(f'Created table: {tbl_name}')
    except Exception as e:
        print(f'Error creating {tbl_name}: {e}')

# Insert default Administrator user and Guest user
cur.execute("REPLACE INTO `tabUser` (`name`, `email`, `first_name`, `enabled`, `user_type`) VALUES ('Administrator', 'admin@example.com', 'Administrator', 1, 'System User')")
cur.execute("REPLACE INTO `tabUser` (`name`, `email`, `first_name`, `enabled`, `user_type`) VALUES ('Guest', 'guest@example.com', 'Guest', 1, 'Website User')")

# Insert default company
cur.execute("REPLACE INTO `tabCompany` (`name`, `company_name`, `default_currency`, `country`) VALUES ('My Company', 'My Company', 'USD', 'United States')")

conn.commit()
conn.close()
print("All base tables created successfully!")

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='hrms')
cur = conn.cursor()
cur.execute("REPLACE INTO `tabEmployee` (`name`, `first_name`, `employee_name`, `user_id`, `company`, `status`) VALUES ('HR-EMP-00001', 'Abhishek', 'Abhishek', 'admin@example.com', 'My Company', 'Active')")
conn.commit()
conn.close()
print("Employee HR-EMP-00001 created successfully!")
