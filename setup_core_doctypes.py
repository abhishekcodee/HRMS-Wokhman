import os
import json
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='hrms', autocommit=True)
cur = conn.cursor(pymysql.cursors.DictCursor)

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

def create_table_for_doctype(doc_path):
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except Exception:
        return
    if not isinstance(meta, dict) or meta.get('doctype') != 'DocType' or not meta.get('name'):
        return
    if meta.get('issingle'):
        return
    
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
    seen = {'name', 'creation', 'modified', 'modified_by', 'owner', 'docstatus', 'parent', 'parentfield', 'parenttype', 'idx'}
    for fld in fields:
        fname = fld.get('fieldname')
        ftype = fld.get('fieldtype')
        if not fname or fname in seen or ftype in ['Section Break', 'Column Break', 'Tab Break', 'HTML', 'Table', 'Table MultiSelect', 'Fold']:
            continue
        seen.add(fname)
        col_type = FIELD_MAP.get(ftype, 'varchar(255)')
        cols.append(f'`{fname}` {col_type} DEFAULT NULL')

    sql = f"CREATE TABLE IF NOT EXISTS `{tbl_name}` (\n  " + ",\n  ".join(cols) + ",\n  PRIMARY KEY (`name`)\n) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
    try:
        cur.execute(sql)
    except Exception as e:
        print(f"Error creating table {tbl_name}: {e}")

print("Scanning for DocTypes to create tables...")
created_count = 0
for base in [r'c:\HRMS-1\frappe\frappe\core', r'c:\HRMS-1\frappe\frappe\desk', r'c:\HRMS-1\frappe\frappe\workflow', r'c:\HRMS-1\frappe\frappe\custom']:
    if os.path.exists(base):
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.endswith('.json'):
                    create_table_for_doctype(os.path.join(root, file))
                    created_count += 1

print(f"Processed {created_count} DocTypes for core tables.")
