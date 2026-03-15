import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="إدارة مطعم كربلاء الاحترافية", layout="wide", initial_sidebar_state="expanded")

# تهيئة المجلدات والملفات الضرورية
if not os.path.exists("images"): os.makedirs("images")
PRODUCTS_FILE = "products.csv"
ORDERS_FILE = "orders.csv"
COMPLETED_ORDERS_FILE = "completed_orders.csv"
BG_CONFIG_FILE = "bg_config.txt"
NUMBERS_FILE = "numbers.txt" 
NAME_CONFIG_FILE = "restaurant_name.txt" # ملف حفظ اسم المطعم

def load_data(file):
    return pd.read_csv(file) if os.path.exists(file) else pd.DataFrame()

# --- دالة التنبيه الصوتي (الجرس) ---
def play_bell_sound():
    sound_url = "https://www.soundjay.com/buttons/sounds/button-37a.mp3"
    st.components.v1.html(
        f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/mp3">
        </audio>
        """,
        height=0,
    )

# --- نظام مراقبة الطلبات الجديدة ---
if "last_order_count" not in st.session_state:
    df_temp = load_data(ORDERS_FILE)
    st.session_state.last_order_count = len(df_temp)

current_df = load_data(ORDERS_FILE)
if len(current_df) > st.session_state.last_order_count:
    play_bell_sound() 
    st.toast("🔔 تنبيه: وصل طلب جديد الآن!", icon="🔥")
    st.session_state.last_order_count = len(current_df)

# 2. القائمة الجانبية المحدثة
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3448/3448650.png", width=100)
    st.title("لوحة التحكم الذكية")
    st.markdown("---")
    menu_option = st.radio(
        "انتقل إلى:",
        [
            "➕ إضافة منتج جديد", 
            "📥 الطلبات الواردة", 
            "✅ الطلبات المنجزة",
            "📦 إدارة المنيو", 
            "🎨 إعدادات المظهر", 
            "📞 أرقام الواتساب"
        ],
        index=1
    )
    
    if st.button("تحديث الحالة 🔄", use_container_width=True):
        st.rerun()

# --- الخيار الأول: إضافة منتج جديد ---
if menu_option == "➕ إضافة منتج جديد":
    st.header("✨ إضافة وجبة جديدة للمنيو")
    with st.container(border=True):
        with st.form("add_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            name = col1.text_input("اسم المنتج")
            price = col2.number_input("السعر بالدينار", min_value=0)
            uploaded_file = st.file_uploader("الصورة من الجهاز", type=['jpg', 'png', 'jpeg'])
            if st.form_submit_button("اعتماد في المنيو 🚀", use_container_width=True):
                if name and uploaded_file:
                    img_path = os.path.join("images", uploaded_file.name)
                    with open(img_path, "wb") as f: f.write(uploaded_file.getbuffer())
                    new_item = pd.DataFrame([{"الاسم": name, "السعر": price, "الصورة": img_path}])
                    new_item.to_csv(PRODUCTS_FILE, mode='a', header=not os.path.exists(PRODUCTS_FILE), index=False)
                    st.success(f"تمت إضافة {name} بنجاح!")

# --- الخيار الثاني: الطلبات الواردة ---
elif menu_option == "📥 الطلبات الواردة":
    st.header("🔔 الطلبات الحالية")
    df_o = load_data(ORDERS_FILE)
    if not df_o.empty:
        st.session_state.last_order_count = len(df_o)
        for idx, order in df_o.iterrows():
            with st.container(border=True):
                st.subheader(f"📍 طاولة {order['الطاولة']} - {order['الزبون']}")
                st.write(f"📦 الطلبات: {order['الطلبات']}")
                if st.button("تم التحضير ✅", key=f"d_{idx}"):
                    completed_order = pd.DataFrame([order])
                    completed_order.to_csv(COMPLETED_ORDERS_FILE, mode='a', header=not os.path.exists(COMPLETED_ORDERS_FILE), index=False)
                    df_o = df_o.drop(idx)
                    df_o.to_csv(ORDERS_FILE, index=False)
                    st.session_state.last_order_count = len(df_o)
                    st.rerun()
    else: st.info("لا توجد طلبات واردة حالياً.")

# --- الخيار الثالث: الطلبات المنجزة ---
elif menu_option == "✅ الطلبات المنجزة":
    st.header("📜 سجل الطلبات المنجزة")
    df_c = load_data(COMPLETED_ORDERS_FILE)
    if not df_c.empty:
        st.dataframe(df_c, use_container_width=True)
        if st.button("مسح سجل المنجز 🧹"):
            os.remove(COMPLETED_ORDERS_FILE)
            st.rerun()
    else: st.info("السجل فارغ.")

# --- الخيار الرابع: إدارة المنيو ---
elif menu_option == "📦 إدارة المنيو":
    st.header("📋 المنتجات المتوفرة")
    df_p = load_data(PRODUCTS_FILE)
    if not df_p.empty:
        for idx, row in df_p.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 3, 1])
                c1.image(row['الصورة'], width=80)
                c2.markdown(f"### {row['الاسم']} \n **السعر:** {row['السعر']} د.ع")
                if c3.button("حذف 🗑️", key=f"p_{idx}"):
                    df_p.drop(idx).to_csv(PRODUCTS_FILE, index=False); st.rerun()

# --- الخيار الخامس: إعدادات المظهر (تحديث شامل) ---
elif menu_option == "🎨 إعدادات المظهر":
    st.header("🎨 تخصيص واجهة المنيو")
    
    # 1. تغيير اسم المطعم
    st.subheader("إعدادات الهوية")
    current_name = ""
    if os.path.exists(NAME_CONFIG_FILE):
        with open(NAME_CONFIG_FILE, "r", encoding="utf-8") as f: current_name = f.read()
    
    res_name = st.text_input("اسم المطعم الحالي", value=current_name)
    if st.button("حفظ اسم المطعم"):
        with open(NAME_CONFIG_FILE, "w", encoding="utf-8") as f: f.write(res_name)
        st.success("تم تحديث اسم المطعم!")

    st.divider()
    
    # 2. تغيير الخلفية
    st.subheader("صورة الخلفية")
    bg_file = st.file_uploader("اختر خلفية جديدة للمنيو", type=['jpg', 'png', 'jpeg'])
    if st.button("تحديث الخلفية 🖼️"):
        if bg_file:
            path = os.path.join("images", "background.jpg")
            with open(path, "wb") as f: f.write(bg_file.getbuffer())
            with open(BG_CONFIG_FILE, "w") as f: f.write(path)
            st.success("تم تحديث الخلفية!")

# --- الخيار السادس: أرقام الواتساب ---
elif menu_option == "📞 أرقام الواتساب":
    st.header("📞 إدارة أرقام الاستلام")
    with st.container(border=True):
        new_no = st.text_input("الرقم (بدون + مثلاً 9647700000000)")
        if st.button("إضافة الرقم"):
            if new_no:
                with open(NUMBERS_FILE, "a") as f: f.write(new_no + "\n")
                st.rerun()

    if os.path.exists(NUMBERS_FILE):
        with open(NUMBERS_FILE, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                c1, c2 = st.columns([3, 1])
                c1.write(f"📱 {line.strip()}")
                if c2.button("حذف", key=f"n_{i}"):
                    lines.pop(i)
                    with open(NUMBERS_FILE, "w") as fn: fn.writelines(lines)
                    st.rerun()
