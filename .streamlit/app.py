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
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header-box h1 { color: white !important; font-weight: 800; margin-bottom: 5px; }
    .metric-card {
        background: white;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        border-left: 5px solid #11998e;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .metric-card h3 {
        margin: 0;
        color: #2c3e50;
        font-size: 1.4rem;
    }
    .metric-card p {
        margin: 0;
        color: #7f8c8d;
        font-size: 0.85rem;
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

# Secure API Key Retrieval from Secrets or Sidebar
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.error("🔑 API Key missing! Please configure Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Header Banner
st.markdown("""
    <div class="header-box">
        <h1>🥗 SmartChef AI</h1>
        <p>Interactive Leftover Recipe & Health Engine | Supporting SDG 3 & SDG 12</p>
    </div>
""", unsafe_allow_html=True)

# Impact Benchmark Metrics (Clarified Top Labels)
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""<div class="metric-card"><h3>SDG 3 & 12</h3><p>Aligned Global Goals</p></div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""<div class="metric-card"><h3>~400g / Meal</h3><p>Avg Benchmark Waste Saved</p></div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""<div class="metric-card"><h3>~1.2 kg CO₂</h3><p>Avg Benchmark Reduction</p></div>""", unsafe_allow_html=True)

st.write("")

col1, col2 = st.columns([1.3, 0.7], gap="large")

with col1:
    st.markdown("### 🧺 Step 1: Supercook-Style Pantry Builder")
    
    input_method = st.radio("Choose Input Method:", ["Interactive Pantry Drawers", "Upload Fridge Photo"], horizontal=True)
    
    selected_ingredients = []
    ingredients_text = ""
    uploaded_image = None

    if input_method == "Interactive Pantry Drawers":
        st.caption("Click drawers below to quickly build your dish like Supercook:")
        
        # Category Drawers
        with st.expander("🥦 Vegetables & Fresh Greens", expanded=True):
            c1, c2, c3 = st.columns(3)
            if c1.checkbox("Spinach"): selected_ingredients.append("Spinach")
            if c1.checkbox("Tomatoes"): selected_ingredients.append("Tomatoes")
            if c1.checkbox("Onions"): selected_ingredients.append("Onions")
            if c2.checkbox("Bell Peppers"): selected_ingredients.append("Bell Peppers")
            if c2.checkbox("Carrots"): selected_ingredients.append("Carrots")
            if c2.checkbox("Broccoli"): selected_ingredients.append("Broccoli")
            if c3.checkbox("Garlic"): selected_ingredients.append("Garlic")
            if c3.checkbox("Cucumber"): selected_ingredients.append("Cucumber")
            if c3.checkbox("Zucchini"): selected_ingredients.append("Zucchini")

        with st.expander("🍚 Grains, Pasta & Bakery"):
            c1, c2, c3 = st.columns(3)
            if c1.checkbox("Cooked Rice"): selected_ingredients.append("Cooked Rice")
            if c1.checkbox("Pasta / Noodles"): selected_ingredients.append("Pasta")
            if c2.checkbox("Bread"): selected_ingredients.append("Bread")
            if c2.checkbox("Oats"): selected_ingredients.append("Oats")
            if c3.checkbox("Quinoa"): selected_ingredients.append("Quinoa")
            if c3.checkbox("Flour"): selected_ingredients.append("Flour")

        with st.expander("🍗 Meat, Poultry & Seafood"):
            c1, c2, c3 = st.columns(3)
            if c1.checkbox("Cooked Chicken"): selected_ingredients.append("Cooked Chicken")
            if c1.checkbox("Ground Beef"): selected_ingredients.append("Ground Beef")
            if c2.checkbox("Canned Tuna"): selected_ingredients.append("Canned Tuna")
            if c2.checkbox("Salmon"): selected_ingredients.append("Salmon")
            if c3.checkbox("Eggs"): selected_ingredients.append("Eggs")
            if c3.checkbox("Shrimp"): selected_ingredients.append("Shrimp")

        with st.expander("🧀 Dairy, Cheese & Plant Alternatives"):
            c1, c2, c3 = st.columns(3)
            if c1.checkbox("Milk"): selected_ingredients.append("Milk")
            if c1.checkbox("Greek Yogurt"): selected_ingredients.append("Greek Yogurt")
            if c2.checkbox("Cheddar / Cheese"): selected_ingredients.append("Cheese")
            if c2.checkbox("Butter"): selected_ingredients.append("Butter")
            if c3.checkbox("Tofu"): selected_ingredients.append("Tofu")
            if c3.checkbox("Heavy Cream"): selected_ingredients.append("Heavy Cream")

        with st.expander("🥫 Canned Goods, Legumes & Spices"):
            c1, c2, c3 = st.columns(3)
            if c1.checkbox("Canned Chickpeas"): selected_ingredients.append("Chickpeas")
            if c1.checkbox("Lentils"): selected_ingredients.append("Lentils")
            if c2.checkbox("Olive Oil"): selected_ingredients.append("Olive Oil")
            if c2.checkbox("Soy Sauce"): selected_ingredients.append("Soy Sauce")
            if c3.checkbox("Mushrooms"): selected_ingredients.append("Mushrooms")
            if c3.checkbox("Tomato Paste"): selected_ingredients.append("Tomato Paste")

        extra_text = st.text_input("➕ Type any missing custom leftovers:", placeholder="e.g., half a lemon, leftover curry")
        
        all_items = selected_ingredients + ([extra_text] if extra_text else [])
        ingredients_text = ", ".join(all_items)
        
        if ingredients_text:
            st.success(f"Selected Pantry Items ({len(all_items)}): **{ingredients_text}**")

    else:
        uploaded_file = st.file_uploader("Upload a clear photo of your fridge shelf:", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Uploaded Fridge View", use_container_width=True)

    st.markdown("### ⏳ Pantry Expiry Radar")
    expiring_items = st.text_input("Items expiring TODAY or TOMORROW:", placeholder="e.g., spinach, open yogurt")

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
    
    st.markdown("### 💡 Smart Chef AI Add-ons")
    allow_missing = st.checkbox("Suggest 1 missing ingredient if needed (Supercook Style)", value=True)

st.divider()

# Recipe Generation Logic
if st.button("✨ Cook Smart with AI", type="primary"):
    if input_method == "Interactive Pantry Drawers" and not ingredients_text:
        st.warning("Please select or type at least one ingredient!")
        st.stop()
        
    with st.spinner("SmartChef AI is crafting your customized recipe..."):
        system_instruction = f"""
        You are an elite nutritionist and zero-waste chef expert.
        Generate a delicious, healthy, low-waste recipe based on leftover ingredients.
        
        User Rules:
        - Health Profile: {health_profile}
        - Servings Required: {family_size}
        - Expiring Priority Ingredients: {expiring_items}
        - Allow Suggesting 1 Missing Core Ingredient: {allow_missing}
        
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
        {'### 💡 Recommended 1 Missing Ingredient to Buy' if allow_missing else ''}
        {'- [Optional 1 missing item]' if allow_missing else ''}
        
        ### 🍳 Step-by-Step Instructions
        1. [Step 1]
        2. [Step 2]
        
        ### 🩸 Blood Sugar & Health Breakdown
        - **Carb & Glycemic Impact:** [Explain glycemic safety]
        - **Nutritional Grade:** [e.g., A+]
        - **Key Macro Breakdown:** [Calories, Protein, Carbs, Fiber per serving]
        
        ### 🌿 Zero-Waste Impact Metrics
        - **Food Waste Prevented:** [Calculate estimated weight in grams based on ingredients provided]
        - **Estimated CO₂ Footprint Saved:** [Calculate estimated CO₂ saved in kg based on ingredients provided]
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
