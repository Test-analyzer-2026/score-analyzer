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

    with 
