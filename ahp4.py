import streamlit as st
import numpy as np
import pandas as pd
import base64

# --- AHP Mathematical Constants ---
RI_DICT = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

# --- Tourist Profiles & Criteria Mapping (10 Unique Criteria Total) ---
TOURIST_PROFILES = {
    "Leisure Tourist": [
        "Cleanliness & Room Comfort", 
        "Rating & Brand", 
        "Price", 
        "Satisfaction", 
        "Hotel Facilities"
    ],
    "Business Tourist": [
        "Informing", 
        "Location & Comfort", 
        "Network Services", 
        "Price", 
        "Hotel Facilities"
    ],
    "Family Trip Tourist": [
        "Hotel Facilities", 
        "Safety & Security", 
        "Satisfaction", 
        "Price", 
        "Hotel Staff & Services"
    ]
}

# --- State & Hotel Alternatives Mapping ---
STATE_HOTELS = {
    "Negeri Sembilan": ["Lexis Hibiscus Port Dickson", "Palm Seremban Hotel", "Royale Chulan Seremban", "The Dusun", "d'Sora Boutique Business Hotel"],
    "Penang": ["Hard Rock Hotel Penang", "Areca Hotel Penang", "The Granite Luxury Hotel", "Lost Paradise Resort", "Amari SPICE Penang"],
    "Sabah": ["The Cara Boutique Hotel Kota Kinabalu", "Sabah Hotel Sandakan", "Cotton Houz by Ayuhouz", "Hilton Kota Kinabalu", "Monocolo Boutique Hotel"],
    "Perak": ["WEIL Hotel", "M Boutique Ipoh", "TUI BLUE The Haven Ipoh", "AVI Pangkor Beach Resort", "Kinta Riverfront Hotel & Suites"],
    "Kuala Lumpur": ["Lanson Place Bukit Ceylon", "Kloe Hotel", "The Majestic Hotel Kuala Lumpur", "The Chow Kit", "Hotel Stripes Kuala Lumpur"],
    "Selangor": ["Golden Palm Tree Malaysia", "Villa Chee", "Double Tree by Hilton Shah Alam i-City", "Royale Chulan Damansara", "Artisan Eco Hotel"],
    "Johor": ["Holiday Inn Johor Bahru City Centre", "Hard Rock Hotel Desaru Coast", "Miyabi Hotel Permas", "Berjaya Waterfront Hotel, Johor Bahru", "Amari Johor Bahru"],
    "Melaka": ["Timez Modern Heritage Hotel", "Baba House Melaka", "Swiss Garden Hotel Melaka", "Hatten Hotel Melaka", "Liu Men Hotel"],
    "Sarawak": ["Legacy Hill Hotel Kuching", "Theatre Hotel Kuching", "Damai Beach Resort", "City Rise Hotel", "Miri Marriott Resort & Spa"],
    "Pahang": ["Ancasa Royale Pekan Pahang", "Zenith Hotel Kuantan", "Oakwood Cameron Highlands", "The Yanné, Onsen Hotel", "Swiss-Belhotel Kuantan"],
    "Terengganu": ["Perhentian Marriott Resort & Spa", "Laguna Redang Island Resort", "Paya Bunga Hotel Terengganu", "The Payang Hotel", "Sutra Beach Resort Terengganu"],
    "Kedah": ["Royale Signature Hotel", "Aloft Langkawi Pantai Tengah", "Mercure Langkawi Pantai Cenang", "Grand Alora Hotel", "Raia Hotel & Convention Centre Alor Setar"],
    "Perlis": ["Elisa Hotel & Suites", "Putra Brasmana Hotel", "Vilana Hotel", "All In Hotel", "Savana Hotel & Serviced Apartments"]
}

# --- Developer Automated Objective Matrix (Saaty 1-9 Scale) ---
HOTEL_OBJECTIVE_SCORES = {
    "Negeri Sembilan": {
        "Cleanliness & Room Comfort": [9, 5, 7, 8, 6],
        "Price":                      [2, 9, 6, 4, 8], 
        "Satisfaction":               [9, 5, 7, 8, 6],
        "Hotel Facilities":           [9, 3, 7, 5, 4],
        "Rating & Brand":             [9, 4, 7, 6, 5],
        "Informing":                  [7, 6, 7, 5, 8],
        "Location & Comfort":         [8, 7, 8, 5, 8],
        "Network Services":           [7, 7, 7, 3, 8],
        "Safety & Security":          [9, 6, 8, 5, 7],
        "Hotel Staff & Services":     [9, 5, 7, 8, 6]
    },
    "Penang": {
        "Cleanliness & Room Comfort": [8, 7, 8, 6, 7],
        "Price":                      [3, 7, 5, 6, 5],
        "Satisfaction":               [9, 8, 8, 7, 8],
        "Hotel Facilities":           [9, 4, 8, 5, 8],
        "Rating & Brand":             [9, 6, 8, 5, 8],
        "Informing":                  [8, 7, 8, 6, 7],
        "Location & Comfort":         [8, 9, 8, 7, 8],
        "Network Services":           [8, 7, 8, 6, 7],
        "Safety & Security":          [8, 7, 8, 6, 7],
        "Hotel Staff & Services":     [9, 8, 7, 7, 7]
    },
    "Sabah": {
        "Cleanliness & Room Comfort": [8, 6, 5, 9, 6],
        "Price":                      [5, 6, 8, 3, 7],
        "Satisfaction":               [8, 6, 5, 9, 7],
        "Hotel Facilities":           [5, 7, 3, 9, 5],
        "Rating & Brand":             [6, 7, 4, 9, 5],
        "Informing":                  [7, 6, 5, 8, 7],
        "Location & Comfort":         [8, 7, 5, 9, 7],
        "Network Services":           [8, 7, 5, 9, 7],
        "Safety & Security":          [8, 7, 4, 9, 7],
        "Hotel Staff & Services":     [8, 6, 5, 9, 7]
    },
    "Perak": {
        "Cleanliness & Room Comfort": [8, 7, 9, 6, 6],
        "Price":                      [5, 6, 3, 6, 7],
        "Satisfaction":               [8, 8, 9, 7, 6],
        "Hotel Facilities":           [7, 5, 9, 6, 7],
        "Rating & Brand":             [8, 7, 9, 6, 7],
        "Informing":                  [7, 8, 7, 6, 7],
        "Location & Comfort":         [9, 8, 7, 8, 8],
        "Network Services":           [8, 7, 7, 5, 7],
        "Safety & Security":          [8, 7, 9, 6, 7],
        "Hotel Staff & Services":     [8, 8, 9, 6, 7]
    },
    "Kuala Lumpur": {
        "Cleanliness & Room Comfort": [8, 7, 9, 7, 8],
        "Price":                      [4, 5, 2, 7, 6],
        "Satisfaction":               [8, 8, 9, 7, 8],
        "Hotel Facilities":           [8, 6, 9, 5, 7],
        "Rating & Brand":             [8, 7, 9, 7, 8],
        "Informing":                  [7, 8, 8, 8, 7],
        "Location & Comfort":         [8, 8, 8, 9, 8],
        "Network Services":           [8, 8, 9, 7, 8],
        "Safety & Security":          [8, 7, 9, 7, 8],
        "Hotel Staff & Services":     [8, 8, 9, 8, 8]
    },
    "Selangor": {
        "Cleanliness & Room Comfort": [8, 6, 9, 8, 6],
        "Price":                      [3, 8, 5, 6, 9],
        "Satisfaction":               [7, 7, 8, 7, 6],
        "Hotel Facilities":           [9, 4, 9, 8, 3],
        "Rating & Brand":             [8, 5, 9, 8, 4],
        "Informing":                  [6, 6, 8, 7, 7],
        "Location & Comfort":         [7, 6, 9, 8, 7],
        "Network Services":           [7, 5, 9, 8, 7],
        "Safety & Security":          [8, 5, 9, 8, 6],
        "Hotel Staff & Services":     [7, 6, 8, 8, 6]
    },
    "Johor": {
        "Cleanliness & Room Comfort": [8, 9, 6, 6, 8],
        "Price":                      [6, 2, 8, 6, 5],
        "Satisfaction":               [8, 9, 6, 6, 8],
        "Hotel Facilities":           [7, 9, 4, 6, 8],
        "Rating & Brand":             [8, 9, 5, 7, 8],
        "Informing":                  [7, 7, 6, 6, 8],
        "Location & Comfort":         [9, 7, 6, 7, 8],
        "Network Services":           [8, 7, 6, 6, 8],
        "Safety & Security":          [8, 9, 6, 6, 8],
        "Hotel Staff & Services":     [8, 9, 6, 6, 8]
    },
    "Melaka": {
        "Cleanliness & Room Comfort": [7, 8, 8, 7, 9],
        "Price":                      [7, 6, 5, 7, 3],
        "Satisfaction":               [8, 8, 7, 7, 9],
        "Hotel Facilities":           [4, 5, 8, 8, 6],
        "Rating & Brand":             [6, 7, 8, 8, 9],
        "Informing":                  [7, 8, 7, 7, 8],
        "Location & Comfort":         [8, 9, 7, 8, 9],
        "Network Services":           [7, 7, 8, 8, 8],
        "Safety & Security":          [7, 8, 8, 8, 9],
        "Hotel Staff & Services":     [8, 8, 7, 7, 9]
    },
    "Sarawak": {
        "Cleanliness & Room Comfort": [7, 8, 8, 6, 9],
        "Price":                      [7, 7, 4, 8, 3],
        "Satisfaction":               [7, 8, 8, 6, 9],
        "Hotel Facilities":           [5, 6, 8, 3, 9],
        "Rating & Brand":             [5, 7, 8, 5, 9],
        "Informing":                  [7, 8, 7, 6, 8],
        "Location & Comfort":         [7, 8, 7, 7, 9],
        "Network Services":           [7, 8, 7, 7, 8],
        "Safety & Security":          [7, 8, 8, 6, 9],
        "Hotel Staff & Services":     [7, 8, 7, 6, 9]
    },
    "Pahang": {
        "Cleanliness & Room Comfort": [7, 8, 8, 9, 8],
        "Price":                      [6, 5, 5, 2, 6],
        "Satisfaction":               [7, 8, 8, 9, 8],
        "Hotel Facilities":           [6, 8, 6, 9, 7],
        "Rating & Brand":             [6, 8, 7, 9, 7],
        "Informing":                  [7, 7, 7, 8, 7],
        "Location & Comfort":         [7, 8, 8, 7, 8],
        "Network Services":           [7, 8, 7, 8, 8],
        "Safety & Security":          [7, 8, 8, 9, 8],
        "Hotel Staff & Services":     [7, 8, 8, 9, 8]
    },
    "Terengganu": {
        "Cleanliness & Room Comfort": [9, 8, 7, 6, 7],
        "Price":                      [2, 4, 7, 8, 7],
        "Satisfaction":               [9, 8, 7, 6, 7],
        "Hotel Facilities":           [9, 8, 6, 4, 5],
        "Rating & Brand":             [9, 8, 7, 5, 6],
        "Informing":                  [8, 7, 7, 7, 6],
        "Location & Comfort":         [9, 8, 8, 8, 7],
        "Network Services":           [8, 7, 8, 7, 6],
        "Safety & Security":          [9, 8, 7, 6, 7],
        "Hotel Staff & Services":     [9, 8, 7, 6, 7]
    },
    "Kedah": {
        "Cleanliness & Room Comfort": [6, 8, 8, 7, 7],
        "Price":                      [7, 4, 5, 7, 7],
        "Satisfaction":               [6, 8, 8, 7, 7],
        "Hotel Facilities":           [5, 8, 8, 6, 6],
        "Rating & Brand":             [6, 8, 8, 6, 6],
        "Informing":                  [7, 8, 7, 7, 7],
        "Location & Comfort":         [7, 9, 9, 7, 6],
        "Network Services":           [7, 8, 8, 7, 7],
        "Safety & Security":          [7, 8, 8, 7, 7],
        "Hotel Staff & Services":     [7, 8, 8, 7, 7]
    },
    "Perlis": {
        "Cleanliness & Room Comfort": [7, 6, 7, 8, 7],
        "Price":                      [7, 8, 7, 8, 7],
        "Satisfaction":               [7, 6, 7, 8, 7],
        "Hotel Facilities":           [5, 5, 5, 6, 5],
        "Rating & Brand":             [5, 6, 5, 7, 5],
        "Informing":                  [7, 6, 7, 8, 7],
        "Location & Comfort":         [7, 8, 7, 8, 7],
        "Network Services":           [7, 7, 7, 8, 7],
        "Safety & Security":          [7, 7, 7, 8, 7],
        "Hotel Staff & Services":     [7, 6, 7, 8, 7]
    }
}

# --- Helper Function: AHP Math & Consistency ---
def calculate_ahp_weights_and_cr(matrix):
    n = matrix.shape[0]
    col_sums = matrix.sum(axis=0)
    norm_matrix = matrix / col_sums
    weights = norm_matrix.mean(axis=1)
    
    if n <= 2:
        return weights, 0.0
        
    weighted_sum_vector = np.dot(matrix, weights)
    lambda_max = (weighted_sum_vector / weights).mean()
    ci = (lambda_max - n) / (n - 1)
    ri = RI_DICT.get(n, 1.12)
    cr = ci / ri
    
    return weights, cr

# --- Initialize Session State Variables ---
if 'tourist_type' not in st.session_state:
    st.session_state.tourist_type = "Leisure Tourist"
if 'criteria' not in st.session_state:
    st.session_state.criteria = TOURIST_PROFILES["Leisure Tourist"]
if 'selected_state' not in st.session_state:
    st.session_state.selected_state = "Negeri Sembilan"
if 'alternatives' not in st.session_state:
    st.session_state.alternatives = STATE_HOTELS["Negeri Sembilan"]

# --- Streamlit UI Configurations ---
st.set_page_config(page_title="Malaysia Hotel Selection AHP System", layout="wide")
st.set_option('client.showErrorDetails', False)

# Dynamic Styling injection
def add_custom_background():
    try:
        with open("background1.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        bg_style = f'background-image: url("data:image/png;base64,{encoded_string}");'
    except:
        bg_style = 'background-color: #f8fafc;'

    st.markdown(f"""
    <style>
    .stApp {{ {bg_style} background-size: cover; background-position: center; background-attachment: fixed; }}
    .block-container {{ padding: 2rem; max-width: 1250px; }}
    .main-card {{ background: rgba(255,255,255,0.96); border-radius: 22px; padding: 32px; margin-bottom: 28px; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 10px 30px rgba(0,0,0,0.06); }}
    .question-card {{ background: rgba(248,250,252,0.95); border-radius: 14px; padding: 20px; margin-bottom: 16px; border: 1px solid rgba(0,0,0,0.04); }}
    h1 {{ color: #0f172a !important; font-size: 36px !important; font-weight: 800 !important; }}
    h2, h3, h4 {{ color: #1e293b !important; font-weight: 700 !important; }}
    .stButton button {{ background: linear-gradient(135deg, #0f172a, #1e293b); color: white !important; border-radius: 10px; padding: 10px 24px; font-weight: 700; border:none; }}
    .winner-box {{ background: linear-gradient(135deg, #1e293b, #0f172a); padding:30px; border-radius:18px; border-left: 10px solid #10b981; margin-bottom:30px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }}
    .winner-box h1, .winner-box h3, .winner-box p, .winner-box span {{ color: #ffffff !important; }}
    </style>
    """, unsafe_allow_html=True)

add_custom_background()
st.title("🏨 Malaysia Hotel Selection AHP System")

# App Navigation Tabs Structure
tab1, tab2, tab3, tab4 = st.tabs(["1. Trip Details", "2. Criteria Assessment", "3. Objective Alternatives Matrix", "4. Final Hotel Ranking"])

# ==========================================
# TAB 1: Trip Details
# ==========================================
with tab1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header("Step 1: Define Your Trip")
    
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("1. What type of tourist are you?")
    selected_type = st.radio("Select your profile:", options=list(TOURIST_PROFILES.keys()))
    
    if selected_type != st.session_state.tourist_type:
        st.session_state.tourist_type = selected_type
        st.session_state.criteria = TOURIST_PROFILES[selected_type]
        st.rerun()
        
    st.info(f"Evaluation Criteria for {st.session_state.tourist_type}:**\n" + "\n".join([f"- {c}" for c in st.session_state.criteria]))
    st.markdown('</div>', unsafe_allow_html=True)  

    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.subheader("2. Where are you traveling?")
    selected_state = st.selectbox(
            "Select the state in Malaysia:",
            options=list(STATE_HOTELS.keys()),
            index=list(STATE_HOTELS.keys()).index(st.session_state.selected_state)
    )
    
    if selected_state != st.session_state.selected_state:
        st.session_state.selected_state = selected_state
        st.session_state.alternatives = STATE_HOTELS[selected_state]
        st.rerun()
        
    st.success(f"📌 **Comparing 5 regional hotel alternatives in {st.session_state.selected_state}:**\n" + "\n".join([f"{i+1}. {a}" for i, a in enumerate(st.session_state.alternatives)]))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 2 : CRITERIA ASSESSMENT (SORTED 1 TO 5)
# ==========================================
with tab2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header("Step 2: Rank Hotel Selection Criteria")
    st.write(
        "Arrange the criteria from MOST important "
        "(Rank 1) to LEAST important (Rank 5). "
        "The system automatically generates "
        "the AHP pairwise matrix."
    )
    
    criteria = st.session_state.criteria
    n_crit = len(criteria)
    rank_selection = {}

    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    for rank in range(1, n_crit + 1):
        col1, col2 = st.columns([0.5, 8])
        with col1:
            st.markdown(f'<div style="display:flex; align-items:center; justify-content:center; color:#0f172a; font-weight:800; font-size:22px; margin-top:28px;">{rank}.</div>', unsafe_allow_html=True)
        with col2:
            label = f"Rank {rank} (Most Important)" if rank == 1 else (f"Rank {rank} (Least Important)" if rank == n_crit else f"Rank {rank}")
            selected = st.selectbox(label, criteria, key=f"rank_{rank}", index=rank-1)
            rank_selection[rank] = selected
    st.markdown('</div>', unsafe_allow_html=True)

    # Validate distinct choices constraint
    selected_items = list(rank_selection.values())
    if len(set(selected_items)) != n_crit:
        st.error("Matrix generation failure: Each tracking metric constraint must assume exactly one isolated rank space index.")
    else:
        # Build pairwise matrix on the fly derived from absolute ranking distances
        criterion_rank = {criterion: rank for rank, criterion in rank_selection.items()}
        criteria_matrix = np.ones((n_crit, n_crit))
        for i in range(n_crit):
            for j in range(i+1, n_crit):
                diff = abs(criterion_rank[criteria[i]] - criterion_rank[criteria[j]])
                value = 1 if diff == 0 else (3 if diff == 1 else (5 if diff == 2 else (7 if diff == 3 else 9)))
                if criterion_rank[criteria[i]] < criterion_rank[criteria[j]]:
                    criteria_matrix[i,j], criteria_matrix[j,i] = value, 1/value
                else:
                    criteria_matrix[i,j], criteria_matrix[j,i] = 1/value, value
                    
        criteria_weights, crit_cr = calculate_ahp_weights_and_cr(criteria_matrix)

      # --- NEW ADDITION: Pairwise Comparison Value Table ---
        st.subheader("Generated Pairwise Matrix")
        st.write("This matrix is mathematically generated based on your ranking choices above:")
        
        matrix_df = pd.DataFrame(
            criteria_matrix, 
            index=criteria, 
            columns=criteria
        )
        # Displaying the matrix with 4 decimal places for reciprocals (e.g., 0.3333)
        st.dataframe(
            matrix_df.style.format("{:.4f}").background_gradient(cmap="Blues"), 
            use_container_width=True
        )
        st.caption(f"📊 **Consistency Ratio (CR):** {crit_cr:.4f} (Must be < 0.10 for mathematical validity)")
        st.divider()

        # --- Existing Leaderboard Section (Now positioned underneath) ---
        st.subheader("Criteria Weight")
        weight_df = pd.DataFrame({"Criterion": criteria, "Weight (%)": criteria_weights * 100})
        
        # Always sort descending by highest weight, reset index, and map 1 to 5
        weight_df = weight_df.sort_values(by="Weight (%)", ascending=False).reset_index(drop=True)
        weight_df.index = weight_df.index + 1
        
        st.dataframe(weight_df.style.format({"Weight (%)": "{:.2f}%"}), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 3: OBJECTIVE ALTERNATIVES MATRIX
# ==========================================
with tab3:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header(f"Step 3: Objective Saaty Intensity Matrix ({st.session_state.selected_state})")
    st.write("The matrix space below records the system-locked Saaty integer intensity scales ($1$ to $9$) mapping structural features across the profile bounds.")
    
    # Retrieve current active state dictionary block 
    state_scores = HOTEL_OBJECTIVE_SCORES[st.session_state.selected_state]
    active_scores = {crit: state_scores[crit] for crit in st.session_state.criteria}
    
    matrix_df = pd.DataFrame(active_scores, index=st.session_state.alternatives)
    st.dataframe(matrix_df.style.background_gradient(cmap="Blues"), use_container_width=True)
    st.caption("📈 *Scale Configuration: 1 = Marginal Performance Match | 5 = Strong Core Alignment | 9 = Absolute Dominance Factor*")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 4: SYNTHESIS OPTIMIZATION ENGINE
# ==========================================
with tab4:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header("🏆 Final Hotel Selection Dashboard")
    
    if st.button("🚀 Calculate Final Ranking", key="calculate_results_btn"):
        # Compile local vector spaces from Saaty configuration map
        state_scores = HOTEL_OBJECTIVE_SCORES[st.session_state.selected_state]
        alt_weights_matrix = np.zeros((5, n_crit))
        
        for c_idx, criterion in enumerate(st.session_state.criteria):
            scores = np.array(state_scores[criterion])
            normalized_weights = scores / scores.sum()  # Column vector absolute scaling normalization
            alt_weights_matrix[:, c_idx] = normalized_weights
            
        # Linear aggregation via dot product matrix multiplication
        final_scores = np.dot(alt_weights_matrix, criteria_weights)
        
        results_df = pd.DataFrame({
            "Hotel Selection Alternative": st.session_state.alternatives,
            "Synthesis Score Profile": final_scores * 100 
        }).sort_values(by="Synthesis Score Profile", ascending=False).reset_index(drop=True)
        results_df.index = results_df.index + 1
        
        # Display optimal vector selection
        winner = results_df.iloc[0]
        st.markdown(f"""
            <div class="winner-box">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <h3 style="margin:0; font-size:13px; letter-spacing:2px; color:#a7f3d0 !important;">BEST HOTEL RECOMMENDATION</h3>
                        <h1 style="margin:10px 0 0 0; font-size:38px; color:#ffffff !important;">{winner['Hotel Selection Alternative']}</h1>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:36px;">🎯</span>
                        <p style="font-size:16px; margin:5px 0 0 0; color:#e2e8f0 !important;">Match {winner['Synthesis Score Profile']:.2f}%</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Output priority rank spaces
        st.subheader("📊 Hotel Ranking")
        for index, row in results_df.iterrows():
            col1, col2, col3 = st.columns([1.5, 4, 1.5])
            with col1:
                st.markdown(f"### Rank {index}")
            with col2:
                bar_color = "linear-gradient(90deg, #10b981, #34d399)" if index == 1 else ("linear-gradient(90deg, #0ea5e9, #38bdf8)" if index == 2 else "linear-gradient(90deg, #64748b, #94a3b8)")
                st.write(f"**{row['Hotel Selection Alternative']}**")
                st.markdown(f'<div style="background:#e2e8f0; border-radius:6px; height:18px; overflow:hidden;"><div style="background:{bar_color}; width:{row["Synthesis Score Profile"]:.2f}%; height:100%;"></div></div>', unsafe_allow_html=True)
            with col3:
                st.metric(label="Overall Priority Weight", value=f"{row['Synthesis Score Profile']:.2f}%")
            st.divider()
            
        with st.expander("View Full Detailed Score Table"):
            st.dataframe(results_df.style.background_gradient(cmap='Greens').format("{:.2f}%", subset=["Synthesis Score Profile"]), use_container_width=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
