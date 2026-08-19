import frappe
from urllib.parse import urlencode


@frappe.whitelist()
def send_onboarding_email(onboarding):

    doc = frappe.get_doc("Employee Onboarding", onboarding)

    recipient = doc.job_applicant

    if not recipient:
        frappe.throw("Employee email not found")

    params = {
        "reference_onboarding": doc.name,
        "job_applicant": doc.job_applicant or "",
        "job_offer": doc.job_offer or "",
        "company": doc.company or "",
        "date_of_joining": doc.date_of_joining or "",
        "onboarding_begins_on": doc.boarding_begins_on or "",
    }

    onboarding_link = (
        frappe.utils.get_url()
        + "/employee-onboarding-details-form/new?"
        + urlencode(params)
    )

    frappe.sendmail(
        recipients=[recipient],
        subject="Employee Onboarding Form",
        message=f"""
        Dear Candidate,<br><br>

        Welcome to NAFED.<br><br>

        Please complete your onboarding form using the link below:<br><br>

        <a href="{onboarding_link}">
            Complete Onboarding Form
        </a>

        <br><br>
        Regards,<br>
        HR Team
        """
    )

    return True