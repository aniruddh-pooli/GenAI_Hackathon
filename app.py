import streamlit as st
import google.generativeai as genai
import json
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Career Compass",
    page_icon="🧭",
    layout="wide",
)

# --- Enhanced UI Styling (Glassmorphism & Modern Theme) ---
st.markdown("""
<style>
    /* Global App Styling */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #e0e6ed;
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    
    /* Fade-in animation for results */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .results-container {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* --- HEADER --- */
    .main-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .main-title {
        font-size: 3.8rem;
        font-weight: 700;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #79c2ff 0%, #42a5f5 50%, #1e88e5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 0 5px 25px rgba(100, 181, 246, 0.2);
    }
    .subtitle {
        font-size: 1.25rem;
        color: #90a4ae;
        font-weight: 300;
    }

    /* --- INPUT SECTION --- */
    .input-container {
        background: rgba(30, 39, 73, 0.7);
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid rgba(100, 181, 246, 0.2);
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .stTextArea > div > div > textarea,
    .stTextInput > div > div > input {
        background-color: rgba(15, 15, 35, 0.8);
        border: 1px solid rgba(100, 181, 246, 0.3);
        border-radius: 12px;
        color: #e0e6ed;
        font-size: 1rem;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    .stTextArea > div > div > textarea:focus,
    .stTextInput > div > div > input:focus {
        border-color: #64b5f6;
        box-shadow: 0 0 20px rgba(100, 181, 246, 0.4);
        transform: translateY(-2px);
    }

    /* --- BUTTONS --- */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.8rem 2rem;
        transition: all 0.3s ease;
        font-size: 1.05rem;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1e88e5 0%, #1976d2 100%);
        border: none;
        color: white;
        box-shadow: 0 4px 15px rgba(30, 136, 229, 0.4);
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(30, 136, 229, 0.6);
        background: linear-gradient(135deg, #2196f3 0%, #1e88e5 100%);
    }
    .stButton > button[kind="secondary"] {
        background: transparent;
        border: 1px solid rgba(144, 164, 174, 0.5);
        color: #90a4ae;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(144, 164, 174, 0.1);
        color: #b0bec5;
        border-color: #90a4ae;
    }
    
    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 2px solid rgba(100, 181, 246, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        background: none;
        padding: 1rem 0.5rem;
        color: #90a4ae;
        font-weight: 600;
        border-radius: 0;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #64b5f6;
        border-bottom: 2px solid #64b5f6;
    }
    
    /* --- ANALYSIS & ROADMAP STYLING --- */
    /* Metric Cards */
    .stMetric {
        background: rgba(30, 39, 73, 0.6);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(100, 181, 246, 0.2);
        backdrop-filter: blur(10px);
    }
    .stMetric [data-testid="metric-value"] {
        color: #79c2ff;
        font-size: 2rem;
    }
    /* Skill Breakdown Cards */
    .skill-card {
        background: rgba(30, 39, 73, 0.6);
        border: 1px solid rgba(100, 181, 246, 0.2);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .skill-card:hover {
        transform: scale(1.02);
        border-color: rgba(100, 181, 246, 0.5);
    }
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .status-matched {
        background-color: rgba(76, 175, 80, 0.2);
        color: #81c784;
    }
    .status-gap {
        background-color: rgba(244, 67, 54, 0.2);
        color: #e57373;
    }
    /* Roadmap Step Cards */
    .roadmap-step-card {
        background: rgba(30, 39, 73, 0.8) !important;
        border: 1px solid rgba(100, 181, 246, 0.3) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        color: #e0e6ed !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
        min-height: 200px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        text-align: left !important;
        cursor: pointer !important;
    }
    .roadmap-step-card:hover {
        transform: translateY(-8px) !important;
        border-color: #64b5f6 !important;
        box-shadow: 0 10px 40px rgba(100, 181, 246, 0.25) !important;
    }
    
    /* --- DIALOG / MODAL --- */
    .stDialog {
        background: rgba(15, 15, 35, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(100, 181, 246, 0.3);
        border-radius: 16px;
    }
    .stDialog .stButton > button {
        background-color: rgba(144, 164, 174, 0.2);
    }
    .resource-link-button {
        display: inline-block;
        padding: 0.6rem 1.2rem;
        background: linear-gradient(135deg, #1e88e5 0%, #1976d2 100%);
        color: white !important;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .resource-link-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(30, 136, 229, 0.4);
    }

    /* --- MISC --- */
    .stSuccess {
        background: rgba(76, 175, 80, 0.15);
        border: 1px solid rgba(76, 175, 80, 0.4);
        border-radius: 12px;
        border-left: 5px solid #4caf50;
    }
    .stInfo {
        background-color: rgba(30, 136, 229, 0.1);
        border: 1px solid rgba(30, 136, 229, 0.3);
        border-left: 5px solid #1e88e5;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- Gemini API Configuration ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("🔴 **Gemini API key not found.** Please add it to your Streamlit secrets.")
    st.info("Create a file at `.streamlit/secrets.toml` and add the line: `GEMINI_API_KEY = 'YOUR_API_KEY'`")
    st.stop()

MODEL_NAME = "gemini-1.5-flash-latest" 
MODEL = genai.GenerativeModel(MODEL_NAME)

# --- LLM Functions (No changes needed here) ---
def synthesize_profile(profile_text):
    prompt = f"""
    You are an expert career advisor bot. Analyze a student's profile and extract their technical skills and key projects.
    Format the output as a clean JSON object with two keys: "skills" and "projects".
    - "skills": A list of technical skills (e.g., ["Python", "TensorFlow", "Data Analysis"]).
    - "projects": A list of brief project descriptions (e.g., ["Built a movie recommender system"]).
    Profile: "{profile_text}"
    """
    try:
        response = MODEL.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Error in profile synthesis: {e}")
        return {"skills": [], "projects": []}

def get_required_skills(target_career):
    prompt = f"""
    You are a data-driven career analyst for the Indian job market.
    List the 5 most critical technical skills for a "{target_career}" role.
    Return a JSON list of strings.
    Example for "Product Manager": ["Market Research", "Product Strategy", "UX Design", "Agile Methodologies", "Data Analysis"]
    Skills for "{target_career}":
    """
    try:
        response = MODEL.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Error fetching required skills: {e}")
        return []

def get_actionable_roadmap(target_career, missing_skills):
    skills_str = ", ".join(missing_skills)
    prompt = f"""
    You are an expert career coach for the tech industry in India.
    Create a 3-step learning roadmap for a student aiming for a "{target_career}" role, missing these skills: {skills_str}.
    Each step must have a "step_title", "description", a concrete "project" idea, and a specific, high-quality "resource" URL (e.g., NPTEL, Coursera, freeCodeCamp).
    Return a JSON object with a single key "roadmap" whose value is a list of these three steps.
    """
    try:
        response = MODEL.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Error generating roadmap: {e}")
        return {"roadmap": []}

# --- Initialize Session State ---
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'required_skills_raw' not in st.session_state:
    st.session_state.required_skills_raw = []
if 'matching_skills' not in st.session_state:
    st.session_state.matching_skills = []
if 'missing_skills_raw' not in st.session_state:
    st.session_state.missing_skills_raw = []
if 'target_career' not in st.session_state:
    st.session_state.target_career = ""
if 'roadmap_steps' not in st.session_state:
    st.session_state.roadmap_steps = []
if 'selected_step' not in st.session_state:
    st.session_state.selected_step = None

# ---- UI Components ----
# HEADER SECTION
st.markdown("""
<div class="main-header">
    <h1 class="main-title">AI Career Compass 🧭</h1>
    <p class="subtitle">Chart Your Path to a Top Tech Career</p>
</div>
""", unsafe_allow_html=True)

# CENTERED INPUT SECTION
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    with st.container():
        profile_text = st.text_area(
            "**Paste Your Resume or Describe Your Profile**",
            height=200,
            placeholder="Example: I am a final year Computer Science student passionate about machine learning. I know Python, Scikit-learn, and Pandas. I built a movie recommendation engine and I'm familiar with Git..."
        )
        target_career = st.text_input(
            "**Enter Your Target Career**",
            placeholder="e.g., AI Engineer, Data Scientist, SDE"
        )
        st.write("") # Spacer
        
        # Action Buttons
        analyze_btn = st.button("🚀 Analyze & Generate Roadmap", type="primary", use_container_width=True)
        if st.session_state.analysis_done:
            if st.button("🔄 Start New Analysis", type="secondary", use_container_width=True):
                st.session_state.clear()
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# --- ANALYSIS LOGIC ---
if analyze_btn:
    if not profile_text or not target_career:
        st.warning("Please fill in both your profile and target career.")
    else:
        st.session_state.analysis_done = False # Reset for new analysis
        
        with st.spinner('🔭 Scanning the job market and your profile...'):
            user_profile = synthesize_profile(profile_text)
            required_skills_raw = get_required_skills(target_career)
        
        user_skills_raw = user_profile.get("skills", [])
        user_skills = [skill.lower().strip() for skill in user_skills_raw]
        required_skills = [skill.lower().strip() for skill in required_skills_raw]

        matching_skills = [skill for skill in required_skills if skill in user_skills]
        missing_skills = [skill for skill in required_skills if skill not in user_skills]
        
        st.session_state.user_profile = user_profile
        st.session_state.required_skills_raw = required_skills_raw
        st.session_state.matching_skills = matching_skills
        st.session_state.missing_skills_raw = [skill for skill in required_skills_raw if skill.lower().strip() in missing_skills]
        st.session_state.target_career = target_career
        st.session_state.selected_step = None
        
        if st.session_state.missing_skills_raw:
            with st.spinner('🗺️ Building your personalized roadmap...'):
                roadmap_data = get_actionable_roadmap(target_career, st.session_state.missing_skills_raw)
                st.session_state.roadmap_steps = roadmap_data.get("roadmap", [])
        
        st.session_state.analysis_done = True
        st.rerun()

# --- DISPLAY RESULTS ---
if st.session_state.analysis_done:
    st.markdown("---")
    
    with st.container():
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📊 Skill Gap Analysis", "🎯 Learning Roadmap"])
        
        with tab1:
            st.header("Your Personalized Skill-Gap Analysis")
            
            if st.session_state.required_skills_raw:
                match_count = len(st.session_state.matching_skills)
                total_count = len(st.session_state.required_skills_raw)
                match_percentage = int((match_count / total_count) * 100) if total_count > 0 else 0
                
                # Progress summary with metrics
                st.subheader("Your Scorecard")
                cols = st.columns(3)
                cols[0].metric("Skills Matched", f"{match_count}/{total_count}")
                cols[1].metric("Match Percentage", f"{match_percentage}%")
                cols[2].metric("Skills to Learn", len(st.session_state.missing_skills_raw))
                st.progress(match_percentage / 100, text=f"You're {match_percentage}% of the way there!")
            
            st.divider()

            # Skills Breakdown with enhanced styling
            st.subheader("Top 5 Skills Breakdown")
            for skill_raw in st.session_state.required_skills_raw:
                skill_norm = skill_raw.lower().strip()
                if skill_norm in st.session_state.matching_skills:
                    status_text = "✅ Matched"
                    status_class = "status-matched"
                else:
                    status_text = "❌ Gap"
                    status_class = "status-gap"
                
                st.markdown(f"""
                <div class="skill-card">
                    <strong style="font-size: 1.1rem;">{skill_raw}</strong>
                    <div class="status-badge {status_class}">{status_text}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.header("Your Personalized Learning Roadmap")
            
            if st.session_state.missing_skills_raw and st.session_state.roadmap_steps:
                st.info(f"Here is your 3-step plan to master the skills you need for a **{st.session_state.target_career}** role.")
                
                cols = st.columns([1, 0.1, 1, 0.1, 1])
                
                for i, step in enumerate(st.session_state.roadmap_steps):
                    col_index = i * 2
                    with cols[col_index]:
                        step_title = step.get('step_title', f'Step {i+1}').replace(f'{i+1}. ', '')
                        if st.button(f"**Step {i+1}:** {step_title}", key=f"step_block_{i}", use_container_width=True, help=f"Click for details on Step {i+1}"):
                            st.session_state.selected_step = i
                    
                    if i < len(st.session_state.roadmap_steps) - 1:
                        cols[col_index + 1].markdown("<div style='text-align: center; font-size: 2rem; color: #64b5f6; padding-top: 0.5rem;'>&rarr;</div>", unsafe_allow_html=True)
                
                if st.session_state.selected_step is not None:
                    selected_step_data = st.session_state.roadmap_steps[st.session_state.selected_step]
                    step_num = st.session_state.selected_step + 1
                    step_title = selected_step_data.get('step_title', f'Step {step_num}').replace(f'{step_num}. ', '')
                    
                    @st.dialog(f"Step {step_num}: {step_title}", width="large")
                    def show_step_modal():
                        st.markdown(f"### 🎯 **Objective:** {selected_step_data.get('description', 'N/A')}")
                        st.divider()
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### 🛠️ Hands-on Project")
                            st.info(selected_step_data.get('project', 'No project suggested.'))
                        with col2:
                            st.markdown("#### 📖 Learning Resource")
                            resource_url = selected_step_data.get('resource', '#')
                            st.markdown(f'<a href="{resource_url}" target="_blank" class="resource-link-button">🔗 Access Resource</a>', unsafe_allow_html=True)
                        
                        st.write("")
                        if st.button("Close", use_container_width=True):
                            st.session_state.selected_step = None
                            st.rerun()
                    
                    show_step_modal()

            elif not st.session_state.missing_skills_raw and st.session_state.required_skills_raw:
                st.balloons()
                st.success(f"**Congratulations! 🎉** You appear to have all the top required skills for a **{st.session_state.target_career}** role. Keep building on your strengths!")
            
            else:
                st.warning("Could not generate a roadmap. This may happen if the analysis was interrupted or the target role is very niche. Please try again.")

        st.markdown('</div>', unsafe_allow_html=True)