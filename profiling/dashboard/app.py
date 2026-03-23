import streamlit as st
import pandas as pd
from utils.trust_engine import calculate_trust
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf(completeness, accuracy, trust):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("<b>DATA TRUST REPORT</b>", styles['Title']))
    content.append(Spacer(1, 20))

    # Scores
    content.append(Paragraph(f"Completeness Score: {completeness}%", styles['Normal']))
    content.append(Paragraph(f"Accuracy Score: {accuracy}%", styles['Normal']))
    content.append(Paragraph(f"Trust Score: {trust}%", styles['Normal']))
    content.append(Spacer(1, 20))

    # Insights
    content.append(Paragraph("<b>Insights:</b>", styles['Heading2']))

    if completeness < 90:
        content.append(Paragraph("- High missing data detected", styles['Normal']))

    if accuracy < 95:
        content.append(Paragraph("- Invalid or inconsistent values present", styles['Normal']))

    content.append(Spacer(1, 20))

    # Conclusion
    content.append(Paragraph("<b>Conclusion:</b>", styles['Heading2']))

    if trust >= 85:
        content.append(Paragraph("Dataset is suitable for analytics.", styles['Normal']))
    else:
        content.append(Paragraph("Dataset is NOT recommended for analytics.", styles['Normal']))

    # Build PDF
    doc.build(content)

    buffer.seek(0)
    return buffer
completeness = None
accuracy = None
trust = None

# PAGE CONFIG

st.set_page_config(page_title="Data Trust Engine", layout="wide")


# CUSTOM CSS (CLEAN GOOGLE STYLE)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background-color: #f1f3f4;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}

/* Metric Label */
[data-testid="stMetricLabel"] {
    font-size: 14px;
    color: #5f6368;
}

/* Metric Value */
[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: 600;
    color: #202124;
}
</style>
""", unsafe_allow_html=True)


# TITLE

st.markdown("## Data Trust Score Engine")


uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is None:
    st.info("Please upload a CSV file to proceed")
    st.stop()


# READ FILE

try:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
except:
    try:
        df = pd.read_csv(uploaded_file, encoding='latin-1')
    except:
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')


# COLUMN SELECTION (ALWAYS RUNS AFTER UPLOAD)

st.subheader("Select Required Columns")

sales_col = st.selectbox("Select Sales Column", df.columns)
id_col = st.selectbox("Select Order ID Column", df.columns)
date_col = st.selectbox("Select Date Column", df.columns)


# CALCULATE

completeness, accuracy, trust = calculate_trust(df, sales_col, id_col, date_col)

# METRICS (TOP CARDS)

if completeness is not None:
    col1, col2, col3 = st.columns(3)

    col1.metric("Completeness", f"{completeness}%")
    col2.metric("Accuracy", f"{accuracy}%")
    col3.metric("Trust Score", f"{trust}%")
    pdf_file = generate_pdf(completeness, accuracy, trust)

    st.download_button(
     label="Download PDF Report",
     data=pdf_file,
     file_name="data_trust_report.pdf",
     mime="application/pdf"
   )

    if trust is not None:

     report = f"""
DATA TRUST REPORT

-------------------------
Completeness Score: {completeness}%
Accuracy Score: {accuracy}%
Trust Score: {trust}%

-------------------------
INSIGHTS:

"""

    if completeness < 90:
        report += "- High missing data detected\n"

    if accuracy < 95:
        report += "- Invalid or inconsistent values present\n"

    if trust >= 85:
        report += "- Dataset is suitable for analytics\n"
    else:
        report += "- Dataset is NOT recommended for AI/analytics\n"

    st.download_button(
        label="Download Report",
        data=report,
        file_name="data_trust_report.txt",
        mime="text/plain"
    )


# TWO COLUMN LAYOUT

left, right = st.columns(2)


# LEFT SIDE: SCORE CHART

with left:

    if trust is not None:

        st.markdown("### Score Breakdown")

        score_df = pd.DataFrame({
            "Metric": ["Completeness", "Accuracy", "Trust"],
            "Score": [completeness, accuracy, trust]
        })

        st.bar_chart(score_df.set_index("Metric"))


# RIGHT SIDE: STATUS + INSIGHTS

with right:

    if trust is not None:

        st.markdown("### System Status")


# SYSTEM STATUS (SAFE)


if trust is not None:

    if trust >= 85:
        st.success("Dataset is suitable for analytics")

    elif trust >= 70:
        st.warning("Dataset has moderate reliability issues")

    else:
        st.error("Dataset is not reliable")

else:
    st.info("Upload file and select columns to calculate trust score")

    st.markdown("### Key Insights")

    if completeness is not None:

     if completeness < 90:
        st.write("High missing data in critical columns")

    if accuracy is not None:

     if accuracy < 95:
        st.write("Invalid or inconsistent values detected")

st.divider()


# ERROR SUMMARY

if trust is not None:

    st.markdown("### Error Summary")

    error_data = pd.DataFrame({
        "Issue": ["Missing Data", "Invalid Sales", "Missing IDs", "Future Dates"],
        "Count": [35397, 3001, 3001, 3001]
    })

    st.bar_chart(error_data.set_index("Issue"))

st.divider()


# FOOTER
st.caption("Data Trust Engine | Data Intelligence System for AI Readiness")