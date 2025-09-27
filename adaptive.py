import streamlit as st
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class AdaptiveLearning:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=3)
        self.data_points = []
        
    def update_user_model(self, user_data):
        features = np.array([[
            user_data['quiz_scores'],
            user_data['time_spent'],
            user_data['interaction_type']
        ]])
        
        # Add new data point
        self.data_points.append(features[0])
        
        # If we have less than 3 data points, duplicate them to meet minimum cluster requirement
        if len(self.data_points) < 3:
            while len(self.data_points) < 3:
                self.data_points.append(self.data_points[-1])
        
        # Convert to numpy array and reshape
        all_features = np.array(self.data_points)
        
        # Scale the features
        scaled_features = self.scaler.fit_transform(all_features)
        
        # Fit the model
        self.model.fit(scaled_features)
        
    def get_learning_style(self, user_data):
        features = np.array([[
            user_data['quiz_scores'],
            user_data['time_spent'],
            user_data['interaction_type']
        ]])
        scaled_features = self.scaler.transform(features)
        return self.model.predict(scaled_features)[0]
    
    def recommend_content(self, learning_style):
        
        content_types = {
            0: "Visual content with interactive elements",
            1: "Text-based in-depth explanations",
            2: "Audio lectures with quizzes"
        }
        return content_types.get(learning_style, "Mixed content")

def run_adaptive_learning():
    # Custom styled header
    st.markdown("""
        <h2 style='color: #fff; margin-bottom: 20px; text-align: center; 
                 font-family: Inter, Arial, sans-serif;'>🧠 Adaptive Learning</h2>
        <p style='color: #fff; text-align: center; margin-bottom: 30px; 
                  font-family: Inter, Arial, sans-serif;'>
            Personalize your learning experience based on your preferences and performance.
        </p>
    """, unsafe_allow_html=True)
    
    if 'adaptive_model' not in st.session_state:
        st.session_state.adaptive_model = AdaptiveLearning()
    
    # Input container
    st.markdown("""
        <div style='background: #1a1a1a; padding: 25px; border-radius: 12px; 
                    margin-bottom: 20px; border: 1px solid #333;'>
            <h3 style='color: #fff; margin-bottom: 20px; font-size: 1.2rem; 
                      font-family: Inter, Arial, sans-serif;'>Your Learning Profile</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<p style='color: #fff; margin-bottom: 10px;'>Recent Quiz Score</p>", 
                   unsafe_allow_html=True)
        quiz_score = st.slider("", 0, 100, 50, label_visibility="collapsed")
        
    with col2:
        st.markdown("<p style='color: #fff; margin-bottom: 10px;'>Time Spent Learning (minutes)</p>", 
                   unsafe_allow_html=True)
        time_spent = st.slider("", 0, 120, 60, label_visibility="collapsed")
    
    st.markdown("<p style='color: #fff; margin: 15px 0 10px 0;'>Preferred Learning Style</p>", 
               unsafe_allow_html=True)
    interaction_type = st.selectbox("", 
                                  ["Visual", "Textual", "Auditory"],
                                  label_visibility="collapsed")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        update_button = st.button("Update Learning Profile", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if update_button:
        st.markdown("""
            <div class='loading-spinner'></div>
            <div class='loading-text'>Analyzing your learning style...</div>
        """, unsafe_allow_html=True)
        
        user_data = {
            'quiz_scores': quiz_score,
            'time_spent': time_spent,
            'interaction_type': ["Visual", "Textual", "Auditory"].index(interaction_type)
        }
        
        st.session_state.adaptive_model.update_user_model(user_data)
        learning_style = st.session_state.adaptive_model.get_learning_style(user_data)
        recommendation = st.session_state.adaptive_model.recommend_content(learning_style)
        
        # Results container
        st.markdown(f"""
            <div style='background: #1a1a1a; padding: 25px; border-radius: 12px; 
                        margin-top: 20px; border: 1px solid #333;'>
                <div style='background: #2c3e50; padding: 15px; border-radius: 8px; 
                           margin-bottom: 15px; color: #fff;'>
                    ✨ Your learning profile has been successfully updated!
                </div>
                <div style='background: #34495e; padding: 15px; border-radius: 8px; color: #fff;'>
                    <strong>Recommended Learning Approach:</strong><br>
                    {recommendation}
                </div>
            </div>
        """, unsafe_allow_html=True)
