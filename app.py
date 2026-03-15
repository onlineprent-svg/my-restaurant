import streamlit as st
import pandas as pd
import os
import urllib.parse
import base64
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="منيو المطعم الاحترافي", layout="centered")

# --- دالة لتحويل الصورة المحلية إلى Base64 ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# --- دالة لجلب اسم المطعم من الإعدادات ---
def get_restaurant_name():
    if os.path.exists("restaurant_name.txt"):
        with open("restaurant_name.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    return "🍴 منيو مطعمك الذكي"

# --- دالة إضافة التصميم الاحترافي بالخلفية البيضاء الشفافة ---
def apply_custom_style():
    bg_image_url = ""
    if os.path.exists("bg_config.txt"):
        with open("bg_config.txt", "r") as f:
            bg_path = f.read().strip()
            bin_str = get_base64_of_bin_file(bg_path)
            if bin_str:
                bg_image_url = f"data:image/png;base64,{bin_str}"

    st.markdown(
        f"""
        <style>
        /* تغيير التعتيم ليكون مائلاً للبياض بدلاً من السواد */
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)), url("{bg_image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* تصميم مستطيل اسم المطعم الفاخر */
        .restaurant-header {{
            background: linear-gradient(135deg, #1e1e1e 0%, #333333 100%);
            padding: 30px;
            border-radius: 20px;
            border: 4px double #FFD700; /* حدود ذهبية مزدوجة للفخامة */
            text-align: center;
            margin: 20px auto 40px auto;
            max-width: 90%;
            box-shadow: 0px 15px 35px rgba(0,0,0,0.4);
        }}

        .restaurant-header h1 {{
            font-size: 55px !important;
            color: #FFD700 !important; /* لون ذهبي */
            text-shadow: 2px 2px 4px #000;
            margin: 0;
            font-family: 'Cairo', sans-serif;
            font-weight: 900;
        }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: rgba(255, 255, 255, 0.8) !important;
            border: 10px solid #FFFFFF !important;
            border-radius: 20px !important;
            padding: 25px !important;
            margin-bottom: 40px !important;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.1) !important;
        }}

        .product-title-box {{
            background: #1E1E1E;
            color: #FFD700 !important; 
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 26px !important;
            font-weight: 900 !important;
            margin-bottom: 15px;
            border: 2px solid #FFD700;
            text-align: center;
        }}

        .price-tag-box {{
            background-color: #D32F2F;
            color: white !important;
            padding: 8px 15px;
            border-radius: 10px;
            font-size: 24px !important;
            font-weight: 900;
            border: 2px solid #FFFFFF;
            text-align: center;
            margin-bottom: 15px;
        }}

        .stCheckbox label p {{
            font-size: 24px !important;
            font-weight: 900 !important;
            color: #1E1E1E !important;
        }}
        
        h3, .stSubheader {{
            color: #1E1E1E !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

apply_custom_style()

# تحميل اسم المطعم
restaurant_name = get_restaurant_name()

def load_products():
    return pd.read_csv("products.csv") if os.path.exists("products.csv") else pd.DataFrame()

products_df = load_products()
selected_items = []
total_sum = 0

# عرض اسم المطعم داخل المستطيل الفاخر
st.markdown(f'''
    <div class="restaurant-header">
        <h1>{restaurant_name}</h1>
    </div>
''', unsafe_allow_html=True)

st.write("---")

if not products_df.empty:
    for index, row in products_df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([1, 1.2])
            with col1:
                if os.path.exists(str(row['الصورة'])):
                    st.image(row['الصورة'], use_container_width=True)
                else:
                    st.write("🖼️")
            with col2:
                st.markdown(f'<div class="product-title-box">{row["الاسم"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="price-tag-box">{row["السعر"]} د.ع</div>', unsafe_allow_html=True)
                
                if st.checkbox("إضافة للطلب ✅", key=f"c_{index}"):
                    selected_items.append(row['الاسم'])
                    total_sum += row['السعر']

    st.write("---")
    st.subheader("🛒 إتمام الطلب")
    customer_name = st.text_input("اسمك الكريم")
    table_num = st.number_input("رقم الطاولة", min_value=1)
    
    if st.button("إرسال الطلب وتأكيده 🚀", use_container_width=True):
        if selected_items and customer_name:
            items_str = "\n".join([f"- {i}" for i in selected_items])
            new_order = {
                "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "الزبون": customer_name,
                "الطاولة": table_num,
                "الطلبات": items_str
            }
            pd.DataFrame([new_order]).to_csv("orders.csv", mode='a', header=not os.path.exists("orders.csv"), index=False)
            st.success(f"تم تسجيل طلبك يا {customer_name}! شكراً لك.")
            st.balloons()
            
            if os.path.exists("numbers.txt"):
                with open("numbers.txt", "r") as f:
                    numbers = [line.strip() for line in f.readlines()]
                if numbers and numbers[0] != "":
                    message = f"*🧾 فاتورة طلب جديدة من {restaurant_name}*\n*👤 الزبون:* {customer_name}\n*📍 طاولة:* {table_num}\n*💰 المجموع:* {total_sum} د.ع\n*📦 الطلبات:*\n{items_str}"
                    url = f"https://wa.me/{numbers[0]}?text={urllib.parse.quote(message)}"
                    st.markdown(f'<a href="{url}" target="_blank" style="display: block; padding: 20px; font-size: 24px; font-weight: bold; text-align: center; color: #fff; background-color: #25D366; border: 4px solid #fff; border-radius: 15px; text-decoration: none;">إرسال الفاتورة عبر واتساب الآن ✅</a>', unsafe_allow_html=True)
        else:
            st.error("لطفاً، اختر وجبة واحدة على الأقل واكتب اسمك.")
else:
    st.info("المنيو فارغ حالياً.")

st.markdown("<br><p style='text-align: center; color: #1E1E1E; font-weight: bold; font-size: 28px;'>تشرفنا بزيارتكم ❤️</p>", unsafe_allow_html=True)
