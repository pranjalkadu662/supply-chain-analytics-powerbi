from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load raw data
project = Path(__file__).resolve().parent.parent
raw = project / "Dataset" / "supply_chain_dataset1.csv"
df = pd.read_csv(raw)
print("Shape:", df.shape)
print(df.head())
df.info()

# 2. Clean
df.columns = df.columns.str.strip()
df["Date"] = pd.to_datetime(df["Date"])
print("Missing:", df.isnull().sum().sum())
print("Duplicates:", df.duplicated().sum())
df = df.drop_duplicates()
df.to_csv(project / "Dataset" / "cleaned_supply_chain.csv", index=False)
print("Cleaned file saved")

# 3. Business questions
df["Inventory_Value"] = df["Inventory_Level"] * df["Unit_Cost"]
df["Below_Reorder"] = df["Inventory_Level"] < df["Reorder_Point"]

top_sku = df.groupby("SKU_ID")["Units_Sold"].sum().nlargest(10)
wh_inv = df.groupby("Warehouse_ID")["Inventory_Level"].mean().sort_values()
sup_lead = df.groupby("Supplier_ID")["Supplier_Lead_Time_Days"].mean().sort_values()
low_stock = df[df["Below_Reorder"]].groupby("SKU_ID").size().nlargest(10)
monthly = df.groupby(df["Date"].dt.to_period("M"))[["Units_Sold", "Demand_Forecast"]].sum()

print("\nTotal inventory value:", round(df["Inventory_Value"].sum(), 2))
print("Rows below reorder point:", int(df["Below_Reorder"].sum()))
print("\nTop SKUs:\n", top_sku)
print("\nSupplier lead time:\n", sup_lead)
print("\nLow-stock SKUs:\n", low_stock)

# 4. Charts
out = project / "Dashboard"
out.mkdir(exist_ok=True)

def bar(series, title, name, horizontal=False):
    plt.figure(figsize=(10, 5))
    series.plot(kind="barh" if horizontal else "bar")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out / name)
    plt.close()

bar(top_sku, "Top 10 SKUs by Units Sold", "top_skus.png")
bar(wh_inv, "Avg Inventory by Warehouse", "warehouse_inventory.png", True)
bar(sup_lead, "Avg Lead Time by Supplier (days)", "supplier_lead_time.png", True)
bar(low_stock, "SKUs Most Often Below Reorder Point", "low_stock.png")

monthly.index = monthly.index.astype(str)
monthly.plot(figsize=(11, 5), title="Monthly Units Sold vs Forecast")
plt.tight_layout()
plt.savefig(out / "demand_vs_forecast.png")
plt.close()

print("\nCharts saved in Dashboard folder")