"""
AgroSmart ML Model Training Script
Trains and saves machine learning models for crop prediction, fertilizer recommendation, and yield estimation.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
import joblib
import os

# Create directories if they don't exist
os.makedirs('trained_models', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

print("=" * 80)
print("🌾 AgroSmart ML Model Training Pipeline")
print("=" * 80)

# =====================================================================
# 1. CROP RECOMMENDATION MODEL
# =====================================================================
print("\n1️⃣  Training Crop Recommendation Model...")
print("-" * 80)

# Load data
crop_data = pd.read_csv('data/raw/Crop_recommendation.csv')
print(f"✓ Loaded crop data: {crop_data.shape}")
print(f"✓ Features: {list(crop_data.columns[:-1])}")
print(f"✓ Target: {crop_data['label'].nunique()} unique crops")

# Check for missing values
if crop_data.isnull().sum().sum() > 0:
    print("⚠️  Missing values detected, filling with median...")
    crop_data.fillna(crop_data.median(numeric_only=True), inplace=True)

# Prepare features and target
X_crop = crop_data.drop('label', axis=1)
y_crop = crop_data['label']

# Split data
X_train_crop, X_test_crop, y_train_crop, y_test_crop = train_test_split(
    X_crop, y_crop, test_size=0.2, random_state=42, stratify=y_crop
)
print(f"✓ Train set: {X_train_crop.shape}, Test set: {X_test_crop.shape}")

# Feature scaling
scaler_crop = StandardScaler()
X_train_crop_scaled = scaler_crop.fit_transform(X_train_crop)
X_test_crop_scaled = scaler_crop.transform(X_test_crop)

# Train model
print("🔄 Training Random Forest Classifier...")
crop_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
crop_model.fit(X_train_crop_scaled, y_train_crop)

# Evaluate
y_pred_crop = crop_model.predict(X_test_crop_scaled)
crop_accuracy = accuracy_score(y_test_crop, y_pred_crop)
print(f"✅ Crop Model Accuracy: {crop_accuracy:.4f} ({crop_accuracy*100:.2f}%)")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X_crop.columns,
    'importance': crop_model.feature_importances_
}).sort_values('importance', ascending=False)
print(f"\n📊 Top 5 Most Important Features:")
print(feature_importance.head().to_string(index=False))

# Save model and scaler
joblib.dump(crop_model, 'trained_models/crop_model.pkl')
joblib.dump(scaler_crop, 'trained_models/crop_scaler.pkl')
joblib.dump(list(X_crop.columns), 'trained_models/crop_features.pkl')
print(f"💾 Saved: crop_model.pkl, crop_scaler.pkl, crop_features.pkl")

# =====================================================================
# 2. FERTILIZER RECOMMENDATION MODEL
# =====================================================================
print("\n2️⃣  Training Fertilizer Recommendation Model...")
print("-" * 80)

# Load data
fert_data = pd.read_csv('data/raw/fertilizer_recommendation_dataset.csv')
print(f"✓ Loaded fertilizer data: {fert_data.shape}")
print(f"✓ Columns: {list(fert_data.columns)}")

# Check column names and handle variations
# Common variations: 'Fertilizer Name', 'fertilizer', 'Fertilizer', etc.
target_col = None
for col in fert_data.columns:
    if 'fertilizer' in col.lower():
        target_col = col
        break

if target_col is None:
    print("⚠️  Could not find fertilizer target column, using last column")
    target_col = fert_data.columns[-1]

print(f"✓ Target column: '{target_col}'")
print(f"✓ Unique fertilizers: {fert_data[target_col].nunique()}")

# Handle missing values
if fert_data.isnull().sum().sum() > 0:
    print("⚠️  Missing values detected, filling...")
    fert_data.fillna(fert_data.median(numeric_only=True), inplace=True)
    fert_data.fillna(fert_data.mode().iloc[0], inplace=True)

# Encode categorical features
label_encoders = {}
for col in fert_data.columns:
    if fert_data[col].dtype == 'object' and col != target_col:
        le = LabelEncoder()
        fert_data[col] = le.fit_transform(fert_data[col].astype(str))
        label_encoders[col] = le

# Prepare features and target
X_fert = fert_data.drop(target_col, axis=1)
y_fert = fert_data[target_col]

# Split data
X_train_fert, X_test_fert, y_train_fert, y_test_fert = train_test_split(
    X_fert, y_fert, test_size=0.2, random_state=42
)
print(f"✓ Train set: {X_train_fert.shape}, Test set: {X_test_fert.shape}")

# Feature scaling
scaler_fert = StandardScaler()
X_train_fert_scaled = scaler_fert.fit_transform(X_train_fert)
X_test_fert_scaled = scaler_fert.transform(X_test_fert)

# Train model
print("🔄 Training Random Forest Classifier...")
fert_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
fert_model.fit(X_train_fert_scaled, y_train_fert)

# Evaluate
y_pred_fert = fert_model.predict(X_test_fert_scaled)
fert_accuracy = accuracy_score(y_test_fert, y_pred_fert)
print(f"✅ Fertilizer Model Accuracy: {fert_accuracy:.4f} ({fert_accuracy*100:.2f}%)")

# Save model
joblib.dump(fert_model, 'trained_models/fertilizer_model.pkl')
joblib.dump(scaler_fert, 'trained_models/fertilizer_scaler.pkl')
joblib.dump(list(X_fert.columns), 'trained_models/fertilizer_features.pkl')
joblib.dump(label_encoders, 'trained_models/fertilizer_encoders.pkl')
joblib.dump(target_col, 'trained_models/fertilizer_target_col.pkl')
print(f"💾 Saved: fertilizer_model.pkl, fertilizer_scaler.pkl, fertilizer_features.pkl")

# =====================================================================
# 3. YIELD ESTIMATION MODEL
# =====================================================================
print("\n3️⃣  Training Yield Estimation Model...")
print("-" * 80)

# Load data
yield_data = pd.read_csv('data/raw/yield_df.csv')
print(f"✓ Loaded yield data: {yield_data.shape}")
print(f"✓ Columns: {list(yield_data.columns)}")

# Find target column (yield related)
target_col_yield = None
for col in yield_data.columns:
    if 'yield' in col.lower() or 'hg/ha' in col.lower():
        target_col_yield = col
        break

if target_col_yield is None:
    print("⚠️  Could not find yield target column, using last column")
    target_col_yield = yield_data.columns[-1]

print(f"✓ Target column: '{target_col_yield}'")

# Handle missing values
if yield_data.isnull().sum().sum() > 0:
    print("⚠️  Missing values detected, dropping rows with missing target...")
    yield_data = yield_data.dropna(subset=[target_col_yield])
    yield_data.fillna(yield_data.median(numeric_only=True), inplace=True)
    yield_data.fillna(yield_data.mode().iloc[0], inplace=True)

# Encode categorical features
yield_label_encoders = {}
for col in yield_data.columns:
    if yield_data[col].dtype == 'object' and col != target_col_yield:
        le = LabelEncoder()
        yield_data[col] = le.fit_transform(yield_data[col].astype(str))
        yield_label_encoders[col] = le

# Prepare features and target
X_yield = yield_data.drop(target_col_yield, axis=1)
y_yield = yield_data[target_col_yield]

# Remove any remaining non-numeric columns
X_yield = X_yield.select_dtypes(include=[np.number])

# Split data
X_train_yield, X_test_yield, y_train_yield, y_test_yield = train_test_split(
    X_yield, y_yield, test_size=0.2, random_state=42
)
print(f"✓ Train set: {X_train_yield.shape}, Test set: {X_test_yield.shape}")

# Feature scaling
scaler_yield = StandardScaler()
X_train_yield_scaled = scaler_yield.fit_transform(X_train_yield)
X_test_yield_scaled = scaler_yield.transform(X_test_yield)

# Train model
print("🔄 Training Random Forest Regressor...")
yield_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
yield_model.fit(X_train_yield_scaled, y_train_yield)

# Evaluate
y_pred_yield = yield_model.predict(X_test_yield_scaled)
yield_r2 = r2_score(y_test_yield, y_pred_yield)
yield_rmse = np.sqrt(mean_squared_error(y_test_yield, y_pred_yield))
yield_mae = np.mean(np.abs(y_test_yield - y_pred_yield))

print(f"✅ Yield Model Performance:")
print(f"   R² Score: {yield_r2:.4f}")
print(f"   RMSE: {yield_rmse:.2f}")
print(f"   MAE: {yield_mae:.2f}")

# Save model
joblib.dump(yield_model, 'trained_models/yield_model.pkl')
joblib.dump(scaler_yield, 'trained_models/yield_scaler.pkl')
joblib.dump(list(X_yield.columns), 'trained_models/yield_features.pkl')
joblib.dump(yield_label_encoders, 'trained_models/yield_encoders.pkl')
joblib.dump(target_col_yield, 'trained_models/yield_target_col.pkl')
print(f"💾 Saved: yield_model.pkl, yield_scaler.pkl, yield_features.pkl")

# =====================================================================
# SUMMARY
# =====================================================================
print("\n" + "=" * 80)
print("🎉 MODEL TRAINING COMPLETE!")
print("=" * 80)
print(f"1️⃣  Crop Recommendation Model - Accuracy: {crop_accuracy*100:.2f}%")
print(f"2️⃣  Fertilizer Recommendation Model - Accuracy: {fert_accuracy*100:.2f}%")
print(f"3️⃣  Yield Estimation Model - R²: {yield_r2:.4f}, RMSE: {yield_rmse:.2f}")
print("\n📁 All models saved in 'trained_models/' directory")
print("✅ Ready to integrate with FastAPI backend!")
print("=" * 80)
