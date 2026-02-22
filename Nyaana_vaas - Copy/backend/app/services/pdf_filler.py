"""
PDFFiller: fills static (scanned/non-fillable) PDF correction forms
by rendering each page as a high-resolution image and overlaying
user-supplied text using fpdf2.

Dependencies: pypdfium2, fpdf2, Pillow (all present in venv)
"""

import os
import uuid
import logging
import tempfile
from typing import Dict, Any

import pypdfium2 as pdfium
from fpdf import FPDF

from .form_definitions import FORM_FIELDS

logger = logging.getLogger(__name__)

# Paths to the original blank forms
FORM_TEMPLATES = {
    "aadhaar": os.path.join(os.path.dirname(__file__), "..", "data", "aadhar_correction.pdf"),
    "dl":      os.path.join(os.path.dirname(__file__), "..", "data", "DL_correction.pdf"),
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "generated_forms")


class PDFFiller:
    """
    Fills a blank correction PDF by:
      1. Rendering each page at 3x scale (≈ 216 DPI) via pypdfium2
      2. Using that render as the A4 background in an fpdf2 PDF
      3. Overlaying user text at calibrated (x, y) positions in mm
      4. Saving the result to OUTPUT_DIR and returning the file path
    """

    def fill(self, form_type: str, field_data: Dict[str, Any]) -> str:
        """
        Args:
            form_type:  "aadhaar" or "dl"
            field_data: dict mapping field id → user-supplied value

        Returns:
            Absolute path to the generated filled PDF
        """
        template_path = os.path.normpath(FORM_TEMPLATES[form_type])
        fields        = FORM_FIELDS[form_type]

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        src_pdf = pdfium.PdfDocument(template_path)
        out_pdf = FPDF(unit="mm", format="A4")
        out_pdf.set_auto_page_break(False)

        tmp_images = []

        try:
            for page_idx in range(len(src_pdf)):
                page   = src_pdf[page_idx]
                # Render at 3x scale → ~216 DPI, sufficient for print quality
                bitmap = page.render(scale=3)
                pil_img = bitmap.to_pil()

                # Save temp image
                tmp_path = os.path.join(tempfile.gettempdir(), f"civia_form_{page_idx}_{uuid.uuid4().hex[:6]}.png")
                pil_img.save(tmp_path, "PNG")
                tmp_images.append(tmp_path)

                # New PDF page — A4 full bleed
                out_pdf.add_page()
                out_pdf.image(tmp_path, x=0, y=0, w=210, h=297)

                # Overlay user text for fields on this page
                out_pdf.set_font("Helvetica", size=9)
                out_pdf.set_text_color(0, 50, 200)  # Bright blue ink

                for field in fields:
                    if field["page"] != page_idx:
                        continue
                    
                    value = str(field_data.get(field["id"], "")).strip()
                    if not value or value.lower() in ("skip", "none", "n/a", "-"):
                        continue

                    f_type = field.get("type", "text")
                    
                    if f_type == "checkbox":
                        # If the value matches one of the options, draw a tick in that option's box
                        options = field.get("options", {})
                        matched_option = None
                        for opt_key in options:
                            if opt_key.lower() in value.lower() or value.lower() in opt_key.lower():
                                matched_option = opt_key
                                break
                        
                        if matched_option:
                            opt = options[matched_option]
                            out_pdf.set_xy(opt["x"], opt["y"] - 0.5) # Centering adjustment
                            out_pdf.set_font("Helvetica", style="B", size=13) # Nice big Bold X
                            out_pdf.cell(w=4, h=4, txt="X", ln=False, align="C")
                            out_pdf.set_font("Helvetica", style="", size=9)
                    
                    elif f_type == "boxed":
                        box_w = field.get("box_width", 5.0)
                        start_x = field["x"]
                        out_pdf.set_font("Courier", style="B", size=11)
                        clean_val = "".join(filter(str.isalnum, value))
                        for i, char in enumerate(clean_val):
                            if i >= field.get("char_count", 99): break
                            out_pdf.set_xy(start_x + (i * box_w), field["y"] + 0.5) # Shift down
                            out_pdf.cell(w=box_w, h=5, txt=char, ln=False, align="C")
                        out_pdf.set_font("Helvetica", style="", size=9)

                    elif f_type == "boxed_date":
                        clean_date = "".join(filter(str.isdigit, value))
                        if len(clean_date) == 8:
                            box_w = 4.86
                            start_x = field["x"]
                            out_pdf.set_font("Courier", style="B", size=11)
                            # DD
                            for i in range(2):
                                out_pdf.set_xy(start_x + (i * box_w), field["y"] + 0.5)
                                out_pdf.cell(w=box_w, h=5, txt=clean_date[i], ln=False, align="C")
                            # MM (skip gap of '/')
                            for i in range(2, 4):
                                out_pdf.set_xy(start_x + (i * box_w) + 1.5, field["y"] + 0.5) 
                                out_pdf.cell(w=box_w, h=5, txt=clean_date[i], ln=False, align="C")
                            # YYYY (skip gap of '/')
                            for i in range(4, 8):
                                out_pdf.set_xy(start_x + (i * box_w) + 3.0, field["y"] + 0.5)
                                out_pdf.cell(w=box_w, h=5, txt=clean_date[i], ln=False, align="C")
                            out_pdf.set_font("Helvetica", style="", size=9)
                    
                    else:
                        # Standard text
                        out_pdf.set_xy(field["x"], field["y"])
                        # Truncate to avoid overflow
                        out_pdf.cell(w=0, h=4, txt=value[:100], ln=False)

        finally:
            # Clean up temp images
            for p in tmp_images:
                try:
                    os.remove(p)
                except OSError:
                    pass

        # Write output file
        out_filename = f"{form_type}_correction_{uuid.uuid4().hex[:10]}.pdf"
        out_path     = os.path.join(OUTPUT_DIR, out_filename)
        out_pdf.output(out_path)

        logger.info(f"[PDFFiller] Generated form: {out_path}")
        return out_path


# Singleton for use in the pipeline
pdf_filler = PDFFiller()
