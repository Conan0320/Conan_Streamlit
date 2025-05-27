import streamlit as st
from modules.data_loader import load_profile
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid
import datetime
import os
from PIL import Image

def profile_component():
    # 三栏布局（参考Mainpage.py）
    col1, col2, col3 = st.columns([1.3, 0.2, 1])
    
    with col1:
        # 个人信息卡片
        st.markdown("""
        <div style='padding:20px; background-color:rgba(240,242,246,0.8); border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1)'>
            <h3>王珂楠 WANG Kenan</h3>
            <p>🎓 香港中文大学 市场营销硕士</p>
            <p>📍 中国香港/上海</p>
            <p>📧 <a href="mailto:wangkenan2024@163.com">wangkenan2024@163.com</a></p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # 头像显示
        image_path = os.path.join("Self_picture.jpg")
        if os.path.exists(image_path):
            st.image(image_path, width=300, caption="Conan")
        else:
            st.warning("头像图片未找到")
    
    # 职业发展部分
    st.header("🧩 职业拼图", divider="rainbow")
    col4, col5 = st.columns(2)
    
    with col4:
        st.subheader("🎯 主业（校招待入职）")
        st.markdown("""
        - **抖音集团** - 用户增长产品运营
        - 负责用户增长策略与数据分析
        - **实习经历** - 喜马拉雅/阳狮/欧莱雅/淘天集团
        """)
        
    with col5:
        st.subheader("📺 自媒体博主")
        st.markdown("""
        Kpop音乐区博主
         <p>b站 <a href="https://space.bilibili.com/457893260" target="_blank">@1Conannnn</a></p>
         <p>油管 <a href="https://www.youtube.com/@Kill1Conannnn" target="_blank">@Kill1Conannnn</a></p>
        """, unsafe_allow_html=True)
    
    # 技能部分
    st.header("🔨 专业技能", divider="rainbow")
    skills = ["Python数据分析", "R语言", "大数据营销", "消费者行为分析", "电商用户运营", "视频剪辑", "辩论"]
    cols = st.columns(3)
    for i, skill in enumerate(skills):
        cols[i%3].button(skill, use_container_width=True)

    # 兴趣爱好
    st.header("🎠 兴趣爱好", divider="rainbow")
    skills = ["KPOP音乐", "电影", "博弈游戏", "女性主义", "存在主义", "阅读"]
    cols = st.columns(3)
    for i, skill in enumerate(skills):
        cols[i%3].button(skill, use_container_width=True)

def bilibili_dashboard():
    # 三栏布局
    col1, col2, col3 = st.columns([1.3, 0.2, 1])
    
    with col1:
        # 个人信息卡片
        st.markdown("""
        <div style='padding:20px; background-color:rgba(240,242,246,0.8); border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1)'>
            <h3>1Conannnn</h3>
            <p>b站Kpop音乐区博主</p>
            <p>努力寻找浪潮中的珍珠，女团音乐全肯定剪辑力无限进步中</p>
            <p>Stan：Yves/Ryujin/Kotone/Doeun/Jvcki Wai</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # 头像显示
        channel_path = "1Conannnn.JPG"
        st.image(channel_path, width=300, caption="@1Conannnn")
       
        
    # 加载数据
    st.header("📊 视频数据看板", divider="rainbow")

    history = pd.read_csv("频道历史数据.csv")
    videos = pd.read_csv("热门稿件数据.csv")
    
    # 确保日期列是datetime类型
    history['时间'] = pd.to_datetime(history['时间'])
    
    # 时间范围选择器
    date_range = st.date_input(
        "选择日期范围",
        value=[history['时间'].min().date(), history['时间'].max().date()],
        min_value=history['时间'].min().date(),
        max_value=history['时间'].max().date()
    )
    # 根据选择过滤数据
    mask = (history['时间'].dt.date >= date_range[0]) & (history['时间'].dt.date <= date_range[1])
    filtered_history = history.loc[mask]

    # 下拉框选择看板类型
    dashboard_type = st.selectbox(
        "选择看板类型",
        ("粉丝数趋势", "播放量趋势", "互动数据趋势")
    )

    if dashboard_type == "粉丝数趋势":
        fig = px.line(filtered_history, x='时间', y='累计粉丝', title='粉丝增长趋势')
        st.plotly_chart(fig, use_container_width=True)
    elif dashboard_type == "播放量趋势":
        fig = px.line(filtered_history, x='时间', y='播放量', title='播放量趋势')
        st.plotly_chart(fig, use_container_width=True)
    elif dashboard_type == "互动数据趋势":
        # 互动数据合并为一张图
        fig = px.line(
            filtered_history,
            x='时间',
            y=['点赞', '收藏', '硬币', '评论', '弹幕', '分享'],
            title='互动数据趋势'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.header("🆚 视频三维对比", divider="rainbow")
    # 视频数据三维散点图
    fig2 = px.scatter_3d(videos, x='播放量', y='点赞量', z='收藏量', color='视频标题')
    st.plotly_chart(fig2, use_container_width=True)
    
    # 交互式表格
    # AgGrid(videos)  # 可以注释掉原表格

    # 热门视频瀑布流（多列）展示
    import json
    import os

    st.header("🔥 视频代表作", divider="rainbow")

    # 加载并展示热门视频数据
    def load_hot_videos():
        try:
            with open("hot_video.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"热门视频数据加载失败: {e}")
            return []

    def get_cover_image(cover_path):
        default_img = "https://static.hdslb.com/images/akari.jpg"
        if not cover_path:
            return default_img
        return cover_path if cover_path.startswith("http") or os.path.exists(cover_path) else default_img

    hot_videos = load_hot_videos()
    
    if hot_videos:
        cols = st.columns(2)
        for idx, video in enumerate(hot_videos):
            with cols[idx % 2]:
                cover_url = get_cover_image(video.get("cover_url", ""))
                st.image(cover_url, use_column_width=True)
                bilibili_url = video.get("bilibili_url", "")
                st.markdown(
                    f"""
                    <div style='background:rgba(248,249,250,0.95);border-radius:12px;padding:10px 8px;margin-bottom:18px;box-shadow:0 2px 8px rgba(44,62,80,0.08);text-align:center;'>
                        <div style="font-weight:600;font-size:1.05rem;margin-bottom:6px;color:#222;">{video.get('title', '')}</div>
                        <div style="color:#666;font-size:0.95rem;">播放量：{video.get('views', '-')} &nbsp; 点赞量：{video.get('likes', '-')}</div>
                        <div style="margin-top:6px;">
                            <a href="{bilibili_url}" target="_blank" style="color:#1e88e5;font-size:0.95rem;">B站直达</a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("暂无热门视频数据")

def contact_form():
    with st.form("contact_form"):
        name = st.text_input("姓名*")
        email = st.text_input("邮箱*")
        message = st.text_area("留言*")
        attachment = st.file_uploader("附件(PDF/Word, 最大50MB)", type=['pdf', 'docx'])
        
        if st.form_submit_button("提交"):
            if not all([name, email, message]):
                st.error("请填写所有必填字段")
            else:
                st.success("提交成功！")