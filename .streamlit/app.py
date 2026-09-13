import streamlit as st
from google import genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="SmartChef AI | Zero Waste Engine",
    page_icon="🥗",
    layout="wide"
)

# Custom CSS Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .header-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header-box h1 { color: white !important; font-weight: 800; margin-bottom: 5px; }
    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        border-left: 5px solid #11998e;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# Secure API Key Logic
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.error("🔑 API Key missing! Please configure Streamlit Secrets.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# Header Banner
st.markdown("""
    <div class="header-box">
        <h1>🥗 SmartChef AI</h1>
        <p>Interactive Leftover Recipe Engine | Supporting SDG 3 & SDG 12</p>
    </div>
""", unsafe_allow_html=True)

# Impact Metrics
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""<div class="metric-card"><h3>SDG 3 & 12</h3><p>Community Goals</p></div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""<div class="metric-card"><h3>~400g Saved</h3><p>Avg Food Saved / Meal</p></div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""<div class="metric-card"><h3>~1.2 kg CO₂</h3><p>Prevented Footprint</p></div>""", unsafe_allow_html=True)

st.write("")

col1, col2 = st.columns([1.2, 0.8], gap="large")

with col1:
    st.markdown("### 🧺 Step 1: Select or Upload Ingredients")
    
    input_method = st.radio("Input Method:", ["Interactive Pantry Selector", "Upload Fridge Photo"], horizontal=True)
    
    selected_ingredients = []
    ingredients_text = ""
    uploaded_image = None

    if input_method == "Interactive Pantry Selector":
        st.write("Click categories below to quickly add available leftovers:")
        
        with st.expander("🥦 Vegetables & Greens", expanded=True):
            v_cols = st.columns(3)
            if v_cols[0].checkbox("Spinach"): selected_ingredients.append("Spinach")
            if v_cols[0].checkbox("Tomatoes"): selected_ingredients.append("Tomatoes")
            if v_cols[1].checkbox("Onions"): selected_ingredients.append("Onions")
            if v_cols[1].checkbox("Bell Peppers"): selected_ingredients.append("Bell Peppers")
            if v_cols[2].checkbox("Carrots"): selected_ingredients.append("Carrots")
            if v_cols[2].checkbox("Broccoli"): selected_ingredients.append("Broccoli")

        with st.expander("🍚 Pantry & Grains"):
            g_cols = st.columns(3)
            if g_cols[0].checkbox("Cooked Rice"): selected_ingredients.append("Cooked Rice")
            if g_cols[0].checkbox("Pasta"): selected_ingredients.append("Pasta")
            if g_cols[1].checkbox("Bread"): selected_ingredients.append("Bread")
            if g_cols[1].checkbox("Oats"): selected_ingredients.append("Oats")
            if g_cols[2].checkbox("Canned Beans"): selected_ingredients.append("Canned Beans")
            if g_cols[2].checkbox("Lentils"): selected_ingredients.append("Lentils")

        with st.expander("🧀 Dairy, Proteins & Extras"):
            d_cols = st.columns(3)
            if d_cols[0].checkbox("Eggs"): selected_ingredients.append("Eggs")
            if d_cols[0].checkbox("Milk / Yogurt"): selected_ingredients.append("Milk / Yogurt")
            if d_cols[1].checkbox("Cheddar / Cheese"): selected_ingredients.append("Cheese")
            if d_cols[1].checkbox("Cooked Chicken"): selected_ingredients.append("Cooked Chicken")
            if d_cols[2].checkbox("Mushrooms"): selected_ingredients.append("Mushrooms")
            if d_cols[2].checkbox("Tofu"): selected_ingredients.append("Tofu")

        extra_text = st.text_input("Add any other custom items (comma separated):", placeholder="e.g., half a lemon, garlic paste")
        
        # Combine selected checkboxes and custom text
        all_items = selected_ingredients + ([extra_text] if extra_text else [])
        ingredients_text = ", ".join(all_items)
        
        if ingredients_text:
            st.success(f"Selected Items: **{ingredients_text}**")

    else:
        uploaded_file = st.file_uploader("Upload a clear photo of your fridge shelf:", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Uploaded View", use_container_width=True)

    st.markdown("### ⏳ Pantry Expiry Radar")
    expiring_items = st.text_input("Which items are expiring TODAY or TOMORROW?", placeholder="e.g., open yogurt, fresh spinach")

with col2:
    st.markdown("### 🎯 Step 2: Health Target")
    
    health_profile = st.selectbox(
        "Select Dietary Mode:",
        [
            "Standard Healthy Household Mode",
            "🩸 Diabetic & Blood-Sugar Friendly (Low GI / High Fiber)",
            "💪 High-Protein & Fitness Focused",
            "🥗 100% Vegetarian / Plant-Based",
            "🥜 Allergen-Safe (Nut-Free / Gluten-Free)"
        ]
    )
    
    family_size = st.slider("Portion Size (Servings):", min_value=1, max_value=6, value=2)
    st.info("💡 **Supercook-Style Feature:** Toggle checkboxes on the left to quickly build your dish without typing!")

st.divider()

# Generation Logic
if st.button("✨ Cook Smart with AI", type="primary"):
    if input_method == "Interactive Pantry Selector" and not ingredients_text:
        st.warning("Please select or type at least one ingredient!")
        st.stop()
        
    with st.spinner("SmartChef AI is crafting your recipe..."):
        system_instruction = f"""
        You are an elite nutritionist and zero-waste chef expert.
        Generate a delicious, healthy, low-waste recipe based on leftover ingredients.
        
        User Rules:
        - Health Profile: {health_profile}
        - Servings Required: {family_size}
        - Expiring Priority Ingredients: {expiring_items}
        
        If Diabetic/Blood-Sugar Friendly mode is selected:
        1. Prioritize low glycemic index (GI) foods.
        2. Combine high-fiber or protein options to prevent glucose spikes.
        3. Cap simple carbohydrates and explain sugar/carb safety.
        
        Structured Output Format Required:
        ---
        ## 🍲 Recipe Title
        **Preparation Time:** [X] Mins | **Difficulty:** [Easy/Medium]
        
        ### 🛒 Ingredients Required (Using Leftovers First)
        - [List items]
        
        ### 🍳 Step-by-Step Instructions
        1. [Step 1]
        2. [Step 2]
        
        ### 🩸 Blood Sugar & Health Breakdown
        - **Carb & Glycemic Impact:** [Explain glycemic safety]
        - **Nutritional Grade:** [e.g., A+]
        - **Key Macro Breakdown:** [Calories, Protein, Carbs, Fiber per serving]
        
        ### 🌿 Zero-Waste Impact Metrics
        - **Food Waste Prevented:** ~[X] grams
        - **Estimated CO₂ Footprint Saved:** ~[X] kg
        ---
        """
        
        try:
            if input_method == "Upload Fridge Photo" and uploaded_image:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=[uploaded_image, system_instruction + "\nFirst, identify the leftover ingredients in the photo, then build the recipe."]
                )
            else:
                prompt = f"{system_instruction}\nLeftover Ingredients Provided: {ingredients_text}"
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
            
            st.success("Recipe Created Successfully!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error connecting to AI backend: {str(e)}")
