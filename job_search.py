#!/usr/bin/env python
# coding: utf-8

# In[64]:


import pandas as pd
import streamlit as st
import plotly.express as px


# In[65]:


# job.csvを読み込む
job_df = pd.read_csv("job.csv")


# In[66]:


# 給与から数値を抽出して時給列を作成
job_df["時給"] = (
    job_df["給与"]
    .str.extract(r'(\d[\d,]*)')[0]
    .str.replace(',', '', regex=False)
)

job_df["時給"] = pd.to_numeric(
    job_df["時給"],
    errors="coerce"
)


# In[67]:


# 列名確認
st.write(job_df.columns)

# 時給列作成
job_df["時給"] = (
    job_df["給与"]
    .str.extract(r'(\d[\d,]*)')[0]
    .str.replace(',', '', regex=False)
)

job_df["時給"] = pd.to_numeric(job_df["時給"], errors="coerce")

# 確認
st.write(job_df[["給与", "時給"]].head())


# In[68]:


# streamlitの部品設計
st.title("ジョブサーチ")

# フィルタ設定
price_limit = st.slider("最低時給の上限", min_value=1060, max_value=2090, step=10, value=1100)
access_limit = st.slider("交通アクセスの下限", min_value=3, max_value=28, step=1, value=6)




# In[69]:


access_limit = st.text_input("駅名・地域名を入力", "金沢")


# In[70]:


# フィルタ処理
filtered_df = job_df[
(job_df['時給'] >= price_limit) &
(job_df['styles_bodytext_ky7'].str.contains(access_limit, na=False))

]


# In[71]:


# 散布図の作成 ( 交通アクセス× 最低時給価格）
fig = px.scatter(
       filtered_df,
       x='時給',
       y='styles_bodytext_ky7',
       hover_data=['タイトル', 'タイトルURL', '画像URL', 'styles_captiontext_rpf1z', '名前', '給与', 'styles_bodytext_ky7', '時給'],
       title='交通アクセスと最低時給価格の散布図'
)

st.plotly_chart(fig)


# In[72]:


# 詳細リンクの表示
selected_job = st.selectbox('気になる求人を選んで詳細を確認', filtered_df['タイトル'])

if selected_job:
    url = filtered_df[filtered_df['タイトル'] == selected_job]['タイトルURL'].values[0]
    st.markdown(f"[{selected_job}のページへ移動]({url})", unsafe_allow_html=True)


# In[73]:


sort_key = st.selectbox(
    "並び替え基準を選んでください",
    ("時給", "タイトル", "名前")
)
ascending = True if sort_key == "時給" else False


# In[74]:


st.subheader(f"{sort_key}による求人ランキング（上位10件）")

ranking_df = filtered_df.sort_values(
    by=sort_key,
    ascending=ascending
).head(10)

st.dataframe(
    ranking_df[
        [
            "タイトル",
            "名前",
            "給与",
            "時給",
            "styles_bodytext_ky7"
        ]
    ]
)


# In[ ]:




