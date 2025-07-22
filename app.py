import os
import re
import datetime
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama3-70b-8192"

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found in .env file")
    st.stop()

# Groq API Client
class ChatGroq:
    def __init__(self, api_key, model_name):
        self.api_key = api_key
        self.model = model_name
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, prompt, max_tokens=6000):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": max_tokens
        }
        response = requests.post(self.endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# Initialize Groq client
llm = ChatGroq(GROQ_API_KEY, MODEL_NAME)

# Context and mood analysis
def get_context():
    return {
        "time": datetime.datetime.now().strftime("%H:%M"),
        "device": "mobile",
        "location": "home"
    }

def analyze_mood(text):
    prompt = f"Analyze the mood from this text in one short sentence:\n{text}"
    return llm.generate(prompt, 150)

# Recommendation generation
def generate_recommendations(context, mood, preferences):
    prompt = f"""
Generate recommendations based on the following details:
- Mood: {mood}
- Context: {context}
- Preferences: {preferences}

For each of the categories listed below, please provide exactly 10 recommendations in the format shown:

🎥 Videos:
1. [Video Title] - [YouTube URL]
2. [Video Title] - [YouTube URL]
...
10. [Video Title] - [YouTube URL]

🎬 Movies:
1. [Movie Title] - [Streaming Service] - [Trending/Popularity/Rating Details]
2. [Movie Title] - [Streaming Service] - [Trending/Popularity/Rating Details]
...
10. [Movie Title] - [Streaming Service] - [Trending/Popularity/Rating Details]

🎵 Songs:
1. [Song Title] - [Artist] - [URL]
2. [Song Title] - [Artist] - [URL]
...
10. [Song Title] - [Artist] - [URL]

🛍️ Products:
1. [Product/App Name] - [URL] - [Reason]
2. [Product/App Name] - [URL] - [Reason]
...
10. [Product/App Name] - [URL] - [Reason]

🎮 Games:
1. [Game Title] - [Platform]
2. [Game Title] - [Platform]
...
10. [Game Title] - [Platform]

📖 Articles:
1. [Article Title] - [URL]
2. [Article Title] - [URL]
...
10. [Article Title] - [URL]

💞 Connect:
1. [Social/Dating Idea] - [URL]
2. [Social/Dating Idea] - [URL]
...
10. [Social/Dating Idea] - [URL]

✈️ Travel:
1. [Destination] - [URL]
2. [Destination] - [URL]
...
10. [Destination] - [URL]

🍽️ Food:
1. [Meal Idea] - [URL]
2. [Meal Idea] - [URL]
...
10. [Meal Idea] - [URL]

🍿 Cine Magic:
1. [Movie/Show Title] - [Streaming Service] - [URL]
2. [Movie/Show Title] - [Streaming Service] - [URL]
...
10. [Movie/Show Title] - [Streaming Service] - [URL]
"""
    return llm.generate(prompt, 6000)

# Streamlit UI configuration with a robotic, futuristic dark theme
st.set_page_config(page_title="MoodX Machina", layout="wide")

st.markdown("""
<style>
/* Global futuristic style */
body {
    background-color: #000000 !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #000000;
}

/* Custom glowing fonts and UI */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

html, body, * {
    font-family: 'Orbitron', sans-serif;
    color: #f0f0f0;
}

/* Animated glowing title */
.glow-title {
    font-size: 2.5em;
    text-align: left;
    animation: glow 2s ease-in-out infinite alternate;
    color: #f72585;
    text-shadow: 0 0 5px #f72585, 0 0 10px #7209b7, 0 0 20px #3a0ca3;
}

@keyframes glow {
    from {
        text-shadow: 0 0 5px #f72585, 0 0 10px #7209b7, 0 0 20px #3a0ca3;
    }
    to {
        text-shadow: 0 0 10px #f72585, 0 0 20px #7209b7, 0 0 30px #3a0ca3;
    }
}

/* Glowing module section */
.section {
    padding: 25px;
    border-radius: 15px;
    margin: 20px 0;
    background: #111111;
    border: 1px solid #7209b7;
    box-shadow: 0 0 15px #f72585, 0 0 20px #7209b7 inset;
}

/* Glowing headers */
.header {
    color: #f72585;
    font-size: 1.6em;
    margin-bottom: 15px;
    text-shadow: 0 0 5px #f72585, 0 0 10px #7209b7;
}

/* Neon glowing item blocks */
.item {
    margin: 15px 0;
    padding: 15px;
    border-left: 4px solid #7209b7;
    background: rgba(255, 255, 255, 0.05);
    box-shadow: 0 0 8px #3a0ca3;
    transition: transform 0.2s;
}
.item:hover {
    transform: scale(1.03);
    box-shadow: 0 0 12px #f72585;
}

/* Tabs styling */
[data-testid="stTabs"] button {
    background-color: #111111;
    color: #f0f0f0;
    border: none;
    border-radius: 0;
    border-bottom: 3px solid #7209b7;
    transition: all 0.3s ease;
}
[data-testid="stTabs"] button:hover {
    color: #f72585;
    border-bottom: 3px solid #f72585;
    box-shadow: 0 0 5px #f72585;
}
[data-testid="stTabs"] button[data-selected="true"] {
    background-color: #1a1a1a;
    border-bottom: 3px solid #f72585;
    box-shadow: 0 0 10px #f72585;
}

/* Input text area glow */
textarea {
    background-color: #0d0d0d !important;
    color: #f0f0f0 !important;
    border: 1px solid #f72585 !important;
    box-shadow: 0 0 5px #f72585 inset !important;
}

/* Button styling */
button[kind="primary"] {
    background-color: #f72585;
    color: white;
    box-shadow: 0 0 10px #f72585;
}
button[kind="primary"]:hover {
    background-color: #7209b7;
    box-shadow: 0 0 15px #7209b7;
}

/* Image styling */
.stImage > img {
    border: 2px solid #f72585;
    border-radius: 10px;
    box-shadow: 0 0 10px #f72585;
}
</style>
""", unsafe_allow_html=True)

# Create a two-column layout
col1, col2 = st.columns([1, 2])

with col1:
    # Image (ensure j.png exists in your project directory)
    st.image("j.png", caption="MoodX Machina Visual", use_column_width=True)

with col2:
    st.markdown("<div class='glow-title'>🤖 MoodX Machina</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color: #f0f0f0; font-size: 1.2em;'>
        Welcome to MoodX Machina, MoodX Machina is an AI-powered recommendation engine that analyzes your mood and preferences 
        to deliver personalized suggestions across multiple categories, including videos, movies, songs, 
        products, games, articles, social connections, travel destinations, and food. 
        By leveraging advanced AI, it curates tailored experiences to match your current vibe, 
        helping you discover new content and activities that resonate with you!
    </div>
    """, unsafe_allow_html=True)

# Create a centered input panel for user inputs
with st.container():
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='input-panel'>", unsafe_allow_html=True)
        user_input = st.text_area("Tell us how you're feeling:", "I'm excited and looking for new adventures!")
        st.markdown("</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='input-panel'>", unsafe_allow_html=True)
        st.write("Preferences")
        lang = st.selectbox("Language", ["English", "Hindi", "Spanish", "Mandarin"])
        include_products = st.checkbox("Include Products", True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Button to generate recommendations (centered)
st.markdown("<div style='text-align: center; margin: 20px;'>", unsafe_allow_html=True)
if st.button("Generate Recommendations"):
    with st.spinner("Analyzing mood and generating recommendations..."):
        # Get context and mood
        context = get_context()
        mood = analyze_mood(user_input)
        
        # Generate recommendations using updated max_tokens
        preferences = {"language": lang, "include_products": include_products}
        recommendations = generate_recommendations(context, mood, preferences)
        
        # Parse recommendations into sections
        sections = {}
        current_section = None
        valid_sections = ["🎥 Videos", "🎬 Movies", "🎵 Songs", "🛍️ Products",
                          "🎮 Games", "📖 Articles", "💞 Connect", "✈️ Travel",
                          "🍽️ Food", "🍿 Cine Magic"]
        for line in recommendations.split('\n'):
            line = line.strip()
            if any(line.startswith(section) for section in valid_sections):
                current_section = line.split(':', 1)[0].strip()
                sections[current_section] = []
            elif current_section and line:
                sections[current_section].append(line)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Define tab names and ordering; "Cine Magic" comes first
        tab_names = {
            "🍿 Cine Magic": "🍿 Cine Magic",
            "🎵 Songs": "🎵 Jam Sessions",
            "🛍️ Products": "🛒 Hot Buys",
            "🎮 Games": "🎮 Game On",
            "📖 Articles": "📚 Thoughtful Reads",
            "🎥 Videos": "📹 Video Vibes",
            "💞 Connect": "💞 Social Sparks",
            "✈️ Travel": "✈️ Wanderlust Escapes",
            "🍽️ Food": "🍽️ Mood Meals"
        }
        ordered_sections = ["🍿 Cine Magic", "🎵 Songs", "🛍️ Products", "🎮 Games",
                            "📖 Articles", "🎥 Videos", "💞 Connect", "✈️ Travel",
                            "🍽️ Food"]
        tabs = st.tabs([tab_names[sec] for sec in ordered_sections])
        
        # Populate each tab with the corresponding recommendations
        with tabs[0]:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("<div class='header'>🍿 Cine Magic</div>", unsafe_allow_html=True)
            for line in sections.get("🍿 Cine Magic", []):
                if match := re.match(r'^\d+\.\s*(.+?)\s*-\s*(.+?)\s*-\s*(.+)', line):
                    st.markdown(f"""
                    <div class="item">
                        <b>{match.group(1)}</b><br>
                        <em>{match.group(2)}</em><br>
                        <a href="{match.group(3)}" target="_blank">Watch Now</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[1]:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("<div class='header'>🎵 Jam Sessions</div>", unsafe_allow_html=True)
            for line in sections.get("🎵 Songs", []):
                if match := re.match(r'^\d+\.\s*(.+?)\s*-\s*(.+?)\s*-\s*(.+)', line):
                    st.markdown(f"""
                    <div class="item">
                        <b>{match.group(1)}</b> by {match.group(2)}<br>
                        <a href="{match.group(3)}" target="_blank">Listen Now</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[2]:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("<div class='header'>🛒 Hot Buys</div>", unsafe_allow_html=True)
            for line in sections.get("🛍️ Products", []):
                if match := re.match(r'^\d+\.\s*(.+?)\s*-\s*(.+?)\s*-\s*(.+)', line):
                    st.markdown(f"""
                    <div class="item">
                        <b>{match.group(1)}</b><br>
                        {match.group(3)}<br>
                        <a href="{match.group(2)}" target="_blank">View Product</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[3]:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("<div class='header'>🎮 Game On</div>", unsafe_allow_html=True)
            for line in sections.get("🎮 Games", []):
                if match := re.match(r'^\d+\.\s*(.+?)\s*-\s*(.+)', line):
                    st.markdown(f"""
                    <div class="item">
                        <b>{match.group(1)}</b><br>
                        <em>Platform: {match.group(2)}</em>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[4]:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("<div class='header'>📚 Thoughtful Reads</div>", unsafe_allow_html=True)
            for line in sections.get("📖 Articles", []):
                if match := re.match(r'^\d+\.\s*(.+?)\s*-\s*(.+)', line):
                    st.markdown(f"""
                    <div class="item">
                        <b>{match.group(1)}</b><br>
                        <a href="{match.group(2)}" target="_blank">Read More</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[5]:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("<div class='header'>📹 Video Vibes</div>", unsafe_allow_html=True)
            for line in sections.get("🎥 Videos", []):
                if match := re.match(r'^\d+\.\s*(.+?)\s*-\s*(.+)', line):
                    st.markdown(f"""
                    <div class="item">
                        <b>{match.group(1)}</b><br>
                        <a href="{match.group(2)}" target="_blank">Watch Now</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[6]:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("<div class='header'>💞 Social Sparks</div>", unsafe_allow_html=True)
            for line in sections.get("💞 Connect", []):
                if match := re.match(r'^\d+\.\s*(.+?)\s*-\s*(.+)', line):
                    st.markdown(f"""
                    <div class="item">
                        <b>{match.group(1)}</b><br>
                        <a href="{match.group(2)}" target="_blank">Explore</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[7]:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("<div class='header'>✈️ Wanderlust Escapes</div>", unsafe_allow_html=True)
            for line in sections.get("✈️ Travel", []):
                if match := re.match(r'^\d+\.\s*(.+?)\s*-\s*(.+)', line):
                    st.markdown(f"""
                    <div class="item">
                        <b>{match.group(1)}</b><br>
                        <a href="{match.group(2)}" target="_blank">Discover</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[8]:
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("<div class='header'>🍽️ Mood Meals</div>", unsafe_allow_html=True)
            for line in sections.get("🍽️ Food", []):
                if match := re.match(r'^\d+\.\s*(.+?)\s*-\s*(.+)', line):
                    st.markdown(f"""
                    <div class="item">
                        <b>{match.group(1)}</b><br>
                        <a href="{match.group(2)}" target="_blank">Explore Recipe</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.success("Recommendations generated successfully, Captain!")