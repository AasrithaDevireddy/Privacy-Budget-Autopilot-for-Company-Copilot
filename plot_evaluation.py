import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
OUT = REPORTS / "graphs"
OUT.mkdir(parents=True, exist_ok=True)

with open(REPORTS / "evaluation_validation.json", encoding="utf-8") as f:
    validation = json.load(f)

with open(REPORTS / "evaluation_test.json", encoding="utf-8") as f:
    test = json.load(f)

# Graph 1: Overall evaluation comparison
metrics = ["Accuracy", "Macro F1"]
val_scores = [
    validation["accuracy"] * 100,
    validation["macro_f1"] * 100,
]
test_scores = [
    test["accuracy"] * 100,
    test["macro_f1"] * 100,
]

x = np.arange(len(metrics))
width = 0.34

fig, ax = plt.subplots(figsize=(8, 5))
bars1 = ax.bar(x - width / 2, val_scores, width, label="Validation")
bars2 = ax.bar(x + width / 2, test_scores, width, label="Test")

ax.set_title("Privacy Budget Autopilot: Evaluation Performance")
ax.set_ylabel("Score (%)")
ax.set_xticks(x, metrics)
ax.set_ylim(0, 105)
ax.legend()
ax.bar_label(bars1, fmt="%.2f%%", padding=3)
ax.bar_label(bars2, fmt="%.2f%%", padding=3)
fig.tight_layout()
fig.savefig(OUT / "overall_performance.png", dpi=300)
plt.close(fig)

# Graph 2: Per-action precision, recall and F1 on test data
actions = [item["action"] for item in test["per_action"]]
precision = [item["precision"] * 100 for item in test["per_action"]]
recall = [item["recall"] * 100 for item in test["per_action"]]
f1 = [item["f1"] * 100 for item in test["per_action"]]

y = np.arange(len(actions))
height = 0.24

fig, ax = plt.subplots(figsize=(11, 6))
ax.barh(y - height, precision, height, label="Precision")
ax.barh(y, recall, height, label="Recall")
ax.barh(y + height, f1, height, label="F1-score")

ax.set_title("Test Performance by Privacy Action")
ax.set_xlabel("Score (%)")
ax.set_yticks(y, actions)
ax.set_xlim(0, 110)
ax.invert_yaxis()
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "per_action_performance.png", dpi=300)
plt.close(fig)

# Graph 3: Test confusion matrix
cm = np.array(test["confusion_matrix"])
fig, ax = plt.subplots(figsize=(10, 8))
image = ax.imshow(cm, interpolation="nearest", aspect="auto")
fig.colorbar(image, ax=ax, label="Number of samples")

ax.set(
    title="Test Confusion Matrix",
    xlabel="Predicted action",
    ylabel="Actual action",
    xticks=np.arange(len(actions)),
    yticks=np.arange(len(actions)),
)
ax.set_xticklabels(actions, rotation=45, ha="right")
ax.set_yticklabels(actions)

threshold = cm.max() / 2
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(
            j, i, str(cm[i, j]),
            ha="center", va="center",
            color="white" if cm[i, j] > threshold else "black",
        )

fig.tight_layout()
fig.savefig(OUT / "confusion_matrix_test.png", dpi=300)
plt.close(fig)

# Graph 4: Safety and policy-enforcement metrics
safety_labels = [
    "Raw model unsafe\ndisclosure rate",
    "Post-policy unsafe\ndisclosure rate",
    "Policy compliance",
]
safety_values = [
    test["raw_model_unsafe_disclosure_rate"] * 100,
    test["unsafe_disclosure_rate"] * 100,
    test["policy_compliance_rate"] * 100,
]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(safety_labels, safety_values)
ax.set_title("Test Safety and Policy Metrics")
ax.set_ylabel("Rate (%)")
ax.set_ylim(0, 110)
ax.bar_label(bars, labels=[f"{v:.2f}%" for v in safety_values], padding=3)
fig.tight_layout()
fig.savefig(OUT / "safety_policy_metrics.png", dpi=300)
plt.close(fig)

print("\nGraphs generated successfully:")
for path in sorted(OUT.glob("*.png")):
    print(f"  {path}")
