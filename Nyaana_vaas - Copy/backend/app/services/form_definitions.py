"""
Form field definitions for Aadhaar Correction and Driving Licence Correction forms.

Each field entry:
  id       - unique key used to store the collected value
  label    - question shown to the user
  page     - 0-indexed PDF page number this field belongs to
  x, y     - position in mm from top-left on A4 page where text is placed
  required - whether the field must be answered (False = optional, can be skipped)
"""

AADHAAR_FIELDS = [
    # ── Section 2.1: Fields for Correction (Checkboxes) ───────────────────────
    {
        "id": "fields_to_update",
        "label": "Which information do you want to update? (e.g., Name, Address, Mobile, Date of Birth)",
        "page": 0, "x": 60, "y": 72, "required": True,
        "type": "checkbox",
        "options": {
            "Biometric": {"x": 28.5, "y": 72.5},
            "Mobile": {"x": 75.5, "y": 72.5},
            "Date of Birth": {"x": 98.5, "y": 72.5},
            "Address": {"x": 121.5, "y": 72.5},
            "Name": {"x": 141.5, "y": 72.5},
            "Gender": {"x": 160.5, "y": 72.5},
            "Email": {"x": 178.5, "y": 72.5},
        }
    },
    # ── Section 2: Aadhaar Number ─────────────────────────────────────────────
    {
        "id": "aadhaar_number",
        "label": "Your existing 12-digit Aadhaar number (e.g., 1234 5678 9012)",
        "page": 0, "x": 122.2, "y": 62, "required": True,
        "type": "boxed", "box_width": 4.88, "char_count": 12
    },
    # ── Section 3: Full Name ──────────────────────────────────────────────────
    {
        "id": "resident_name",
        "label": "Your full name as it should appear on Aadhaar (e.g., Rohan Sreejith)",
        "page": 0, "x": 60, "y": 78.5, "required": True,
    },
    # ── Section 4: Gender ─────────────────────────────────────────────────────
    {
        "id": "gender",
        "label": "Gender (Male / Female / Transgender)",
        "page": 0, "x": 60, "y": 84, "required": True,
        "type": "checkbox",
        "options": {
            "Male": {"x": 33.5, "y": 85},
            "Female": {"x": 46.5, "y": 85},
            "Transgender": {"x": 61.5, "y": 85}
        }
    },
    # ── Section 5: Date of Birth ──────────────────────────────────────────────
    {
        "id": "dob",
        "label": "Date of birth in DD/MM/YYYY format (e.g., 15/08/1990)",
        "page": 0, "x": 162.5, "y": 84, "required": True,
        "type": "boxed_date"
    },
    # ── Section 6: Address (Two-Column Layout) ────────────────────────────────
    {
        "id": "address_line1",
        "label": "House, Building, or Apartment number (e.g., Flat 101, B-Block)",
        "page": 0, "x": 45, "y": 110, "required": True,
    },
    {
        "id": "address_line2",
        "label": "Street, Road, or Lane name (e.g., MG Road, Baker Street)",
        "page": 0, "x": 125, "y": 110, "required": False,
    },
    {
        "id": "landmark",
        "label": "Nearby landmark (optional - e.g., Near City Hospital)",
        "page": 0, "x": 45, "y": 118, "required": False,
    },
    {
        "id": "area",
        "label": "Area, Locality, or Sector (e.g., Koramangala 4th Block)",
        "page": 0, "x": 125, "y": 118, "required": False,
    },
    {
        "id": "city",
        "label": "Village, Town, or City name (e.g., Trivandrum, Kochi)",
        "page": 0, "x": 45, "y": 124.5, "required": True,
    },
    {
        "id": "post_office",
        "label": "Registered Post Office (e.g., GPO, Pattom SO)",
        "page": 0, "x": 125, "y": 124.5, "required": True,
    },
    {
        "id": "district",
        "label": "District (e.g., Thiruvananthapuram, Ernakulam)",
        "page": 0, "x": 45, "y": 133.5, "required": True,
    },
    {
        "id": "state",
        "label": "State (e.g., Kerala, Tamil Nadu)",
        "page": 0, "x": 125, "y": 133.5, "required": True,
    },
    {
        "id": "email",
        "label": "Email address (e.g., name@example.com)",
        "page": 0, "x": 45, "y": 141, "required": False,
    },
    {
        "id": "mobile",
        "label": "Your 10-digit mobile number (e.g., 9876543210)",
        "page": 0, "x": 118.5, "y": 141, "required": True,
        "type": "boxed", "box_width": 4.88, "char_count": 10
    },
    {
        "id": "pincode",
        "label": "6-digit PIN Code (e.g., 695001)",
        "page": 0, "x": 174.5, "y": 141, "required": True,
        "type": "boxed", "box_width": 4.88, "char_count": 6
    },
    # ── Section 8: Reason for Correction ──────────────────────────────────────
    {
        "id": "correction_reason",
        "label": "Reason for correction (e.g., Spelling mistake in name)",
        "page": 0, "x": 130, "y": 178, "required": True,
    },
    # ── Section 8: Supporting Documents ──────────────────────────────────────
    {
        "id": "documents_enclosed",
        "label": "Documents attached for proof (e.g., Passport, Voter ID, PAN)",
        "page": 0, "x": 45, "y": 168.5, "required": True,
    },
    # ── Section 9: Declaration ────────────────────────────────────────────────
    {
        "id": "place",
        "label": "Place of declaration (e.g., Chennai, Mumbai)",
        "page": 0, "x": 30, "y": 240, "required": True,
    },
    {
        "id": "date",
        "label": "Today's date (DD/MM/YYYY)",
        "page": 0, "x": 160, "y": 240, "required": True,
    },
]

DL_FIELDS = [
    # ── Applicant Details ──────────────────────────────────────────────────────
    {
        "id": "applicant_name",
        "label": "Full name as it appears on your existing Driving Licence",
        "page": 0, "x": 70, "y": 66, "required": True,
    },
    {
        "id": "dl_number",
        "label": "Existing Driving Licence number (e.g. KA01-20200012345)",
        "page": 0, "x": 70, "y": 78, "required": True,
    },
    {
        "id": "dob",
        "label": "Date of birth as on DL (DD/MM/YYYY)",
        "page": 0, "x": 70, "y": 90, "required": True,
    },
    {
        "id": "father_husband_name",
        "label": "Father's / Husband's / Wife's full name",
        "page": 0, "x": 70, "y": 102, "required": True,
    },
    {
        "id": "mobile",
        "label": "Mobile number",
        "page": 0, "x": 70, "y": 114, "required": True,
    },
    {
        "id": "email",
        "label": "Email address (optional — press Enter to skip)",
        "page": 0, "x": 70, "y": 126, "required": False,
    },
    # ── Address ────────────────────────────────────────────────────────────────
    {
        "id": "address_line1",
        "label": "Current address — House/Flat number and Street name",
        "page": 0, "x": 70, "y": 142, "required": True,
    },
    {
        "id": "address_line2",
        "label": "Address — Area / Landmark (optional)",
        "page": 0, "x": 70, "y": 152, "required": False,
    },
    {
        "id": "city",
        "label": "City / Town",
        "page": 0, "x": 70, "y": 162, "required": True,
    },
    {
        "id": "state",
        "label": "State",
        "page": 0, "x": 140, "y": 162, "required": True,
    },
    {
        "id": "pincode",
        "label": "PIN Code (6 digits)",
        "page": 0, "x": 70, "y": 172, "required": True,
    },
    # ── Licence Details ────────────────────────────────────────────────────────
    {
        "id": "rto_name",
        "label": "Name of RTO (Regional Transport Office) that issued your DL",
        "page": 0, "x": 70, "y": 188, "required": True,
    },
    {
        "id": "vehicle_class",
        "label": "Vehicle class(es) on your DL (e.g. LMV, MCWG, Transport)",
        "page": 0, "x": 70, "y": 200, "required": True,
    },
    {
        "id": "dl_validity",
        "label": "DL validity date as shown on your licence (DD/MM/YYYY)",
        "page": 0, "x": 70, "y": 212, "required": True,
    },
    # ── Correction Details ─────────────────────────────────────────────────────
    {
        "id": "correction_fields",
        "label": "Which details need correction? (e.g. Name, Address, Date of Birth, Photo)",
        "page": 0, "x": 70, "y": 228, "required": True,
    },
    {
        "id": "correction_reason",
        "label": "Brief reason for correction (e.g. Typographical error, Address change)",
        "page": 0, "x": 70, "y": 240, "required": True,
    },
    {
        "id": "documents_enclosed",
        "label": "Documents you will attach (e.g. Aadhaar, Passport, address proof, passport photo)",
        "page": 0, "x": 70, "y": 252, "required": True,
    },
    # ── Declaration ────────────────────────────────────────────────────────────
    {
        "id": "place",
        "label": "Place (city where you are signing this form)",
        "page": 0, "x": 70, "y": 270, "required": True,
    },
    {
        "id": "date",
        "label": "Today's date (DD/MM/YYYY)",
        "page": 0, "x": 140, "y": 270, "required": True,
    },
]

FORM_FIELDS = {
    "aadhaar": AADHAAR_FIELDS,
    "dl": DL_FIELDS,
}

FORM_LABELS = {
    "aadhaar": "Aadhaar Correction Form",
    "dl": "Driving Licence Correction Form",
}

POST_SUBMISSION_INSTRUCTIONS = {
    "aadhaar": (
        "**What to do with your filled Aadhaar Correction Form:**\n"
        "1. Print the form on A4 paper.\n"
        "2. Affix a recent passport-size photograph in the given space.\n"
        "3. Attach self-attested copies of: Proof of Identity (POI), Proof of Address (POA), and Proof of Date of Birth (POB) if applicable.\n"
        "4. Sign the form in the designated signature box.\n"
        "5. Visit your nearest **Aadhaar Enrolment/Update Centre** (book a slot free at appointments.uidai.gov.in).\n"
        "6. Submit the form along with originals of supporting documents for verification.\n"
        "7. **The correction service is completely FREE of charge.** Insist on a receipt/acknowledgement slip.\n"
        "8. Track correction status at: https://myaadhaar.uidai.gov.in"
    ),
    "dl": (
        "**What to do with your filled Driving Licence Correction Form:**\n"
        "1. Print the form on A4 paper.\n"
        "2. Attach: self-attested copy of existing DL, one recent passport-size photo, address proof (Aadhaar/Passport/Voter ID).\n"
        "3. Sign the declaration section of the form.\n"
        "4. Take the form + documents to your **issuing RTO (Regional Transport Office)**.\n"
        "5. Pay the applicable fee (usually ₹200–₹500 depending on your state).\n"
        "6. Collect the acknowledgement receipt — you may need it to track the corrected DL delivery.\n"
        "7. Alternatively, many states allow DL corrections via the **Sarathi Parivahan portal**: https://sarathi.parivahan.gov.in"
    ),
}
