import pandas as pd

# データ入力
subjects = [
    "国語総合",
    "数学Ⅱ",
    "数学B",
    "英語コミュ",
    "英語論理",
    "化学",
    "物理"
]

scores = [75, 92, 70, 78, 85, 64, 65]
averages = [62.5, 66.6, 57.2, 51.3, 60.1, 50.3, 57.3]

# 仮の標準偏差推定関数
def estimate_sd(avg):

    if 45 <= avg <= 55:
        return 18

    elif 35 <= avg < 45:
        return 15

    elif 55 < avg <= 65:
        return 15

    else:
        return 12

# 偏差値計算
def hensachi(score, avg, sd):
    return round(50 + 10 * (score - avg) / sd, 1)

result = []

for sub, score, avg in zip(subjects, scores, averages):

    sd = estimate_sd(avg)

    dev = hensachi(score, avg, sd)

    result.append(
        [sub, score, avg, sd, dev]
    )

df = pd.DataFrame(
    result,
    columns=[
        "科目",
        "得点",
        "平均点",
        "推定標準偏差",
        "推定偏差値"
    ]
)

display(df)
