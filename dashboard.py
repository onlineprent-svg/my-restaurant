import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="لوحة تحكم مطعم الحجي", layout="wide")

PRODUCTS_FILE = "products.csv"
NUMBERS_FILE = "numbers.txt"

# دالة لتحميل البيانات
def load_data(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame()

# 2. القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الإدارة")
    option = st.radio("انتقل إلى:", ["📦 إدارة المنتجات", "📞 أرقام الواتساب"])

# --- القسم الأول: إدارة المنتجات ---
if option == "📦 إدارة المنتجات":
    st.header("📊 قائمة الطعام الحالية")
    df = load_data(PRODUCTS_FILE)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        st.subheader("🗑️ حذف منتج")
        product_to_del = st.selectbox("اختر المنتج المراد حذفه", df['الاسم'].tolist())
        if st.button("تأكيد الحذف"):
            df = df[df['الاسم'] != product_to_del]
            df.to_csv(PRODUCTS_FILE, index=False)
            st.success(f"تم حذف {product_to_del} بنجاح!")
            st.rerun()
    else:
        st.info("لا توجد منتجات حالياً في ملف products.csv")

    st.divider()
    st.subheader("➕ إضافة منتج جديد")
    with st.form("add_product"):
        new_name = st.text_input("اسم الوجبة")
        new_price = st.number_input("السعر (د.ع)", min_value=0)
        new_img = st.text_input("مسار الصورة (مثلاً: images/burger.jpg)")
        submit = st.form_submit_button("إضافة للمنيو")
        
        if submit and new_name:
            new_row = pd.DataFrame([{"الاسم": new_name, "السعر": new_price, "الصورة": new_img}])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(PRODUCTS_FILE, index=False)
            st.success("تمت الإضافة! (تذكر: الإضافة من هنا مؤقته على السيرفر المجاني)")

# --- القسم الثاني: أرقام الواتساب ---
elif option == "📞 أرقام الواتساب":
    st.header("📞 رقم استلام الطلبات")
    if os.path.exists(NUMBERS_FILE):
        with open(NUMBERS_FILE, "r") as f:
            current_num = f.read().strip()
    else:
        current_num = "لا يوجد رقم مسجل"
    
    st.write(f"الرقم الحالي: `{current_num}`")
    
    new_num = st.text_input("أدخل الرقم الجديد (مثلاً: 9647700000000)")
    if st.button("حفظ الرقم"):
        with open(NUMBERS_FILE, "w") as f:
            f.write(new_num)
        st.success("تم تحديث الرقم!")
        st.rerun()
