import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="統計的偏差値分析アプリ",
    layout="wide"
)

st.title("📊 定期考査 統計的偏差値＆伸びしろ分析")

st.markdown(
    """
    平均点と自分の得点から推定偏差値を算出し、
    復習優先順位を提案します。
    """
)

subjects = [
    "国語総合",
    "数学Ⅱ",
    "数学B",
    "英語コミュ",
    "英語論理",
    "化学",
    "物理"
]

default_scores = [75,92,70,78,85,64,65]
default_avgs = [62.5,66.6,57.2,51.3,60.1,50.3,57.3]

st.header("入力")

data = []

for i, subject in enumerate(subjects):

    col1,col2 = st.columns(2)

    with col1:
        score = st.number_input(
            f"{subject} 得点",
            0.0,
            100.0,
            float(default_scores[i]),
            key=f"s{i}"
        )

    with col2:
        avg = st.number_input(
            f"{subject} 平均点",
            0.0,
            100.0,
            float(default_avgs[i]),
            key=f"a{i}"
        )

    data.append([subject, score, avg])


def estimate_sd(avg):

    if avg >= 65:
        return 12

    elif avg >= 55:
        return 15

    elif avg >= 45:
        return 18

    else:
        return 15


def calculate_hensachi(score, avg, sd):
    return round(
        50 + 10*(score-avg)/sd,
        1
    )


results = []

for subject, score, avg in data:

    sd = estimate_sd(avg)

    hensachi = calculate_hensachi(
        score,
        avg,
        sd
    )

    low = calculate_hensachi(
        score,
        avg,
        sd+3
    )

    high = calculate_hensachi(
        score,
        avg,
        max(8,sd-3)
    )

    results.append(
        [
            subject,
            score,
            avg,
            hensachi,
            low,
            high
        ]
    )


df = pd.DataFrame(
    results,
    columns=[
        "科目",
        "得点",
        "平均点",
        "推定偏差値",
        "下限",
        "上限"
    ]
)

st.header("分析結果")

st.dataframe(df)

weak_subject = df.loc[
    df["推定偏差値"].idxmin(),
    "科目"
]

st.error(
    f"最優先復習科目：{weak_subject}"
)

st.subheader("推定偏差値レーダーチャート")

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=df["推定偏差値"],
        theta=df["科目"],
        fill="toself",
        name="推定偏差値"
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[40,80]
        )
    ),
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("推定偏差値一覧")

for _, row in df.iterrows():

    st.write(
        f"{row['科目']}："
        f"偏差値 {row['推定偏差値']} "
        f"(推定範囲 {row['下限']} ～ {row['上限']})"
    )


with st.expander("📗 本アプリの計算ロジックと統計的限界について"):

    st.markdown("""
### 1. このアプリの計算ロジック

本アプリは、学校で配布される

- 自分の点数
- 学年平均点

という限られた情報から、統計学的な考え方を用いて
「推定偏差値」と「学習上の伸びしろ」を可視化することを目的としています。

実際の偏差値は、

偏差値 = 50 + 10 × (得点 − 平均点) ÷ 標準偏差

によって計算されます。

しかし、多くの高校の定期考査では標準偏差が公表されません。

そのため本アプリでは、テスト平均点と得点分布の一般的傾向をもとに
標準偏差を推定し、その値から推定偏差値を算出しています。

---

### 2. 推定偏差値の幅表示

本アプリでは単一の偏差値だけでなく、

- 推定下限値
- 推定上限値

も同時に表示します。

これは、標準偏差自体が推定値であるためです。

実際の標準偏差が予測より大きい場合と小さい場合を考慮し、
推定偏差値を「範囲（レンジ）」で示しています。

そのため、

偏差値 64.2

よりも

偏差値 62.5 ～ 65.8

のような表示の方が、
現実的な不確実性を反映した結果になります。

---

### 3. 弱点科目の抽出

各科目の推定偏差値を比較し、
相対的に最も低い科目を「最優先復習科目」としています。

これは単純な点数比較ではなく、

「他教科と比べてどこに改善余地があるか」

を見つけることを目的としています。

---

### 4. このアプリの統計的限界

本アプリで表示される偏差値は
『推定値』であり、実際の偏差値とは一致しない場合があります。

理由は以下の通りです。

- 実際の標準偏差が公開されていない
- テストごとに得点分布が異なる
- 得点分布が正規分布とは限らない
- 科目や出題難易度によってばらつきが異なる

したがって、本アプリは
順位や偏差値を正確に予測するものではなく、

『どの科目を優先的に学習すべきかを考えるための意思決定支援ツール』

として利用することを想定しています。

---

### 5. 今後の改善予定

今後は、

- 実データを用いた標準偏差推定モデルの改良
- レーダーチャート分析
- 偏差値目標から必要得点を逆算する機能
- 推定精度の検証

などを実装し、より実用的な学習分析ツールへ発展させる予定です。
""")
