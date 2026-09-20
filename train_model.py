from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "device_data_ai.csv"
MODEL_FILE = BASE_DIR / "digital_twin_model.pkl"

FEATURES = [
    "cpu_load",
    "memory_usage",
    "temperature",
    "battery",
    "network_latency",
]
TARGET = "anomaly"


def main():
    if not DATA_FILE.exists():
        print(f"Dataset not found: {DATA_FILE}")
        print("Run: python generate_dataset.py")
        return

    df = pd.read_csv(DATA_FILE)
    X = df[FEATURES]
    y = df[TARGET]

    print("=" * 60)
    print("DATASET")
    print("=" * 60)
    print(f"Rows: {len(df)}")
    print(y.value_counts().rename({0: "normal", 1: "fault"}).to_string())

    # Sanity check: do the features actually differ between the two classes?
    print("\nMean feature values by class:")
    print(df.groupby(TARGET)[FEATURES].mean().round(2).to_string())
    print("(If these two rows look identical, the labels are not learnable.)")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )

    # max_depth is capped so the forest generalises instead of memorising.
    # It also keeps the saved model small enough to commit sensibly.
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    baseline = max((y_test == 0).mean(), (y_test == 1).mean())

    print("\n" + "=" * 60)
    print("HELD-OUT TEST RESULTS")
    print("=" * 60)
    print(f"Accuracy          : {accuracy_score(y_test, predictions):.3f}")
    print(f"Majority baseline : {baseline:.3f}   <- must beat this")
    print(f"ROC-AUC           : {roc_auc_score(y_test, probabilities):.3f}   (0.5 = coin flip)")

    print("\nConfusion matrix (rows = actual, cols = predicted):")
    print(confusion_matrix(y_test, predictions))

    print("\n" + classification_report(
        y_test, predictions, target_names=["NORMAL", "FAULT"]
    ))

    cv = cross_val_score(
        model, X, y,
        cv=StratifiedKFold(5, shuffle=True, random_state=42),
        scoring="roc_auc",
    )
    print(f"5-fold CV ROC-AUC : {cv.mean():.3f} (+/- {cv.std():.3f})")

    print("\nFeature importance:")
    importance = pd.Series(model.feature_importances_, index=FEATURES)
    print(importance.sort_values(ascending=False).round(3).to_string())

    joblib.dump(model, MODEL_FILE, compress=3)
    size_mb = MODEL_FILE.stat().st_size / 1_000_000
    print(f"\nModel saved to {MODEL_FILE} ({size_mb:.2f} MB)")

    # Does the model actually fire on the scenarios fault_stimulation.py injects?
    print("\n" + "=" * 60)
    print("SANITY CHECK ON INJECTED FAULT SCENARIOS")
    print("=" * 60)
    scenarios = {
        "idle / normal":  [30, 40, 40, 100, 20],
        "CPU overload":   [95, 45, 55, 90, 25],
        "memory overload": [35, 95, 50, 90, 22],
        "overheating":    [40, 40, 92, 90, 20],
        "network failure": [35, 40, 40, 95, 400],
        "low battery":    [35, 40, 40, 5, 20],
    }
    for name, values in scenarios.items():
        row = pd.DataFrame([values], columns=FEATURES)
        label = "FAULT " if model.predict(row)[0] == 1 else "NORMAL"
        prob = model.predict_proba(row)[0][1] * 100
        print(f"  {name:17s} -> {label}  (fault probability {prob:5.1f}%)")


if __name__ == "__main__":
    main()