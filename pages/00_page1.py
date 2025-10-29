import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv("./countriesMBTI_16types.csv")

# 퍼센트 변환
for col in df.columns[1:]:
    df[col] = (df[col] * 100).round(2)

# 제목
st.header("🧑🏻‍💻서울고 석리송 선생님과 함께하는! 👩🏻‍💻")
st.title("🌍 국가별 MBTI 성향 분석 프로젝트 🔍")

st.markdown(
    "📊 **데이터 출처**: [Kaggle - MBTI Types by Country](https://www.kaggle.com/datasets/yamaerenay/mbtitypes-full/data)",
    help="MBTI 유형의 국가별 분포 데이터를 Kaggle에서 가져왔습니다."
)

# 국가 선택
global_mbti_types = sorted(set(df.columns) - {"Country"})
country = st.selectbox("🌏 국가를 선택하세요:", df["Country"].unique())

# 선택 국가의 MBTI 분포
st.subheader(f"📊 {country}의 MBTI 분포")
selected_data = df[df["Country"] == country].iloc[:, 1:].T
selected_data.columns = [country]
selected_data = selected_data.sort_values(by=country, ascending=False)

fig = px.bar(
    selected_data, x=selected_data.index, y=country, text=selected_data[country],
    title=f"{country}의 MBTI 분포", labels={country: "비율 (%)"},
    hover_data=[country],
    color=selected_data.index,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig)

# 전체 평균 MBTI
st.subheader("📊 전체 국가의 MBTI 평균 비율")
mbti_avg = df.iloc[:, 1:].mean().sort_values(ascending=False)
mbti_avg_df = pd.DataFrame({"MBTI": mbti_avg.index, "비율 (%)": mbti_avg.values})

fig_avg = px.bar(
    mbti_avg_df, x="MBTI", y="비율 (%)", text="비율 (%)",
    title="전체 국가별 MBTI 평균", labels={"비율 (%)": "평균 비율 (%)"},
    hover_data=["비율 (%)"], color="MBTI",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_avg)

# MBTI 상위 10개국
target_mbti = st.selectbox("💡 MBTI 유형을 선택하세요:", global_mbti_types)
st.subheader(f"🏆 {target_mbti} 비율이 높은 국가 TOP 10 & 한국")

if target_mbti in df.columns:
    try:
        top_10 = df.nlargest(10, target_mbti)[["Country", target_mbti]].copy()
        korea_value = df[df["Country"] == "South Korea"][target_mbti].values[0] if "South Korea" in df["Country"].values else None

        if korea_value is not None:
            korea_data = pd.DataFrame({"Country": ["South Korea"], target_mbti: [korea_value]})
            top_10 = pd.concat([top_10, korea_data])

        top_10 = top_10.sort_values(by=target_mbti, ascending=False)

        # 색상 강조
        colors = ["red" if c == "South Korea" else "#AEC6CF" for c in top_10["Country"]]

        fig_top = px.bar(
            top_10, x="Country", y=target_mbti, text=target_mbti,
            title=f"{target_mbti} 비율 TOP 10 & 한국",
            labels={target_mbti: "비율 (%)"},
            hover_data=[target_mbti],
            color_discrete_sequence=colors
        )
        st.plotly_chart(fig_top)

    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")
else:
    st.error("선택한 MBTI 유형이 데이터에 존재하지 않습니다.")
