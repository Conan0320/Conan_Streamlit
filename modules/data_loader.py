import streamlit as st

@st.cache_data
def load_profile():
    with open("profile.md", "r", encoding="utf-8") as f:
        return f.read()

@st.cache_data
def load_bilibili_data():
    # 这里可以添加B站API调用的代码
    pass