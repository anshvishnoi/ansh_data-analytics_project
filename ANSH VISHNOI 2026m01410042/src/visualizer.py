"""
Visualizer Module
Generates high-resolution publication-grade static figures (PNG) for reports/presentations
and dynamic Plotly charts for the interactive Streamlit dashboard.
"""

from pathlib import Path
from typing import Optional
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless file generation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns


# Set uniform professional visual styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.dpi"] = 300


class Visualizer:
    """
    Visualization engine handling both static chart exporting and interactive Plotly objects.
    """

    def __init__(self, df: pd.DataFrame, output_dir: str = "eda_summary/figures"):
        self.df = df.copy()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # STATIC CHART EXPORTERS (Matplotlib / Seaborn)
    # ---------------------------------------------------------

    def export_missing_values_chart(self, missing_df: pd.DataFrame, filename: str = "01_missing_values_audit.png") -> str:
        """Exports missing value percentage bar chart."""
        fig, ax = plt.subplots(figsize=(10, 5))
        plot_data = missing_df[missing_df["Missing_Count"] > 0].sort_values(by="Missing_Percentage", ascending=True)
        bars = ax.barh(plot_data["Column"], plot_data["Missing_Percentage"], color="#3b82f6", edgecolor="#1d4ed8")
        ax.set_xlabel("Missing Percentage (%)", fontsize=11, fontweight="bold")
        ax.set_title("Data Quality Audit: Missing Values per Attribute (%)", fontsize=13, fontweight="bold", pad=12)
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2, f"{width:.2f}%", va="center", fontsize=10)
        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_sales_distribution(self, filename: str = "02_sales_distribution_skew.png") -> str:
        """Exports Sales distribution histogram with KDE overlay showing right-skewness."""
        fig, ax = plt.subplots(figsize=(10, 5))
        mean_val = self.df["Sales"].mean()
        median_val = self.df["Sales"].median()

        sns.histplot(self.df["Sales"], kde=True, color="#0284c7", bins=45, ax=ax, alpha=0.6)
        ax.axvline(mean_val, color="#dc2626", linestyle="--", linewidth=2, label=f"Mean: ₹{mean_val:,.0f}")
        ax.axvline(median_val, color="#16a34a", linestyle="-", linewidth=2, label=f"Median: ₹{median_val:,.0f}")

        ax.set_title(f"Sales Distribution (Right-Skewed, Skew = {self.df['Sales'].skew():.2f})", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Sales Value (₹)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Transaction Frequency", fontsize=11, fontweight="bold")
        ax.legend(frameon=True, facecolor="white", edgecolor="none")
        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_income_distribution(self, filename: str = "03_income_distribution.png") -> str:
        """Exports Income distribution histogram with KDE."""
        fig, ax = plt.subplots(figsize=(10, 5))
        mean_val = self.df["Income"].mean()
        median_val = self.df["Income"].median()

        sns.histplot(self.df["Income"], kde=True, color="#8b5cf6", bins=40, ax=ax, alpha=0.6)
        ax.axvline(mean_val, color="#dc2626", linestyle="--", linewidth=2, label=f"Mean: ₹{mean_val:,.0f}")
        ax.axvline(median_val, color="#16a34a", linestyle="-", linewidth=2, label=f"Median: ₹{median_val:,.0f}")

        ax.set_title(f"Annual Customer Income Distribution (Skew = {self.df['Income'].skew():.2f})", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Annual Income (₹)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Customer Count", fontsize=11, fontweight="bold")
        ax.legend(frameon=True, facecolor="white", edgecolor="none")
        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_age_distribution(self, filename: str = "04_age_demographics.png") -> str:
        """Exports Age demographic distribution histogram."""
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(self.df["Age"], kde=True, color="#10b981", bins=30, ax=ax, alpha=0.6)
        ax.set_title(f"Customer Age Demographics (Mean: {self.df['Age'].mean():.1f} yrs)", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Age (Years)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Customer Count", fontsize=11, fontweight="bold")
        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_category_and_segment_share(self, filename: str = "05_category_and_segment_share.png") -> str:
        """Exports multi-panel categorical breakdown for Region, Product Category, and Segment."""
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # Panel 1: Region
        self.df["Region"].value_counts().plot(kind="bar", ax=axes[0], color="#3b82f6", rot=0)
        axes[0].set_title("Orders by Region", fontweight="bold")
        axes[0].set_ylabel("Order Count")

        # Panel 2: Product Category
        self.df["Product_Category"].value_counts().plot(kind="bar", ax=axes[1], color="#f59e0b", rot=20)
        axes[1].set_title("Orders by Product Category", fontweight="bold")

        # Panel 3: Customer Segment
        self.df["Customer_Segment"].value_counts().plot(kind="bar", ax=axes[2], color="#ec4899", rot=0)
        axes[2].set_title("Orders by Customer Segment", fontweight="bold")

        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_outlier_boxplots(self, filename: str = "06_outliers_boxplots.png") -> str:
        """Exports 4-panel boxplots illustrating IQR outlier spreads for Sales, Profit, Income, Age."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        cols = [("Sales", "#0284c7"), ("Profit", "#10b981"), ("Income", "#8b5cf6"), ("Age", "#f59e0b")]

        for ax, (col, color) in zip(axes.flatten(), cols):
            sns.boxplot(x=self.df[col], ax=ax, color=color, flierprops={"marker": "o", "color": "red", "markersize": 3})
            ax.set_title(f"Outlier Detection: {col}", fontweight="bold", fontsize=12)
            ax.set_xlabel(col, fontsize=10)

        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_sales_vs_profit_scatter(self, filename: str = "07_sales_vs_profit_outliers.png") -> str:
        """Exports Sales vs Profit scatter plot colored by Customer Segment."""
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(
            data=self.df,
            x="Sales",
            y="Profit",
            hue="Customer_Segment",
            palette="Set2",
            alpha=0.7,
            ax=ax
        )
        ax.set_title("Sales vs Profit Scatter Analysis with High-Value Transactions", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Sales (₹)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Profit (₹)", fontsize=11, fontweight="bold")
        ax.legend(title="Segment", frameon=True)
        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_aov_by_region(self, filename: str = "08_aov_by_region.png") -> str:
        """Exports Average Order Value by Region comparison bar chart."""
        fig, ax = plt.subplots(figsize=(9, 5))
        aov = self.df.groupby("Region")["Sales"].mean().sort_values(ascending=False)
        bars = ax.bar(aov.index, aov.values, color="#059669", edgecolor="#047857", width=0.55)
        ax.set_title("Average Order Value (AOV) by Region (₹)", fontsize=13, fontweight="bold", pad=12)
        ax.set_ylabel("Mean Sales per Order (₹)", fontsize=11, fontweight="bold")
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 100, f"₹{height:,.0f}", ha="center", fontsize=10, fontweight="bold")
        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_profit_margin_by_category(self, filename: str = "09_profit_margin_by_category.png") -> str:
        """Exports Profit Margin % across Product Categories."""
        fig, ax = plt.subplots(figsize=(10, 5))
        cat_perf = self.df.groupby("Product_Category").agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        cat_perf["Margin_Pct"] = (cat_perf["Profit"] / cat_perf["Sales"]) * 100
        cat_perf = cat_perf.sort_values(by="Margin_Pct", ascending=True)

        bars = ax.barh(cat_perf.index, cat_perf["Margin_Pct"], color="#d97706", edgecolor="#b45309", height=0.55)
        ax.set_title("Profit Margin (%) across Product Categories", fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Profit Margin (%)", fontsize=11, fontweight="bold")
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.3, bar.get_y() + bar.get_height() / 2, f"{width:.1f}%", va="center", fontsize=10, fontweight="bold")
        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_return_rate_analysis(self, filename: str = "10_return_rate_analysis.png") -> str:
        """Exports return rate grouped bar chart by Customer Segment and Delivery Mode."""
        fig, ax = plt.subplots(figsize=(10, 5))
        ret_df = self.df.groupby(["Customer_Segment", "Delivery_Mode"]).agg(
            Total=("Transaction_ID", "count"),
            Returned=("Returned", lambda x: (x == "Yes").sum())
        ).reset_index()
        ret_df["Return_Rate"] = (ret_df["Returned"] / ret_df["Total"]) * 100

        sns.barplot(data=ret_df, x="Customer_Segment", y="Return_Rate", hue="Delivery_Mode", palette="crest", ax=ax)
        ax.set_title("Return Rate (%) by Customer Segment & Delivery Mode", fontsize=13, fontweight="bold", pad=12)
        ax.set_ylabel("Return Rate (%)", fontsize=11, fontweight="bold")
        ax.set_xlabel("Customer Segment", fontsize=11, fontweight="bold")
        ax.legend(title="Delivery Mode", frameon=True)
        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_correlation_heatmap(self, filename: str = "11_correlation_heatmap.png") -> str:
        """Exports correlation matrix heatmap for all key numerical variables."""
        fig, ax = plt.subplots(figsize=(10, 8))
        num_cols = ["Age", "Income", "Quantity", "Unit_Price", "Discount", "Sales", "Cost", "Profit"]
        if "Delivery_Days" in self.df.columns:
            num_cols.append("Delivery_Days")
        corr = self.df[num_cols].corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
        ax.set_title("Inter-Variable Correlation Matrix", fontsize=13, fontweight="bold", pad=12)
        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_monthly_sales_trend(self, filename: str = "12_monthly_sales_trend.png") -> str:
        """Exports 2023-2024 monthly sales and profit timeline trend."""
        fig, ax1 = plt.subplots(figsize=(12, 5))
        if "Order_YearMonth" not in self.df.columns:
            self.df["Order_YearMonth"] = pd.to_datetime(self.df["Order_Date"]).dt.to_period("M").astype(str)

        monthly = self.df.groupby("Order_YearMonth").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()

        ax1.plot(monthly["Order_YearMonth"], monthly["Sales"], marker="o", color="#0284c7", linewidth=2.5, label="Total Sales (₹)")
        ax1.plot(monthly["Order_YearMonth"], monthly["Profit"], marker="s", color="#16a34a", linewidth=2, linestyle="--", label="Total Profit (₹)")
        ax1.set_title("Monthly Revenue & Profit Growth Trajectory (2023 - 2024)", fontsize=13, fontweight="bold", pad=12)
        ax1.set_xlabel("Year-Month", fontsize=11, fontweight="bold")
        ax1.set_ylabel("Amount (₹)", fontsize=11, fontweight="bold")
        ax1.set_xticks(range(len(monthly)))
        ax1.set_xticklabels(monthly["Order_YearMonth"], rotation=45, ha="right", fontsize=9)
        ax1.legend(frameon=True)
        plt.tight_layout()
        save_path = self.output_dir / filename
        fig.savefig(save_path, bbox_inches="tight")
        plt.close(fig)
        return str(save_path)

    def export_all_figures(self, missing_df: Optional[pd.DataFrame] = None) -> list:
        """Exports complete suite of 12 publication-ready PNG figures."""
        paths = []
        if missing_df is not None:
            paths.append(self.export_missing_values_chart(missing_df))
        paths.append(self.export_sales_distribution())
        paths.append(self.export_income_distribution())
        paths.append(self.export_age_distribution())
        paths.append(self.export_category_and_segment_share())
        paths.append(self.export_outlier_boxplots())
        paths.append(self.export_sales_vs_profit_scatter())
        paths.append(self.export_aov_by_region())
        paths.append(self.export_profit_margin_by_category())
        paths.append(self.export_return_rate_analysis())
        paths.append(self.export_correlation_heatmap())
        paths.append(self.export_monthly_sales_trend())
        return paths

    # ---------------------------------------------------------
    # INTERACTIVE PLOTLY BUILDERS (For Streamlit Application)
    # ---------------------------------------------------------

    def create_interactive_sales_dist(self) -> go.Figure:
        fig = px.histogram(
            self.df,
            x="Sales",
            nbins=50,
            marginal="box",
            title="Interactive Sales Distribution & Outlier Box",
            color_discrete_sequence=["#0284c7"]
        )
        fig.update_layout(template="plotly_white", xaxis_title="Sales (₹)", yaxis_title="Count")
        return fig

    def create_interactive_scatter_sales_profit(self) -> go.Figure:
        fig = px.scatter(
            self.df,
            x="Sales",
            y="Profit",
            color="Product_Category",
            size="Quantity",
            hover_data=["Transaction_ID", "Customer_Segment", "Delivery_Mode"],
            title="Sales vs Profit Bubble Chart (Size = Quantity)",
            template="plotly_white"
        )
        return fig

    def create_interactive_regional_bar(self) -> go.Figure:
        regional = self.df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
        fig = px.bar(
            regional,
            x="Region",
            y=["Sales", "Profit"],
            barmode="group",
            title="Total Sales and Profit by Region",
            template="plotly_white",
            color_discrete_sequence=["#2563eb", "#10b981"]
        )
        return fig

    def create_interactive_monthly_trend(self) -> go.Figure:
        monthly = self.df.groupby("Order_YearMonth").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
        fig = px.line(
            monthly,
            x="Order_YearMonth",
            y=["Sales", "Profit"],
            markers=True,
            title="2-Year Revenue & Profit Trajectory (2023 - 2024)",
            template="plotly_white",
            color_discrete_sequence=["#0284c7", "#16a34a"]
        )
        fig.update_xaxes(title="Month")
        fig.update_yaxes(title="Rupees (₹)")
        return fig
