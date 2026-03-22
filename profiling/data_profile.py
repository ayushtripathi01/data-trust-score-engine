import pandas as pd



print("STARTING TRUST ENGINE\n")

df = pd.read_csv("C:/Users/Ayush/OneDrive/Desktop/data-trust-score-engine/data/raw/superstore.csv")

print("Dataset Loaded Successfully")
print("Shape:", df.shape)

critical_columns = ['sales', 'order_id', 'order_date']
# -----------------------------
# STRONG DATA ISSUES (FINAL)
# -----------------------------

# Large missing values
df.loc[0:3000, 'sales'] = None

# Large negative sales
df.loc[3000:6000, 'sales'] = -100

# Missing order_id
df.loc[6000:9000, 'order_id'] = None

# Future dates
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df.loc[9000:12000, 'order_date'] = pd.Timestamp('2099-01-01')

# -----------------------------
# COMPLETENESS CALCULATION
# -----------------------------

# -----------------------------
# COMPLETENESS (CRITICAL ONLY)
# -----------------------------

missing_cells = df[critical_columns].isnull().sum().sum()
total_cells = len(df) * len(critical_columns)

completeness_score = ((total_cells - missing_cells) / total_cells) * 100

print("\n[Critical Columns Only]")
print("Total Cells:", total_cells)
print("Missing Cells:", missing_cells)

print(f"\nCompleteness Score: {completeness_score:.2f}%")

# -----------------------------
# ACCURACY CHECKS
# -----------------------------

total_checks = 0
failed_checks = 0

# Convert sales to numeric (IMPORTANT FIX)
df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

# Rule 1: Sales should not be negative
total_checks += len(df)
failed_checks += (df['sales'] < 0).sum()

print("Negative Sales Count:", (df['sales'] < 0).sum())
# Rule 2: Order ID should not be missing
if 'order_id' in df.columns:
    total_checks += len(df)
    failed_checks += df['order_id'].isnull().sum()
    print("Missing Order ID:", df['order_id'].isnull().sum())

# Rule 3: Order Date should not be in future
if 'order_date' in df.columns:
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    total_checks += len(df)
    failed_checks += (df['order_date'] > pd.Timestamp.today()).sum()
    print("Future Dates Count:", (df['order_date'] > pd.Timestamp.today()).sum())

# -----------------------------
# ACCURACY SCORE
# -----------------------------

if total_checks == 0:
    accuracy_score = 0
else:
    accuracy_score = ((total_checks - failed_checks) / total_checks) * 100

print(f"\nAccuracy Score: {accuracy_score:.2f}%")

# -----------------------------
# FINAL TRUST SCORE
# -----------------------------

trust_score = (completeness_score * 0.5) + (accuracy_score * 0.5)

print(f"\nFinal Trust Score: {trust_score:.2f}%")

# -----------------------------
# RECOMMENDATION ENGINE
# -----------------------------

print("\n--- RECOMMENDATION ---")

if completeness_score < 95:
    print("High missing data. Consider data cleaning.")

if accuracy_score < 95:
    print("Data contains invalid or inconsistent values.")

if trust_score >= 85:
    print("Dataset is suitable for analytics.")
else:
    print("Dataset is NOT recommended for AI/analytics.")