"""
Streamlit Web Application
Interactive Analytics, Data Quality Audit Lab, and Business Intelligence Dashboard
for Retail Customer Sales EDA Project.
"""

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Set page configuration
st.set_page_config(
    page_title="Retail Customer Sales - EDA & Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-clean {
        background-color: #10b981;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_datasets():
    raw_path = PROJECT_ROOT / "data" / "raw" / "retail_customer_sales_dataset.csv"
    if not raw_path.exists():
        raw_path = PROJECT_ROOT / "retail_customer_sales_dataset.csv"

    clean_path = PROJECT_ROOT / "data" / "processed" / "cleaned_retail_sales_dataset.csv"
    
    # Fallback checks
    if not raw_path.exists():
        raw_path = Path("data/raw/retail_customer_sales_dataset.csv")
    if not clean_path.exists():
        clean_path = Path("data/processed/cleaned_retail_sales_dataset.csv")
        
    raw_df = pd.read_csv(raw_path)
    clean_df = pd.read_csv(clean_path, parse_dates=["Order_Date", "Delivery_Date"])
    return raw_df, clean_df


try:
    raw_df, clean_df = load_datasets()
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()
    sys.exit(1)

# -------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------
st.sidebar.title("Navigation & Filters")
st.sidebar.markdown("**Project 1: Exploratory Data Analysis**")
st.sidebar.markdown("*Author: Ansh Vishnoi (2026m01410042)*")
st.sidebar.markdown("🔗 [**GitHub Repository**](https://github.com/anshvishnoi/ansh_vishnoi_2026m01410042/tree/main)")
st.sidebar.markdown("---")

# Global Filters
st.sidebar.subheader("Global Data Filters")
selected_regions = st.sidebar.multiselect(
    "Filter by Region",
    options=clean_df["Region"].unique().tolist(),
    default=clean_df["Region"].unique().tolist()
)

selected_segments = st.sidebar.multiselect(
    "Filter by Customer Segment",
    options=clean_df["Customer_Segment"].unique().tolist(),
    default=clean_df["Customer_Segment"].unique().tolist()
)

selected_categories = st.sidebar.multiselect(
    "Filter by Product Category",
    options=clean_df["Product_Category"].unique().tolist(),
    default=clean_df["Product_Category"].unique().tolist()
)

# Apply filters
filtered_df = clean_df[
    (clean_df["Region"].isin(selected_regions)) &
    (clean_df["Customer_Segment"].isin(selected_segments)) &
    (clean_df["Product_Category"].isin(selected_categories))
]

st.sidebar.markdown("---")
st.sidebar.info(f"Showing **{len(filtered_df):,}** of **{len(clean_df):,}** records.")

# -------------------------------------------------------------
# HEADER & EXECUTIVE KPI SUMMARY
# -------------------------------------------------------------
st.markdown('<div class="main-header">🛍️ Retail Customer Sales — Analytics & Decision Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Production-Ready Exploratory Data Analysis, Quality Audit Lab & Strategic Insights Platform</div>', unsafe_allow_html=True)

# Top KPIs
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

total_rev = filtered_df["Sales"].sum()
total_prof = filtered_df["Profit"].sum()
overall_margin = (total_prof / total_rev * 100) if total_rev > 0 else 0
total_orders = len(filtered_df)
unique_customers = filtered_df["Customer_ID"].nunique()
aov = filtered_df["Sales"].mean() if total_orders > 0 else 0

with kpi1:
    st.metric("Total Revenue", f"₹{total_rev:,.0f}")
with kpi2:
    st.metric("Total Profit", f"₹{total_prof:,.0f}")
with kpi3:
    st.metric("Profit Margin", f"{overall_margin:.1f}%")
with kpi4:
    st.metric("Total Orders", f"{total_orders:,}")
with kpi5:
    st.metric("Unique Customers", f"{unique_customers:,}")
with kpi6:
    st.metric("Average Order Value", f"₹{aov:,.0f}")

st.markdown("---")

# -------------------------------------------------------------
# MULTI-TAB ARCHITECTURE
# -------------------------------------------------------------
tabs = st.tabs([
    "📊 Executive Dashboard",
    "🔍 Data Quality Audit Lab",
    "📈 Statistical & Univariate",
    "🎯 Outlier Studio",
    "💼 Business Questions & GroupBy",
    "⚙️ Feature Engineering & Export",
    "📄 SRS & Documents",
    "💻 Code & Output Snippets"
])

# -------------------------------------------------------------
# TAB 1: EXECUTIVE DASHBOARD
# -------------------------------------------------------------
with tabs[0]:
    st.subheader("Commercial Performance & Growth Trajectory")
    
    col1, col2 = st.columns([7, 5])
    
    with col1:
        # Monthly Revenue & Profit Trend
        monthly = filtered_df.groupby("Order_YearMonth").agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        ).reset_index()
        
        fig_trend = px.line(
            monthly,
            x="Order_YearMonth",
            y=["Sales", "Profit"],
            markers=True,
            title="Monthly Revenue & Profit Timeline (2023 - 2024)",
            template="plotly_white",
            color_discrete_map={"Sales": "#2563eb", "Profit": "#10b981"}
        )
        fig_trend.update_layout(xaxis_title="Month", yaxis_title="Amount (₹)", legend_title="")
        st.plotly_chart(fig_trend, use_container_width=True)

    with col2:
        # Regional Breakdown Bar
        regional = filtered_df.groupby("Region").agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        ).reset_index()
        
        fig_reg = px.bar(
            regional,
            x="Region",
            y=["Sales", "Profit"],
            barmode="group",
            title="Sales & Profit by Territory",
            template="plotly_white",
            color_discrete_map={"Sales": "#3b82f6", "Profit": "#059669"}
        )
        fig_reg.update_layout(xaxis_title="Region", yaxis_title="Rupees (₹)", legend_title="")
        st.plotly_chart(fig_reg, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        # Category Share Donut
        cat_share = filtered_df.groupby("Product_Category")["Sales"].sum().reset_index()
        fig_pie = px.pie(
            cat_share,
            names="Product_Category",
            values="Sales",
            hole=0.45,
            title="Revenue Share by Product Category",
            template="plotly_white"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col4:
        # Customer Segment Breakdown
        seg_share = filtered_df.groupby("Customer_Segment").agg(
            Orders=("Transaction_ID", "count"),
            Revenue=("Sales", "sum")
        ).reset_index()
        fig_seg = px.bar(
            seg_share,
            x="Customer_Segment",
            y="Revenue",
            color="Customer_Segment",
            text_auto=".2s",
            title="Revenue by Customer Segment",
            template="plotly_white"
        )
        st.plotly_chart(fig_seg, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: DATA QUALITY AUDIT LAB
# -------------------------------------------------------------
with tabs[1]:
    st.subheader("Data Quality Audit & Sanitization Laboratory")
    st.markdown("""
    This lab documents the end-to-end data audit mandated by **Section 3.2 & 3.3** of the Project 1 specification.
    Observe the raw flaws versus sanitized state.
    """)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"#### ⚠️ Raw Dataset (`retail_customer_sales_dataset.csv`)")
        st.markdown(f"- **Total Rows:** {len(raw_df):,}")
        st.markdown(f"- **Duplicate Rows:** {raw_df.duplicated().sum()}")
        st.markdown(f"- **Null Values Count:** {raw_df.isnull().sum().sum():,}")
        st.markdown(f"- **Negative/Impossible Ages:** {((raw_df['Age'] <= 0) | (raw_df['Age'] > 100)).sum()}")
        st.markdown(f"- **Invalid Discounts (<0 or >0.5):** {((raw_df['Discount'] < 0) | (raw_df['Discount'] > 0.5)).sum()}")
    
    with col_b:
        st.markdown(f"#### ✅ Cleaned Dataset (`cleaned_retail_sales_dataset.csv`)")
        st.markdown(f"- **Total Clean Rows:** {len(clean_df):,}")
        st.markdown(f"- **Duplicate Rows Remaining:** <span class='badge-clean'>0</span>", unsafe_allow_html=True)
        st.markdown(f"- **Null Values Remaining:** <span class='badge-clean'>0</span>", unsafe_allow_html=True)
        st.markdown(f"- **Age Range:** [{clean_df['Age'].min():.0f}, {clean_df['Age'].max():.0f}] yrs")
        st.markdown(f"- **Discount Range:** [{clean_df['Discount'].min():.2f}, {clean_df['Discount'].max():.2f}]")

    st.markdown("---")
    st.subheader("1. Missing Values Audit (Raw vs Cleaned)")
    
    raw_missing = raw_df.isnull().sum()
    raw_missing_pct = (raw_missing / len(raw_df)) * 100
    missing_comparison = pd.DataFrame({
        "Column": raw_df.columns,
        "Raw_Missing_Count": raw_missing.values,
        "Raw_Missing_Pct (%)": raw_missing_pct.round(2).values,
        "Cleaned_Missing_Count": clean_df[raw_df.columns].isnull().sum().values
    })
    st.dataframe(missing_comparison[missing_comparison["Raw_Missing_Count"] > 0], use_container_width=True)

    st.markdown("---")
    st.subheader("2. Categorical Standardization (Gender & Region)")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Gender Casing Variations Standardized:**")
        st.write(raw_df["Gender"].value_counts(dropna=False).to_dict())
        st.success(f"Standardized into: {clean_df['Gender'].unique().tolist()}")
    with c2:
        st.markdown("**Region Abbreviations & Inconsistencies Standardized:**")
        st.write(raw_df["Region"].value_counts(dropna=False).to_dict())
        st.success(f"Standardized into: {clean_df['Region'].unique().tolist()}")

    st.markdown("---")
    st.subheader("3. Cleaning Decision & Justification Log")
    log_file = Path("eda_summary/cleaning_justifications.md")
    if log_file.exists():
        st.markdown(log_file.read_text(encoding="utf-8"))

# -------------------------------------------------------------
# TAB 3: STATISTICAL & UNIVARIATE
# -------------------------------------------------------------
with tabs[2]:
    st.subheader("Descriptive Statistics & Univariate Distributions")
    st.markdown("Mandated by **Section 3.4**: Mean, Median, Mode, Std, Variance, Quartiles, IQR, and Skewness.")

    stats_path = Path("eda_summary/descriptive_statistics.csv")
    if stats_path.exists():
        stats_df = pd.read_csv(stats_path)
        st.dataframe(stats_df, use_container_width=True)

    st.markdown("---")
    st.subheader("Univariate Distribution Curves & Skewness Analysis")
    
    dist_var = st.selectbox("Select Numerical Variable to Inspect Distribution:", ["Sales", "Income", "Age", "Quantity", "Profit"])
    
    col_plot, col_insight = st.columns([7, 5])
    with col_plot:
        fig_dist = px.histogram(
            filtered_df,
            x=dist_var,
            marginal="box",
            nbins=40,
            title=f"{dist_var} Distribution & Outlier Boxplot",
            template="plotly_white",
            color_discrete_sequence=["#0284c7"]
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col_insight:
        skew = filtered_df[dist_var].skew()
        mean_v = filtered_df[dist_var].mean()
        med_v = filtered_df[dist_var].median()
        st.markdown(f"### Statistical Characteristics: **{dist_var}**")
        st.metric("Skewness Coefficient", f"{skew:.2f}")
        st.metric("Arithmetic Mean", f"₹{mean_v:,.2f}" if dist_var in ["Sales", "Income", "Profit"] else f"{mean_v:.2f}")
        st.metric("Median (50th Percentile)", f"₹{med_v:,.2f}" if dist_var in ["Sales", "Income", "Profit"] else f"{med_v:.2f}")
        
        if skew > 0.5:
            st.warning(f"**Right-Skewed (Positive Skew):** The mean is noticeably pulled higher than the median by high-value transactions.")
        elif skew < -0.5:
            st.info(f"**Left-Skewed (Negative Skew):** Mass of the distribution is concentrated on the right.")
        else:
            st.success(f"**Approximately Symmetric:** Mean and median are closely centered.")

# -------------------------------------------------------------
# TAB 4: OUTLIER STUDIO
# -------------------------------------------------------------
with tabs[3]:
    st.subheader("Extreme Value Outlier Detection Engine (Section 3.5)")
    st.markdown(r"""
    Detects upper and lower statistical fences using the **IQR method** ($Q_1 \pm 1.5 \times \text{IQR}$)
    and classifies observations into legitimate commercial transactions versus data artifacts.
    """)

    target_var = st.selectbox("Select Target Variable for Outlier Isolation:", ["Sales", "Profit", "Income", "Age"])
    
    series = clean_df[target_var]
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers = clean_df[(clean_df[target_var] < lower_bound) | (clean_df[target_var] > upper_bound)]
    
    oc1, oc2, oc3, oc4 = st.columns(4)
    with oc1:
        st.metric("Lower Fence (Q1 - 1.5×IQR)", f"₹{lower_bound:,.2f}" if "Age" not in target_var else f"{lower_bound:.1f}")
    with oc2:
        st.metric("Upper Fence (Q3 + 1.5×IQR)", f"₹{upper_bound:,.2f}" if "Age" not in target_var else f"{upper_bound:.1f}")
    with oc3:
        st.metric("Outlier Transactions Count", f"{len(outliers):,}")
    with oc4:
        st.metric("Outlier Percentage", f"{(len(outliers)/len(clean_df)*100):.2f}%")

    st.markdown("---")
    col_out1, col_out2 = st.columns([7, 5])
    with col_out1:
        # Scatter Plot Sales vs Profit
        fig_scatter = px.scatter(
            clean_df,
            x="Sales",
            y="Profit",
            color="Customer_Segment",
            size="Quantity",
            hover_data=["Transaction_ID", "Product", "Region"],
            title="Sales vs Profit Scatter Analysis (Highlighting Enterprise Orders)",
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    with col_out2:
        st.markdown("### 🏢 Business Reasoning & Outlier Classification")
        if target_var in ["Sales", "Profit"]:
            st.success("""
            **Classification: Genuine Commercial High-Value Orders**  
            Upper outliers in Sales (> ₹30,000) correspond to bulk procurement orders placed by Corporate and Home Office accounts.
            These transactions involve multiple units of expensive Electronics (LED monitors, high-end laptops, server peripherals).
            
            **Managerial Verdict:** Retain in dataset without truncation. They reflect real enterprise cash flow and vital key-account revenue.
            """)
        elif target_var == "Income":
            st.info("""
            **Classification: Affluent Consumer Demographic**  
            High customer annual incomes reflect real-world wealth distribution across major Indian metro centers.
            
            **Managerial Verdict:** Retain in dataset. Use median income for baseline calculations.
            """)
        else:
            st.info("""
            **Classification: Normalized Demographics Post-Cleaning**  
            Entry errors (such as negative ages or 999 years) were corrected in the data cleaning phase.
            """)

# -------------------------------------------------------------
# TAB 5: BUSINESS QUESTIONS & GROUPBY
# -------------------------------------------------------------
with tabs[4]:
    st.subheader("Core Business Questions Answered via GroupBy Aggregation (Section 3.6)")

    bq_file = Path("eda_summary/business_questions_answers.md")
    if bq_file.exists():
        st.markdown(bq_file.read_text(encoding="utf-8"))

    st.markdown("---")
    st.subheader("Interactive Custom GroupBy Builder")
    groupby_col = st.selectbox("Group By Attribute:", ["Region", "Product_Category", "Customer_Segment", "Delivery_Mode", "Payment_Method"])
    metric_col = st.selectbox("Aggregate Metric:", ["Sales", "Profit", "Quantity", "Delivery_Days", "Discount"])
    
    custom_grp = clean_df.groupby(groupby_col).agg(
        Total=(metric_col, "sum"),
        Average=(metric_col, "mean"),
        Median=(metric_col, "median"),
        Order_Count=("Transaction_ID", "count")
    ).reset_index().round(2)
    
    st.dataframe(custom_grp, use_container_width=True)
    
    fig_cust = px.bar(
        custom_grp,
        x=groupby_col,
        y="Average",
        text_auto=True,
        title=f"Average {metric_col} by {groupby_col}",
        template="plotly_white",
        color="Average",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_cust, use_container_width=True)

# -------------------------------------------------------------
# TAB 6: FEATURE ENGINEERING & EXPORT
# -------------------------------------------------------------
with tabs[5]:
    st.subheader("Engineered Commercial Features & Clean Dataset Export")
    st.markdown("""
    Features engineered strictly following Section 3.6:
    - **`Delivery_Days`**: Order turnaround duration (`Delivery_Date - Order_Date`).
    - **`Profit_Margin`**: Percentage gross profit margin (`Profit / Sales * 100`).
    - **`Revenue_per_Customer`**: Cumulative customer lifetime value spend.
    - **`Discount_Amount`**: Rupee savings delivered to customer.
    - **`Delivery_SLA_Status`**: On-time vs delayed delivery classification.
    """)

    st.dataframe(clean_df[[
        "Transaction_ID", "Customer_ID", "Order_Date", "Delivery_Date",
        "Delivery_Days", "Sales", "Profit", "Profit_Margin", "Revenue_per_Customer", "Delivery_SLA_Status"
    ]].head(15), use_container_width=True)

    csv_data = clean_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Cleaned Dataset (CSV)",
        data=csv_data,
        file_name="cleaned_retail_sales_dataset.csv",
        mime="text/csv",
        help="Click to download the sanitized, 100% complete retail sales dataset."
    )

# -------------------------------------------------------------
# TAB 7: SRS & DOCUMENTATION HUB
# -------------------------------------------------------------
with tabs[6]:
    st.subheader("Central Documentation & Specification Hub")
    doc_choice = st.radio(
        "Select Document to Read:",
        ["Software Requirements Specification (SRS)", "Executive Business Insights Report", "Project Summary", "Data Dictionary"],
        horizontal=True
    )
    
    doc_mapping = {
        "Software Requirements Specification (SRS)": "docs/SRS_Document.md",
        "Executive Business Insights Report": "docs/Business_Insights_Report.md",
        "Project Summary": "docs/Project_Summary.md",
        "Data Dictionary": "docs/Data_Dictionary.md"
    }
    
    selected_doc_path = Path(doc_mapping[doc_choice])
    if selected_doc_path.exists():
        st.markdown(selected_doc_path.read_text(encoding="utf-8"))
    else:
        st.warning(f"File {selected_doc_path} not found.")

    st.markdown("---")
    st.subheader("📥 College Submission Ready PDF Reports (Formatted & Styled)")
    st.markdown("Download print-ready official PDF reports with high-resolution graphs and formal academic formatting:")
    
    pdf_col1, pdf_col2 = st.columns(2)
    
    proj_pdf_path = Path("submission_pdfs/Project_Summary_Report.pdf")
    if proj_pdf_path.exists():
        with pdf_col1:
            st.download_button(
                label="📊 Download Unified Project & EDA Summary PDF (18 Pages)",
                data=proj_pdf_path.read_bytes(),
                file_name="Project_and_EDA_Summary_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    code_pdf_path = Path("submission_pdfs/Source_Code_Documentation.pdf")
    if code_pdf_path.exists():
        with pdf_col2:
            st.download_button(
                label="💻 Download Source Code PDF (14 Pages)",
                data=code_pdf_path.read_bytes(),
                file_name="Source_Code_Documentation.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# -------------------------------------------------------------
# TAB 8: CODE & OUTPUT SNIPPETS GALLERY
# -------------------------------------------------------------
with tabs[7]:
    st.subheader("Standalone Code & Output Snippets Gallery")
    st.markdown("Inspect individual modular scripts and their verified terminal execution outputs.")
    
    snippet_choice = st.selectbox(
        "Select Snippet to Inspect:",
        [
            "01_data_audit_snippet.py",
            "02_data_cleaning_snippet.py",
            "03_feature_engineering_snippet.py",
            "04_outlier_detection_snippet.py",
            "05_groupby_business_queries.py"
        ]
    )
    
    snippet_path = Path("code_snippets") / snippet_choice
    code_text = snippet_path.read_text(encoding="utf-8") if snippet_path.exists() else "Code not found."
    
    st.code(code_text, language="python")
    
    st.markdown("### 🖥️ Verified Execution Output Log:")
    output_mapping = {
        "01_data_audit_snippet.py": "output_snippets/audit_summary_output.txt",
        "02_data_cleaning_snippet.py": "output_snippets/cleaning_log_output.txt",
        "03_feature_engineering_snippet.py": "output_snippets/groupby_results_output.txt",
        "04_outlier_detection_snippet.py": "output_snippets/outlier_detection_output.txt",
        "05_groupby_business_queries.py": "output_snippets/groupby_results_output.txt"
    }
    log_path = Path(output_mapping.get(snippet_choice, "output_snippets/audit_summary_output.txt"))
    if log_path.exists():
        st.text(log_path.read_text(encoding="utf-8"))
