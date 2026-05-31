import io
import pandas as pd
from fpdf import FPDF
import datetime

def convert_df_to_csv(df):
    """
    Converts a pandas DataFrame to a CSV string.
    """
    return df.to_csv(index=False).encode('utf-8')

def create_pdf_report(title, df, summary=""):
    """
    Generates a PDF report containing a summary and data snapshot using fpdf2.
    """
    class PDF(FPDF):
        def header(self):
            self.set_font("helvetica", "B", 18)
            self.cell(0, 10, title, border=False, align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("helvetica", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf = PDF()
    pdf.add_page()
    
    # Timestamp
    pdf.set_font("helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Summary
    if summary:
        pdf.set_font("helvetica", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 8, summary)
        pdf.ln(10)
    
    # Data Table Snapshot
    if not df.empty:
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "Data Snapshot (Top 20 rows):", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        pdf.set_font("helvetica", "", 9)
        
        display_df = df.head(20).astype(str)
        cols = list(display_df.columns[:6]) # Display up to 6 columns safely
        
        with pdf.table(text_align="CENTER") as table:
            # Header
            header_row = table.row()
            for col_name in cols:
                header_row.cell(col_name)
                
            # Data rows
            for _, row in display_df.iterrows():
                data_row = table.row()
                for col_name in cols:
                    text = (row[col_name][:20] + '..') if len(row[col_name]) > 20 else row[col_name]
                    data_row.cell(text)

    return bytes(pdf.output())
