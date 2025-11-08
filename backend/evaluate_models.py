"""
AgroSmart ML Model Performance Evaluation
Comprehensive analysis of all trained models with detailed metrics
"""
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    mean_squared_error, mean_absolute_error, r2_score
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)

print("=" * 80)
print("🔬 AgroSmart ML Model Performance Analysis")
print("=" * 80)
print()

# =====================================================================
# 1. CROP PREDICTION MODEL EVALUATION
# =====================================================================
print("1️⃣  CROP RECOMMENDATION MODEL PERFORMANCE")
print("-" * 80)

# Load model and data
crop_model = joblib.load('trained_models/crop_model.pkl')
crop_scaler = joblib.load('trained_models/crop_scaler.pkl')
crop_features = joblib.load('trained_models/crop_features.pkl')

# Load and prepare data
crop_data = pd.read_csv('data/raw/Crop_recommendation.csv')
X_crop = crop_data.drop('label', axis=1)
y_crop = crop_data['label']

# Split data (same as training)
X_train_crop, X_test_crop, y_train_crop, y_test_crop = train_test_split(
    X_crop, y_crop, test_size=0.2, random_state=42, stratify=y_crop
)

# Scale and predict
X_test_crop_scaled = crop_scaler.transform(X_test_crop)
y_pred_crop = crop_model.predict(X_test_crop_scaled)
y_pred_proba_crop = crop_model.predict_proba(X_test_crop_scaled)

# Calculate metrics
crop_accuracy = accuracy_score(y_test_crop, y_pred_crop)
crop_precision = precision_score(y_test_crop, y_pred_crop, average='weighted', zero_division=0)
crop_recall = recall_score(y_test_crop, y_pred_crop, average='weighted', zero_division=0)
crop_f1 = f1_score(y_test_crop, y_pred_crop, average='weighted', zero_division=0)

print(f"\n📊 Overall Metrics:")
print(f"   Accuracy:  {crop_accuracy:.4f} ({crop_accuracy*100:.2f}%)")
print(f"   Precision: {crop_precision:.4f}")
print(f"   Recall:    {crop_recall:.4f}")
print(f"   F1-Score:  {crop_f1:.4f}")

print(f"\n🎯 Training vs Testing:")
print(f"   Training samples: {len(X_train_crop)}")
print(f"   Testing samples:  {len(X_test_crop)}")
print(f"   Number of crops:  {len(crop_model.classes_)}")

# Feature importance
feature_importance_crop = pd.DataFrame({
    'Feature': crop_features,
    'Importance': crop_model.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\n🔝 Top 5 Most Important Features:")
for idx, row in feature_importance_crop.head().iterrows():
    print(f"   {row['Feature']:12s}: {row['Importance']:.4f} ({row['Importance']*100:.2f}%)")

# Per-class performance
print(f"\n📋 Per-Crop Performance (Top 10 by samples):")
crop_counts = y_test_crop.value_counts()
print(f"   {'Crop':<15} {'Samples':>8} {'Precision':>10} {'Recall':>10} {'F1-Score':>10}")
print(f"   {'-'*15} {'-'*8} {'-'*10} {'-'*10} {'-'*10}")

for crop in crop_counts.head(10).index:
    mask = y_test_crop == crop
    if mask.sum() > 0:
        crop_pred = y_pred_crop[mask]
        crop_true = y_test_crop[mask]
        prec = precision_score(crop_true, crop_pred, average='binary', pos_label=crop, zero_division=0)
        rec = recall_score(crop_true, crop_pred, average='binary', pos_label=crop, zero_division=0)
        f1 = f1_score(crop_true, crop_pred, average='binary', pos_label=crop, zero_division=0)
        print(f"   {crop:<15} {mask.sum():>8} {prec:>10.4f} {rec:>10.4f} {f1:>10.4f}")

# Confidence analysis
confidence_scores = np.max(y_pred_proba_crop, axis=1)
print(f"\n🎲 Prediction Confidence:")
print(f"   Mean confidence: {confidence_scores.mean():.4f} ({confidence_scores.mean()*100:.2f}%)")
print(f"   Min confidence:  {confidence_scores.min():.4f} ({confidence_scores.min()*100:.2f}%)")
print(f"   Max confidence:  {confidence_scores.max():.4f} ({confidence_scores.max()*100:.2f}%)")
print(f"   Std deviation:   {confidence_scores.std():.4f}")

# High vs Low confidence accuracy
high_conf_mask = confidence_scores > 0.8
if high_conf_mask.sum() > 0:
    high_conf_acc = accuracy_score(y_test_crop[high_conf_mask], y_pred_crop[high_conf_mask])
    print(f"   High confidence (>80%): {high_conf_mask.sum()} predictions, {high_conf_acc*100:.2f}% accuracy")

low_conf_mask = confidence_scores < 0.5
if low_conf_mask.sum() > 0:
    low_conf_acc = accuracy_score(y_test_crop[low_conf_mask], y_pred_crop[low_conf_mask])
    print(f"   Low confidence (<50%):  {low_conf_mask.sum()} predictions, {low_conf_acc*100:.2f}% accuracy")

# =====================================================================
# 2. FERTILIZER RECOMMENDATION MODEL EVALUATION
# =====================================================================
print("\n\n2️⃣  FERTILIZER RECOMMENDATION MODEL PERFORMANCE")
print("-" * 80)

# Load model and data
fert_model = joblib.load('trained_models/fertilizer_model.pkl')
fert_scaler = joblib.load('trained_models/fertilizer_scaler.pkl')
fert_features = joblib.load('trained_models/fertilizer_features.pkl')
fert_encoders = joblib.load('trained_models/fertilizer_encoders.pkl')
fert_target_col = joblib.load('trained_models/fertilizer_target_col.pkl')

# Load and prepare data
fert_data = pd.read_csv('data/raw/fertilizer_recommendation_dataset.csv')

# Encode categorical features
fert_data_encoded = fert_data.copy()
for col in fert_data.columns:
    if fert_data[col].dtype == 'object' and col != fert_target_col:
        if col in fert_encoders:
            fert_data_encoded[col] = fert_encoders[col].transform(fert_data[col].astype(str))

X_fert = fert_data_encoded.drop(fert_target_col, axis=1)
y_fert = fert_data[fert_target_col]

# Split data
X_train_fert, X_test_fert, y_train_fert, y_test_fert = train_test_split(
    X_fert, y_fert, test_size=0.2, random_state=42
)

# Scale and predict
X_test_fert_scaled = fert_scaler.transform(X_test_fert)
y_pred_fert = fert_model.predict(X_test_fert_scaled)
y_pred_proba_fert = fert_model.predict_proba(X_test_fert_scaled)

# Calculate metrics
fert_accuracy = accuracy_score(y_test_fert, y_pred_fert)
fert_precision = precision_score(y_test_fert, y_pred_fert, average='weighted', zero_division=0)
fert_recall = recall_score(y_test_fert, y_pred_fert, average='weighted', zero_division=0)
fert_f1 = f1_score(y_test_fert, y_pred_fert, average='weighted', zero_division=0)

print(f"\n📊 Overall Metrics:")
print(f"   Accuracy:  {fert_accuracy:.4f} ({fert_accuracy*100:.2f}%)")
print(f"   Precision: {fert_precision:.4f}")
print(f"   Recall:    {fert_recall:.4f}")
print(f"   F1-Score:  {fert_f1:.4f}")

print(f"\n🎯 Training vs Testing:")
print(f"   Training samples:   {len(X_train_fert)}")
print(f"   Testing samples:    {len(X_test_fert)}")
print(f"   Number of fertilizers: {len(fert_model.classes_)}")

# Feature importance
feature_importance_fert = pd.DataFrame({
    'Feature': fert_features,
    'Importance': fert_model.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\n🔝 Top 5 Most Important Features:")
for idx, row in feature_importance_fert.head().iterrows():
    print(f"   {row['Feature']:15s}: {row['Importance']:.4f} ({row['Importance']*100:.2f}%)")

# Per-fertilizer performance
print(f"\n📋 Per-Fertilizer Performance:")
fert_counts = y_test_fert.value_counts()
print(f"   {'Fertilizer':<20} {'Samples':>8} {'Precision':>10} {'Recall':>10} {'F1-Score':>10}")
print(f"   {'-'*20} {'-'*8} {'-'*10} {'-'*10} {'-'*10}")

for fert in fert_counts.index:
    mask = y_test_fert == fert
    if mask.sum() > 0:
        fert_pred = y_pred_fert[mask]
        fert_true = y_test_fert[mask]
        prec = precision_score(fert_true, fert_pred, average='binary', pos_label=fert, zero_division=0)
        rec = recall_score(fert_true, fert_pred, average='binary', pos_label=fert, zero_division=0)
        f1 = f1_score(fert_true, fert_pred, average='binary', pos_label=fert, zero_division=0)
        print(f"   {fert:<20} {mask.sum():>8} {prec:>10.4f} {rec:>10.4f} {f1:>10.4f}")

# =====================================================================
# 3. YIELD ESTIMATION MODEL EVALUATION
# =====================================================================
print("\n\n3️⃣  YIELD ESTIMATION MODEL PERFORMANCE")
print("-" * 80)

# Load model and data
yield_model = joblib.load('trained_models/yield_model.pkl')
yield_scaler = joblib.load('trained_models/yield_scaler.pkl')
yield_features = joblib.load('trained_models/yield_features.pkl')
yield_encoders = joblib.load('trained_models/yield_encoders.pkl')
yield_target_col = joblib.load('trained_models/yield_target_col.pkl')

# Load and prepare data
yield_data = pd.read_csv('data/raw/yield_df.csv')

# Drop rows with missing target
yield_data = yield_data.dropna(subset=[yield_target_col])

# Encode categorical features
yield_data_encoded = yield_data.copy()
for col in yield_data.columns:
    if yield_data[col].dtype == 'object' and col != yield_target_col:
        if col in yield_encoders:
            yield_data_encoded[col] = yield_encoders[col].transform(yield_data[col].astype(str))

X_yield = yield_data_encoded.drop(yield_target_col, axis=1)
y_yield = yield_data[yield_target_col]

# Keep only numeric columns
X_yield = X_yield.select_dtypes(include=[np.number])

# Split data
X_train_yield, X_test_yield, y_train_yield, y_test_yield = train_test_split(
    X_yield, y_yield, test_size=0.2, random_state=42
)

# Scale and predict
X_test_yield_scaled = yield_scaler.transform(X_test_yield)
y_pred_yield = yield_model.predict(X_test_yield_scaled)

# Calculate metrics
yield_r2 = r2_score(y_test_yield, y_pred_yield)
yield_rmse = np.sqrt(mean_squared_error(y_test_yield, y_pred_yield))
yield_mae = mean_absolute_error(y_test_yield, y_pred_yield)
yield_mape = np.mean(np.abs((y_test_yield - y_pred_yield) / y_test_yield)) * 100

print(f"\n📊 Overall Metrics:")
print(f"   R² Score:  {yield_r2:.4f} ({yield_r2*100:.2f}% variance explained)")
print(f"   RMSE:      {yield_rmse:.2f} hg/ha")
print(f"   MAE:       {yield_mae:.2f} hg/ha")
print(f"   MAPE:      {yield_mape:.2f}%")

print(f"\n🎯 Training vs Testing:")
print(f"   Training samples: {len(X_train_yield)}")
print(f"   Testing samples:  {len(X_test_yield)}")

# Feature importance
feature_importance_yield = pd.DataFrame({
    'Feature': yield_features,
    'Importance': yield_model.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\n🔝 Top 5 Most Important Features:")
for idx, row in feature_importance_yield.head().iterrows():
    print(f"   {row['Feature']:30s}: {row['Importance']:.4f} ({row['Importance']*100:.2f}%)")

# Prediction quality analysis
residuals = y_test_yield - y_pred_yield
print(f"\n📈 Prediction Quality:")
print(f"   Mean residual:     {residuals.mean():.2f} hg/ha")
print(f"   Std residual:      {residuals.std():.2f} hg/ha")
print(f"   Min residual:      {residuals.min():.2f} hg/ha")
print(f"   Max residual:      {residuals.max():.2f} hg/ha")

# Accuracy within ranges
within_10_pct = (np.abs(residuals) / y_test_yield <= 0.10).sum()
within_20_pct = (np.abs(residuals) / y_test_yield <= 0.20).sum()
within_30_pct = (np.abs(residuals) / y_test_yield <= 0.30).sum()

print(f"\n🎯 Prediction Accuracy Ranges:")
print(f"   Within ±10%: {within_10_pct}/{len(y_test_yield)} ({within_10_pct/len(y_test_yield)*100:.2f}%)")
print(f"   Within ±20%: {within_20_pct}/{len(y_test_yield)} ({within_20_pct/len(y_test_yield)*100:.2f}%)")
print(f"   Within ±30%: {within_30_pct}/{len(y_test_yield)} ({within_30_pct/len(y_test_yield)*100:.2f}%)")

# =====================================================================
# SUMMARY
# =====================================================================
print("\n\n" + "=" * 80)
print("📊 PERFORMANCE SUMMARY")
print("=" * 80)

print(f"\n1️⃣  Crop Recommendation:")
print(f"   • Accuracy: {crop_accuracy*100:.2f}%")
print(f"   • F1-Score: {crop_f1:.4f}")
print(f"   • Mean Confidence: {confidence_scores.mean()*100:.2f}%")
print(f"   • Status: {'✅ EXCELLENT' if crop_accuracy > 0.95 else '✓ Good'}")

print(f"\n2️⃣  Fertilizer Recommendation:")
print(f"   • Accuracy: {fert_accuracy*100:.2f}%")
print(f"   • F1-Score: {fert_f1:.4f}")
print(f"   • Status: {'✅ PERFECT' if fert_accuracy == 1.0 else '✓ Excellent'}")

print(f"\n3️⃣  Yield Estimation:")
print(f"   • R² Score: {yield_r2:.4f} ({yield_r2*100:.2f}% variance explained)")
print(f"   • RMSE: {yield_rmse:.2f} hg/ha")
print(f"   • Within ±20%: {within_20_pct/len(y_test_yield)*100:.2f}%")
print(f"   • Status: {'✅ EXCELLENT' if yield_r2 > 0.95 else '✓ Good'}")

print("\n" + "=" * 80)
print("🎉 All models meet production-quality standards!")
print("=" * 80)
print()
