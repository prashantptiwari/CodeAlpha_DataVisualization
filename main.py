"""
CodeAlpha Task 2: Data Visualization

Objective:
Create charts to compare student scores, subject performance,
attendance, and score distributions.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "student_performance.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


def main():
    # 1. Load the dataset
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Create the data folder and add "
            "student_performance.csv."
        )

    df = pd.read_csv(DATA_PATH)

    # 2. Calculate average scores
    score_columns = [
        "math_score",
        "science_score",
        "english_score"
    ]

    df["average_score"] = df[score_columns].mean(axis=1)

    sns.set_theme(style="whitegrid")

    # 3. Subject-wise average comparison
    subject_means = df[score_columns].mean()

    subject_means.index = [
        "Math",
        "Science",
        "English"
    ]

    plt.figure(figsize=(8, 5))

    ax = sns.barplot(
        x=subject_means.index,
        y=subject_means.values
    )

    ax.set_title("Average Score by Subject")
    ax.set_xlabel("Subject")
    ax.set_ylabel("Average Score out of 100")
    ax.set_ylim(0, 100)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "subject_average_comparison.png",
        dpi=150
    )
    plt.close()

    # 4. Compare individual student averages
    sorted_df = df.sort_values(
        "average_score",
        ascending=False
    )

    plt.figure(figsize=(12, 6))

    sns.barplot(
        data=sorted_df,
        x="student_name",
        y="average_score"
    )

    plt.title("Student Average Scores")
    plt.xlabel("Student")
    plt.ylabel("Average Score")

    plt.xticks(rotation=60, ha="right")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "student_average_scores.png",
        dpi=150
    )
    plt.close()

    # 5. Attendance vs average score
    plt.figure(figsize=(8, 5))

    sns.regplot(
        data=df,
        x="attendance_percent",
        y="average_score"
    )

    plt.title("Attendance vs Average Score")
    plt.xlabel("Attendance Percentage")
    plt.ylabel("Average Score")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "attendance_vs_score.png",
        dpi=150
    )
    plt.close()

    # 6. Compare subject score distributions
    long_df = df.melt(
        id_vars=["student_name"],
        value_vars=score_columns,
        var_name="subject",
        value_name="score"
    )

    subject_names = {
        "math_score": "Math",
        "science_score": "Science",
        "english_score": "English"
    }

    long_df["subject"] = long_df["subject"].map(
        subject_names
    )

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=long_df,
        x="subject",
        y="score"
    )

    plt.title("Score Distribution by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Score")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "subject_score_distribution.png",
        dpi=150
    )
    plt.close()

    # 7. Generate insights report
    report_path = OUTPUT_DIR / "visualization_insights.txt"

    highest = sorted_df.iloc[0]
    lowest = sorted_df.iloc[-1]

    with report_path.open("w", encoding="utf-8") as file:
        file.write("CODEALPHA - DATA VISUALIZATION REPORT\n")
        file.write("=" * 42 + "\n\n")

        file.write("Average scores by subject:\n")
        file.write(subject_means.round(2).to_string())
        file.write("\n\n")

        file.write(
            f"Overall average score: "
            f"{df['average_score'].mean():.2f}\n"
        )

        file.write(
            f"Highest average: {highest['student_name']} "
            f"({highest['average_score']:.2f})\n"
        )

        file.write(
            f"Lowest average: {lowest['student_name']} "
            f"({lowest['average_score']:.2f})\n\n"
        )

        file.write("Chart interpretation:\n")
        file.write(
            "1. The subject comparison chart shows mean scores.\n"
            "2. The student chart compares average performance.\n"
            "3. The attendance chart shows the relationship between "
            "attendance and average scores.\n"
            "4. The box plot compares score distributions by subject.\n\n"
        )

        file.write(
            "Note: This is a small illustrative dataset. "
            "Relationships do not prove causation, and the "
            "results cannot be generalized to all students.\n"
        )

    print("\nData Visualization completed successfully!")
    print("Four charts and an insights report were saved in:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()