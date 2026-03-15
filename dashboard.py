import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os

st.set_page_config(page_title="إدارة المطعم - جوجل شيت", layout="wide")

# الاتصال
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📞 إدارة المنتجات عبر Google Sheets")

# عرض المنتجات الحالية
df = conn.read(worksheet="Sheet1", ttl="0")
st.subheader("المنتجات الحالية في الجدول:")
st.dataframe(df, use_container_width=True)

# إضافة منتج جديد
st.divider()
st.subheader("➕ إضافة وجبة جديدة")
with st.form("add_form"):
    name = st.text_input("اسم الوجبة")
    price = st.number_input("السعر", min_value=0)
    img_url = st.text_input("رابط الصورة (ضع رابطاً مباشراً من الإنترنت أو ImgBB)")
    submit = st.form_submit_button("إضافة للجدول ✅")
    
    if submit and name:
        new_row = pd.DataFrame([{"الاسم": name, "السعر": price, "الصورة": img_url}])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        st.success("تم التحديث! سيظهر المنتج في المنيو خلال لحظات.")
        st.rerun()
