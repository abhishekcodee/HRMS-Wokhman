"""
Automated Private SMTP Email Setup for Self-Hosted Frappe HRMS.

Execute via Frappe Bench:
    bench --site <your-site-name> run-python /path/to/email_smtp_setup.py
"""

import frappe

# ================= PRIVATE SMTP SETTINGS =================
SMTP_SERVER = "smtp.yourcompany.local"    # Internal SMTP server (Exchange, Postfix, etc.)
SMTP_PORT = 587                          # 587 (TLS), 465 (SSL), or 25 (Internal relay)
USE_TLS = 1                              # 1 for TLS, 0 otherwise
USE_SSL = 0                              # 1 for SSL, 0 otherwise
EMAIL_ID = "hrms-notifications@yourcompany.local"
EMAIL_PASSWORD = "YourInternalSmtpPassword"
SENDER_NAME = "HR Department"
# ========================================================

def configure_private_smtp():
    frappe.init(site=frappe.local.site)
    frappe.connect()

    account_name = "Company HR Outgoing"
    if frappe.db.exists("Email Account", account_name):
        doc = frappe.get_doc("Email Account", account_name)
    else:
        doc = frappe.new_doc("Email Account")
        doc.email_account_name = account_name

    doc.email_id = EMAIL_ID
    doc.smtp_server = SMTP_SERVER
    doc.smtp_port = SMTP_PORT
    doc.use_tls = USE_TLS
    doc.use_ssl = USE_SSL
    doc.password = EMAIL_PASSWORD
    doc.enable_outgoing = 1
    doc.default_outgoing = 1
    doc.send_unsubscribe_message = 0
    doc.name_title = SENDER_NAME

    doc.save(ignore_permissions=True)
    frappe.db.commit()

    print(f"Successfully configured '{account_name}' as the default outgoing email server.")

if __name__ == "__main__":
    configure_private_smtp()
