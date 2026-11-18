import os
import json
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='hrms', autocommit=True)
cur = conn.cursor(pymysql.cursors.DictCursor)

def get_cols(table):
    cur.execute(f"DESCRIBE `{table}`")
    return {r["Field"] for r in cur.fetchall()}

doctype_cols = get_cols("tabDocType")
docfield_cols = get_cols("tabDocField")

def import_doctype_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return
    if not isinstance(d, dict) or d.get("doctype") != "DocType" or not d.get("name"):
        return
    
    dt_name = d.get("name")
    
    # 1. Insert into tabDocType
    row = {k: v for k, v in d.items() if k in doctype_cols and not isinstance(v, (list, dict))}
    row["name"] = dt_name
    row["modified_by"] = "Administrator"
    row["owner"] = "Administrator"
    row["docstatus"] = 0
    
    c_keys = list(row.keys())
    c_vals = list(row.values())
    c_placeholders = ", ".join(["%s"] * len(c_keys))
    cur.execute(
        f"REPLACE INTO `tabDocType` ({', '.join([f'`{k}`' for k in c_keys])}) VALUES ({c_placeholders})",
        tuple(c_vals)
    )
    
    # 2. Insert fields into tabDocField
    fields = d.get("fields", [])
    for idx, fld in enumerate(fields):
        if not isinstance(fld, dict) or not fld.get("fieldname"):
            continue
        fname = fld.get("fieldname")
        field_row = {k: v for k, v in fld.items() if k in docfield_cols and not isinstance(v, (list, dict))}
        field_row["name"] = f"{dt_name}-{fname}"
        field_row["parent"] = dt_name
        field_row["parentfield"] = "fields"
        field_row["parenttype"] = "DocType"
        field_row["idx"] = idx + 1
        field_row["modified_by"] = "Administrator"
        field_row["owner"] = "Administrator"
        field_row["docstatus"] = 0
        
        fk = list(field_row.keys())
        fv = list(field_row.values())
        cur.execute(
            f"REPLACE INTO `tabDocField` ({', '.join([f'`{k}`' for k in fk])}) VALUES ({', '.join(['%s']*len(fk))})",
            tuple(fv)
        )

print("Populating tabDocType and tabDocField from JSON definitions...")
total = 0
for base in [r"c:\HRMS-1\frappe", r"c:\HRMS-1\erpnext", r"c:\HRMS-1\hrms"]:
    if os.path.exists(base):
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.endswith(".json"):
                    import_doctype_json(os.path.join(root, file))
                    total += 1

print(f"Completed importing {total} JSON definitions into tabDocType and tabDocField.")
