import streamlit as st
from agent import CreativeAgent

# Page config
st.set_page_config(
    page_title="Creative Agent",
    page_icon="✦",
    layout="wide",
)

# Initialize OpenAI client in session state
if "agent" not in st.session_state:
    st.session_state.agent = CreativeAgent(api_key=st.secrets["OPENAI_API_KEY"])

# Session state for UI
if "ui_language" not in st.session_state:
    st.session_state.ui_language = "English"
if "campaign_result" not in st.session_state:
    st.session_state.campaign_result = None
if "strategic_brief" not in st.session_state:
    st.session_state.strategic_brief = None

# Translation dictionaries
TEXTS = {
    "English": {
        "title": "Creative Agent",
        "subtitle": "From brief to campaign narrative — in seconds.",
        "product_name": "Product Name",
        "product_name_placeholder": "e.g., Mint & Lemon, Coffee Blend, Energy Drink",
        "product_desc": "Product Description",
        "product_desc_placeholder": "What is it? What makes it special? Natural ingredients? No sugar?",
        "target_audience": "Target Audience",
        "target_audience_placeholder": "Who are you speaking to? Age, lifestyle, values, daily struggles...",
        "brand_voice": "Brand Voice",
        "brand_voice_options": ["Youthful", "Fun", "Natural", "Refreshing", "Bold", "Premium", "Warm", "Playful"],
        "output_language": "Output Language",
        "submit": "Generate Campaign",
        "campaign_narrative": "Campaign Narrative",
        "strategic_brief": "Strategic Brief",
        "analyzing": "Analyzing brief...",
        "writing": "Writing narrative...",
        "fill_warning": "Please fill in all required fields (Product Name, Description, and Target Audience)",
        "footer": "AI-Powered Marketing Studio",
        "example_product": "Example: Mint & Lemon",
        "example_desc": "Example: Natural mint and lemon drink, no sugar, refreshing",
        "example_audience": "Example: University students & young professionals, 18-30, health-conscious",
        "output_lang_hint": "Output will be in English"
    },
    "Arabic": {
        "title": "وكيل الإبداع",
        "subtitle": "من الموجز إلى سرد الحملة — في ثوانٍ",
        "product_name": "اسم المنتج",
        "product_name_placeholder": "مثال: نعناع وليمون، قهوة مختصة، مشروب طاقة",
        "product_desc": "وصف المنتج",
        "product_desc_placeholder": "وش هو؟ وش اللي يخليه مميز؟ طبيعي؟ بدون سكر؟",
        "target_audience": "الجمهور المستهدف",
        "target_audience_placeholder": "لمن تتكلم؟ العمر، نمط الحياة، القيم، التحديات اليومية...",
        "brand_voice": "صوت العلامة التجارية",
        "brand_voice_options": ["شبابي", "مرح", "طبيعي", "منعش", "جريء", "فاخر", "دافئ", "مرح"],
        "output_language": "لغة الإخراج",
        "submit": "إنشاء الحملة",
        "campaign_narrative": "السرد التسويقي",
        "strategic_brief": "الموجز الاستراتيجي",
        "analyzing": "جاري تحليل الموجز...",
        "writing": "جاري كتابة السرد...",
        "fill_warning": "يرجى ملء جميع الحقول المطلوبة (اسم المنتج والوصف والجمهور المستهدف)",
        "footer": "استوديو تسويق بالذكاء الاصطناعي",
        "example_product": "مثال: نعناع وليمون",
        "example_desc": "مثال: مشروب طبيعي نعناع وليمون، بدون سكر، منعش",
        "example_audience": "مثال: طلاب الجامعة والموظفين الجدد، ١٨-٣٠، مهتمين بالصحة",
        "output_lang_hint": "المخرجات ستكون بالعربية"
    }
}

# Voice mapping for Arabic to English
VOICE_MAP = {
    "شبابي": "Youthful", "مرح": "Fun", "طبيعي": "Natural",
    "منعش": "Refreshing", "جريء": "Bold", "فاخر": "Premium",
    "دافئ": "Warm",
}

def t(key):
    """Get translated text"""
    return TEXTS[st.session_state.ui_language][key]

def map_voice_to_english(voice_list):
    """Convert voice selections to English for API"""
    return [VOICE_MAP.get(v, v) for v in voice_list]

# Language toggle function - syncs both UI and output language
def toggle_language():
    """Toggle between English and Arabic for both UI and output"""
    if st.session_state.ui_language == "English":
        st.session_state.ui_language = "Arabic"
    else:
        st.session_state.ui_language = "English"
    st.rerun()

# Reduce default spacing in Streamlit
st.markdown("""
<style>
    /* Reduce spacing between elements */
    .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect {
        margin-bottom: -0.5rem;
    }
    .stForm {
        gap: 0.5rem;
    }
    div[data-testid="stForm"] {
        gap: 0.5rem;
    }
    /* Reduce title spacing */
    h1 {
        margin-bottom: 0rem;
    }
    /* Reduce column gap */
    .row-widget.stHorizontal {
        gap: 1rem;
    }
    /* Make toggle button compact */
    .stButton button {
        padding: 0.25rem 0.5rem;
        font-size: 0.9rem;
    }
    /* Hint text styling */
    .output-hint {
        font-size: 0.8rem;
        color: #666;
        margin-top: -0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with title and language toggle
header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.title(t("title"))
    st.caption(t("subtitle"))

with header_col2:
    # Language toggle button with emoji
    button_text = "🌐 العربية" if st.session_state.ui_language == "English" else "🌐 English"
    if st.button(button_text, use_container_width=True, key="lang_toggle"):
        toggle_language()

st.markdown("---")

# Create two columns with reduced gap
col1, col2 = st.columns([1, 1], gap="small")

# Left column - Input form
with col1:
    with st.form(key="campaign_form"):
        # Show output language hint (read-only)
        st.info(f"ℹ️ {t('output_lang_hint')}")
        
        # Input fields with reduced spacing
        product_name = st.text_input(
            t("product_name"),
            placeholder=t("product_name_placeholder"),
            key="product_name"
        )
        
        product_desc = st.text_area(
            t("product_desc"),
            placeholder=t("product_desc_placeholder"),
            height=80,
            key="product_desc"
        )
        
        target_audience = st.text_area(
            t("target_audience"),
            placeholder=t("target_audience_placeholder"),
            height=80,
            key="target_audience"
        )
        
        brand_voice = st.multiselect(
            t("brand_voice"),
            options=t("brand_voice_options"),
            default=[t("brand_voice_options")[0]],
            key="brand_voice"
        )
        
        submit_button = st.form_submit_button(
            t("submit"),
            type="primary",
            use_container_width=True
        )

# Right column - Output
with col2:
    if submit_button and product_name and product_desc and target_audience:
        # Prepare voice for API
        voice_english = map_voice_to_english(brand_voice)
        brand_voice_str = ", ".join(voice_english) if voice_english else "Authentic"
        
        # Output language is automatically the same as UI language
        output_lang = st.session_state.ui_language
        
        # Generate campaign using the agent
        with st.status(t("analyzing"), expanded=True) as status:
            result = st.session_state.agent.generate_campaign(
                product_name=product_name,
                product_desc=product_desc,
                target_audience=target_audience,
                brand_voice=brand_voice_str,
                output_language=output_lang
            )
            
            st.session_state.strategic_brief = result["strategic_brief"]
            st.session_state.campaign_result = result["campaign_narrative"]
            
            status.update(label="Campaign generated successfully!", state="complete")
        
        st.divider()
        
        # Campaign Narrative
        st.subheader(t("campaign_narrative"))
        narrative = st.session_state.campaign_result
        if narrative:
            # Display with proper formatting
            paragraphs = narrative.split('\n\n')
            
            for para in paragraphs:
                if para.strip():
                    if output_lang == "Arabic":
                        st.markdown(f'<p dir="rtl">{para.strip()}</p>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<p>{para.strip()}</p>', unsafe_allow_html=True)
                    st.write("")  # Add small spacing between paragraphs
        
        # Strategic Brief (collapsible)
        with st.expander(f"📊 {t('strategic_brief')}"):
            st.json(st.session_state.strategic_brief)
            
    elif submit_button:
        st.warning(t("fill_warning"))

# Footer
st.divider()
st.caption(t("footer"))