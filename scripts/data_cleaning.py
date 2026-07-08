"""
=========================================================
Healthcare Analytics Project
Module 2 : Data Cleaning & Transformation

Author : Niharika

Purpose:
--------
Profile hospital_raw_data.csv before cleaning.
=========================================================
"""

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Project Paths
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = pd.read_csv(
    DATA_DIR / "hospital_raw_data.csv",
    low_memory=False
)

print("=" * 60)
print("MODULE 2 : DATA CLEANING & TRANSFORMATION")
print("=" * 60)

# --------------------------------------------------
# Dataset Shape
# --------------------------------------------------
print("\n1. Dataset Shape")
print(df.shape)

# --------------------------------------------------
# Column Information
# --------------------------------------------------
print("\n2. Dataset Information")
print(df.info())

# --------------------------------------------------
# Missing Values
# --------------------------------------------------
print("\n3. Missing Values")
print(df.isnull().sum())

# --------------------------------------------------
# Duplicate Records
# --------------------------------------------------
print("\n4. Duplicate Records")
print(df.duplicated().sum())

# --------------------------------------------------
# Numerical Summary
# --------------------------------------------------
print("\n5. Numerical Summary")
print(df.describe())

# --------------------------------------------------
# Categorical Summary
# --------------------------------------------------
print("\n6. Categorical Summary")
print(df.describe(include="object"))

# --------------------------------------------------
# First Five Rows
# --------------------------------------------------
print("\n7. First Five Records")
print(df.head())
# --------------------------------------------------
# Payment Typology 3 Analysis
# --------------------------------------------------

print("\n8. Payment Typology 3 Analysis")
print("-" * 50)

print("\nNon-null records:")
print(df["Payment Typology 3"].notna().sum())

print("\nUnique values:")
print(df["Payment Typology 3"].dropna().unique())

print("\nValue Counts:")
print(df["Payment Typology 3"].value_counts(dropna=False))