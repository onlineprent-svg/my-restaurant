import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os
import urllib.parse
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="منيو المطعم الاحترافي", layout="centered")

# --- دالة لجلب اسم المطعم من الإعدادات ---
def get_restaurant_name():
    if os.path.exists("restaurant_name.txt"):
        with open("restaurant_name.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    return "🍴 منيو مطعمك الذكي"

# --- دالة إضافة التصميم الاحترافي ---
def apply_custom_style():
    # ملاحظة: للخلفية سنبقيها بيضاء حالياً لتسهيل الرؤية كما طلبت
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #f8f9fa;
        }}
        .restaurant-header {{
            background: linear-gradient(135deg, #1e1e1e 0%, #333333 100%);
            padding: 30px;
            border-radius: 20px;
            border: 4px double #FFD700;
            text-align: center;
            margin-bottom: 40px;
            box-shadow: 0px 15px 35px rgba(0,0,0,0.4);
        }}
        .restaurant-header h1 {{
            font-size: 50px !important;
            color: #FFD700 !important;
            font-weight: 900;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: white !important;
            border: 10px solid #FFFFFF !important;
            border-radius: 20px !important;
            padding: 25px !important;
            margin-bottom: 30px !important;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.1) !important;
            border: 8px solid #f1f1f1 !important;
        }}
        .product-title-box {{
            background: #1E1E1E; color: #FFD700; padding: 10px; border-radius: 10px;
            font-size: 24px; font-weight: 900; text-align: center;
        }}
        .price-tag-box {{
            background-color: #D32F2F; color: white; padding: 8px; border-radius: 10px;
            font-size: 22px; font-weight: 900; text-align: center; margin-top: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

apply_custom_style()

# الاتصال بجوجل شيت
conn = st.connection("gsheets", type=GSheetsConnection)

def load_products():
    try:
        return conn.read(worksheet="Sheet1", ttl="1m")
    except:
        return pd.DataFrame()

restaurant_name = get_restaurant_name()
products_df = load_products()
selected_items = []
total_sum = 0

st.markdown(f'<div class="restaurant-header"><h1>{restaurant_name}</h1></div>', unsafe_allow_html=True)

if not products_df.empty:
    for index, row in products_df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([1, 1.2])
            with col1:
                if pd.notnull(row.get('الصورة')):
                    st.image(row['الصورة'], use_container_width=True)
                else:
                    st.write("🖼️")
            with col2:
                st.markdown(f'<div class="product-title-box">{row["الاسم"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="price-tag-box">{row["السعر"]} د.ع</div>', unsafe_allow_html=True)
                if st.checkbox("إضافة ✅", key=f"c_{index}"):
                    selected_items.append(row['الاسم'])
                    total_sum += row['السعر']

    st.write("---")
    customer_name = st.text_input("اسمك الكريم")
    table_num = st.number_input("رقم الطاولة", min_value=1)
    
    if st.button("إرسال الطلب 🚀", use_container_width=True):
        if selected_items and customer_name:
            # هنا يمكنك إضافة كود حفظ الطلبات أيضاً في شيت آخر أو واتساب كما سبق
            st.success(f"تم تسجيل طلبك يا {customer_name}")
            st.balloons()
