from collections.abc import Generator

import requests

import frappe
from frappe.utils import add_days, date_diff

country_info = {}


@frappe.whitelist(allow_guest=True)
def get_country(fields: list | None = None) -> dict:
	global country_info
	ip = frappe.local.request_ip

	if ip not in country_info:
		# Sovereign fallback: use system configured country without transmitting IP to external IP-API services
		default_country = frappe.db.get_default("country") or ""
		country_info[ip] = {
			"countryCode": default_country[:2].upper() if default_country else "",
			"country": default_country,
			"regionName": "",
			"city": "",
		}

	return country_info[ip]


def get_date_range(start_date: str, end_date: str) -> list[str]:
	"""returns list of dates between start and end dates"""
	no_of_days = date_diff(end_date, start_date) + 1
	return [add_days(start_date, i) for i in range(no_of_days)]


def generate_date_range(start_date: str, end_date: str, reverse: bool = False) -> Generator[str, None, None]:
	no_of_days = date_diff(end_date, start_date) + 1

	date_field = end_date if reverse else start_date
	direction = -1 if reverse else 1

	for n in range(no_of_days):
		yield add_days(date_field, direction * n)


def get_employee_email(employee_id: str) -> str | None:
	employee_emails = frappe.db.get_value(
		"Employee",
		employee_id,
		["prefered_email", "user_id", "company_email", "personal_email"],
		as_dict=True,
	)

	return (
		employee_emails.prefered_email
		or employee_emails.user_id
		or employee_emails.company_email
		or employee_emails.personal_email
	)


def extend_bootinfo(bootinfo):
	bootinfo.hr_only_setup = bool(frappe.conf.sk_hrms)
