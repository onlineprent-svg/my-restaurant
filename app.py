import streamlit as st
import pandas as pd

st.set_page_config(page_title="منيو مطعم الحجي", layout="centered")

# دالة لجلب البيانات من GitHub مباشرة لضمان المزامنة
@st.cache_data(ttl=60) # يطلب البيانات الجديدة كل دقيقة
def load_data():
    try:
        # استبدل الرابط أدناه برابط ملف products.csv الخاص بك (نسخة Raw من GitHub)
        url = "https://raw.githubusercontent.com/USER_NAME/REPO_NAME/main/products.csv"
        return pd.read_csv(url)
    except:
        return pd.DataFrame(columns=["الاسم", "السعر", "الصورة"])

st.title("🍴 منيو مطعم الحجي")
df = load_data()

if not df.empty:
    for _, row in df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(row['الصورة'], use_container_width=True)
            with col2:
                st.subheader(row['الاسم'])
                st.write(f"السعر: {row['السعر']} د.ع")
else:
    st.warning("جاري تحديث القائمة... يرجى الانتظار")
