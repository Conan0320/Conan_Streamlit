import streamlit as st
from modules.ui_components import profile_component, bilibili_dashboard, contact_form
from modules.data_loader import load_profile, load_bilibili_data
import yaml

# 加载配置
with open('config.yaml') as f:
    config = yaml.safe_load(f)

# 应用设置
st.set_page_config(
    page_title="Conan's Club",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 暗黑/明亮模式切换
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# 主应用
def main():
    # 美化边栏样式
    st.sidebar.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        background-image: linear-gradient(315deg, #f8f9fa 0%, #e9ecef 74%);
        padding: 1.5rem;
    }
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .nav-item {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .nav-item:hover {
        background-color: #e9ecef;
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .nav-item.active {
        background-color: #2c3e50;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    @media (max-width: 768px) {
        .sidebar .sidebar-content {
            padding: 1rem;
        }
        .nav-item {
            padding: 0.5rem 0.75rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<p class="sidebar-title">Conan\'s Club 🪩</p>', unsafe_allow_html=True)

    # 自定义导航栏
    navs = [
        ("关于我(｡ì _ í｡)", "about"),
        ("B站分身(*ˉ︶ˉ*)", "bilibili"),
        ("联系我(≧∇≦)", "contact")
    ]
    if "page" not in st.session_state:
        st.session_state.page = "about"

    # 只保留按钮实现导航
    for nav_name, nav_key in navs:
        if st.sidebar.button(nav_name, key=nav_key):
            st.session_state.page = nav_key

    # 页面内容切换
    if st.session_state.page == "about":
        profile_component()
    elif st.session_state.page == "bilibili":
        bilibili_dashboard()
    elif st.session_state.page == "contact":
        contact_form()

if __name__ == "__main__":
    main()