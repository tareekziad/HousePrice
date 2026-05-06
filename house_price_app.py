import pandas as pd
import numpy as np
import streamlit as st
import joblib

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Riyadh Property Valuator",
    page_icon="🏠",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: #fff;
    letter-spacing: -0.5px;
    margin-bottom: 0.25rem;
}
.hero p {
    color: rgba(255,255,255,0.55);
    font-size: 1rem;
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Glass card ── */
.glass-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.5rem;
}

/* ── Section label ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4);
    margin-bottom: 1rem;
}

/* ── Sliders ── */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #a78bfa, #818cf8) !important;
}
.stSlider label {
    color: rgba(255,255,255,0.8) !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
}
.stSlider p { color: rgba(255,255,255,0.8) !important; }

/* ── Selectboxes ── */
.stSelectbox label {
    color: rgba(255,255,255,0.8) !important;
    font-size: 0.85rem !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #fff !important;
}

/* ── Predict button ── */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #a78bfa, #818cf8);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 1rem 2rem;
    font-size: 1rem;
    font-weight: 500;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: opacity 0.2s;
    margin-top: 0.5rem;
}
div.stButton > button:hover {
    opacity: 0.88;
    border: none;
}

/* ── Result card ── */
.result-card {
    background: linear-gradient(135deg, rgba(167,139,250,0.18), rgba(129,140,248,0.18));
    border: 1px solid rgba(167,139,250,0.4);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin-top: 1.5rem;
}
.result-label {
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin-bottom: 0.5rem;
}
.result-value {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: #fff;
    margin: 0;
}
.result-currency {
    font-size: 1.1rem;
    color: rgba(255,255,255,0.6);
    margin-top: 0.25rem;
}

/* ── Summary row ── */
.summary-chip {
    display: inline-block;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 50px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.7);
    margin: 0.25rem;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🏠 Property Valuator</h1>
    <p>Riyadh Real Estate · AI Price Estimation</p>
</div>
""", unsafe_allow_html=True)


# ── Input form ────────────────────────────────────────────────────────────────
def get_input():
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">🛏  Property Details</div>', unsafe_allow_html=True)
        beds         = st.slider('Bedrooms',       min_value=1, max_value=7,        step=1,   value=4)
        livings      = st.slider('Living Rooms',   min_value=1, max_value=5,        step=1,   value=2)
        wc           = st.slider('Bathrooms',      min_value=1, max_value=5,        step=1,   value=3)
        age          = st.slider('Property Age (years)', min_value=0, max_value=36, step=1,   value=15)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">📐  Dimensions & Location</div>', unsafe_allow_html=True)
        area         = st.slider('Area (m²)',       min_value=1,   max_value=86000000, step=100,  value=50000)
        street_width = st.slider('Street Width (m)', min_value=1, max_value=2015,     step=100,  value=200)
        rent_period  = st.selectbox('Listing Type', ['sell', 'Yearly', 'Daily', 'Monthly'])
        property_category = st.selectbox('Property Category', ['Land', 'other', 'Apartment', 'Villa', 'Floor'])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">📍  District</div>', unsafe_allow_html=True)
    district = st.selectbox('Select District', [
        'حي الدار البيضاء','اخري','حي النرجس','حي العريجاء الغربية','حي العزيزية',
        'حي النظيم','حي الرمال','حي اشبيلية','حي الربوة','حي ظهرة لبن',
        'حي السليمانية','حي ضاحية نمار','حي ظهرة نمار','حي طويق','حي الشرق',
        'حي الملز','حي الخليج','حي الحزم','حي المونسية','حي المعيزلة',
        'حي الجنادرية','حي القيروان','حي الياسمين','حي العارض','حي النسيم الغربي',
        'حي الملك فيصل','حي عريض','حي عرقة','حي النزهة','حي العقيق','حي حطين',
        'حي المهدية','حي بدر','حي بنبان','حي النهضة','حي الحمراء','حي النفل',
        'حي السويدي','حي قرطبة','حي اليرموك حي الروضة','حي العليا','حي الملقا',
        'حي القادسية','حي الصحافة','حي الاندلس','حي النسيم الشرقي','حي النخيل',
        'حي طيبة','حي عكاظ','حي الندى','حي الفلاح','حي الملك فهد','حي السعادة',
        'حي المحمدية','حي الوادي','حي التعاون','حي المصيف','حي المروج',
        'حي الروابي','حي الشفا','حي غرناطة','حي القدس','حي الربيع','حي ديراب',
        'حي الزهرة','حي الشهداء','حي الازدهار','حي الورود',
        'حي مطار الملك خالد الدولي'
    ])
    st.markdown('</div>', unsafe_allow_html=True)

    return pd.DataFrame(
        data=[[beds, livings, wc, area, street_width, age, rent_period, district, property_category]],
        columns=['beds','livings','wc','area','street_width','age','rent_period','district','property_category']
    ), beds, livings, wc, area, street_width, age, rent_period, district, property_category


inputs, beds, livings, wc, area, street_width, age, rent_period, district, property_category = get_input()


# ── Summary chips ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; margin: 0.5rem 0 1.5rem;">
    <span class="summary-chip">🛏 {beds} beds</span>
    <span class="summary-chip">🛋 {livings} living</span>
    <span class="summary-chip">🚿 {wc} wc</span>
    <span class="summary-chip">📐 {area:,} m²</span>
    <span class="summary-chip">🏷 {rent_period}</span>
    <span class="summary-chip">🏗 {property_category}</span>
</div>
""", unsafe_allow_html=True)


# ── Predict ───────────────────────────────────────────────────────────────────
model = joblib.load('model.pkl')

if st.button('✨  Estimate Property Value'):
    with st.spinner('Calculating...'):
        log_prediction  = model.predict(inputs)
        real_prediction = np.exp(log_prediction)
        price           = real_prediction[0]

    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">Estimated Market Value</div>
        <div class="result-value">{price:,.0f}</div>
        <div class="result-currency">Saudi Riyal · SAR</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Range hint ────────────────────────────────────────────────────────────
    low  = price * 0.90
    high = price * 1.10
    st.markdown(f"""
    <p style="text-align:center; color:rgba(255,255,255,0.4); font-size:0.8rem; margin-top:0.75rem;">
        Estimated range &nbsp;·&nbsp; {low:,.0f} – {high:,.0f} SAR
    </p>
    """, unsafe_allow_html=True)
