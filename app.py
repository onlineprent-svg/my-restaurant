import streamlit as st
import pandas as pd
import os
import urllib.parse

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="مطعم الحجي - كربلاء", layout="centered")

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #fdfdfd; }
        .restaurant-header {
            background: #1e1e1e; padding: 25px; border-radius: 15px;
            border: 3px solid #FFD700; text-align: center; margin-bottom: 30px;
        }
        .restaurant-header h1 { color: #FFD700 !important; font-size: 45px !important; }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: white !important; border-radius: 15px !important;
            padding: 20px !important; margin-bottom: 25px !important;
            border: 2px solid #eeeeee !important; box-shadow: 0px 4px 12px rgba(0,0,0,0.05) !important;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# 2. تحميل البيانات
if os.path.exists("products.csv"):
    df = pd.read_csv("products.csv")
else:
    df = pd.DataFrame(columns=["الاسم", "السعر", "الصورة"])

# 3. عرض المنيو
st.markdown('<div class="restaurant-header"><h1>🍴 مطعم الحجي</h1></div>', unsafe_allow_html=True)

selected_items = []
total_sum = 0

if not df.empty:
    for index, row in df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([1, 1.2])
            with col1:
                if os.path.exists(str(row['الصورة'])):
                    st.image(row['الصورة'], use_container_width=True)
                else:
                    st.write("🖼️ صورة الوجبة")
            with col2:
                st.markdown(f"<h2 style='color:#1e1e1e;'>{row['الاسم']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='color:#D32F2F;'>{row['السعر']} د.ع</h3>", unsafe_allow_html=True)
                if st.checkbox("إضافة للطلب", key=f"item_{index}"):
                    selected_items.append(row['الاسم'])
                    total_sum += row['السعر']

# 4. إتمام الطلب (واتساب فقط)
if selected_items:
    st.divider()
    customer_name = st.text_input("اسمك")
    if st.button("إرسال الطلب عبر واتساب 🚀", use_container_width=True):
        if customer_name:
            items_str = "\n".join([f"- {i}" for i in selected_items])
            msg = f"*طلب جديد*\n*الزبون:* {customer_name}\n*المجموع:* {total_sum}\n*الطلبات:*\n{items_str}"
            # سيتم جلب الرقم من ملف numbers.txt إذا وجد
            num = "964..." # ضع رقمك هنا مؤقتاً
            url = f"https://wa.me/{num}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank" style="text-decoration:none; color:white; background:#25D366; padding:15px; border-radius:10px; display:block; text-align:center;">اضغط هنا للتأكيد عبر واتساب</a>', unsafe_allow_html=True)
