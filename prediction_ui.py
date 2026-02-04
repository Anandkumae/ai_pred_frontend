"""
AI Prediction Interface with Model Selection

Interactive Streamlit UI for making predictions with good or bad model selection.
"""

import streamlit as st
import requests
import json
import os

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Page configuration
st.set_page_config(
    page_title="AI-Driven ML Failure Prediction Framework",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #1e1e1e;
        margin: 10px 0;
        color: white;
    }
    .prediction-box h4 {
        color: white;
        margin-top: 0;
    }
    .prediction-box ul {
        list-style-type: none;
        padding-left: 0;
    }
    .prediction-box li {
        color: white;
        padding: 5px 0;
    }
    .prediction-box strong {
        color: #ffffff;
    }
    .good-model {
        border-left: 5px solid #00C851;
        background-color: #1a2e1a;
    }
    .bad-model {
        border-left: 5px solid #ff4444;
        background-color: #2e1a1a;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.title("🤖 AI-Driven ML Failure Prediction Framework")
    st.caption("Predicting Machine Learning Model Failures Before Deployment or Retraining")
    st.markdown("---")
    
    # Sidebar - Model Selection
    st.sidebar.title("⚙️ Settings")
    
    model_choice = st.sidebar.selectbox(
        "Select Model",
        ["good", "bad"],
        help="Choose between the good model (high accuracy) or bad model (lower accuracy)"
    )
    
    # Model info
    if model_choice == "good":
        st.sidebar.success("✅ **Good Model Selected**")
        st.sidebar.info("This model has been trained with high-quality data and should provide accurate predictions.")
    else:
        st.sidebar.warning("⚠️ **Bad Model Selected**")
        st.sidebar.info("This model has been trained with lower-quality data and may provide less accurate predictions.")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About This Framework")
    st.sidebar.markdown("""
    **AI-Driven ML Failure Prediction**
    
    This framework helps predict ML model failures by:
    - Monitoring model confidence and performance
    - Detecting data drift (PSI)
    - Tracking concept drift (ADWIN)
    - Predicting failure probability
    - Comparing good vs degraded models
    
    **Use Cases:**
    - Pre-deployment validation
    - Retraining decision support
    - Model health monitoring
    - Performance degradation detection
    """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Input Features")
        
        # Input fields
        traffic_volume = st.number_input(
            "Traffic Volume",
            min_value=0,
            max_value=200,
            value=50,
            help="Number of vehicles"
        )
        
        time_of_day = st.slider(
            "Hour of Day",
            min_value=0,
            max_value=23,
            value=12,
            help="Hour in 24-hour format (0-23)"
        )
        
        day_of_week = st.slider(
            "Day of Week",
            min_value=0,
            max_value=6,
            value=2,
            help="0=Monday, 6=Sunday"
        )
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            weather_risk = st.selectbox(
                "Weather Risk",
                options=[0, 1, 2],
                index=1,
                help="0=Low, 1=Medium, 2=High"
            )
        
        with col_b:
            road_risk = st.selectbox(
                "Road Risk",
                options=[0, 1, 2],
                index=0,
                help="0=Low, 1=Medium, 2=High"
            )
        
        st.markdown("---")
        
        # Predict button
        if st.button("🚀 Make Prediction", type="primary", use_container_width=True):
            # Create payload
            payload = {
                "model_type": model_choice,
                "traffic_volume": traffic_volume,
                "time_of_day": time_of_day,
                "day_of_week": day_of_week,
                "weather_risk": weather_risk,
                "road_risk": road_risk
            }
            
            # Show loading spinner
            with st.spinner("Making prediction..."):
                try:
                    # Call API
                    response = requests.post(
                        f"{API_BASE_URL}/predict",
                        json=payload,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display results
                        st.success("✅ Prediction completed successfully!")
                        
                        # Results in columns
                        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
                        
                        with col_r1:
                            st.metric(
                                label="Prediction",
                                value=result["prediction"],
                                help="Predicted class (0 or 1)"
                            )
                        
                        with col_r2:
                            st.metric(
                                label="Confidence",
                                value=f"{result['confidence']:.2%}",
                                help="Model confidence in the prediction"
                            )
                        
                        with col_r3:
                            st.metric(
                                label="Latency",
                                value=f"{result['latency']*1000:.2f} ms",
                                help="Time taken for prediction"
                            )
                        
                        with col_r4:
                            st.metric(
                                label="Model Used",
                                value=result["model_type"].upper(),
                                help="Which model was used"
                            )
                        
                        st.markdown("---")
                        
                        # STEP 6: Model Health Risk (Based on Degradation)
                        st.subheader("🏥 Model Health Risk")
                        
                        # Fetch failure risk from API
                        try:
                            risk_response = requests.get(f"{API_BASE_URL}/failure-risk", timeout=5)
                            if risk_response.status_code == 200:
                                risk_data = risk_response.json()
                                
                                if "error" not in risk_data:
                                    risk_level = risk_data.get("risk", "UNKNOWN")
                                    degradation = risk_data.get("degradation", {})
                                    overall_deg = degradation.get("overall_degradation", 0)
                                    
                                    # Display risk based on degradation (STEP 6)
                                    if risk_level == "HIGH":
                                        st.error("🔴 **Model Likely to Collapse**")
                                        st.error(f"Degradation: {overall_deg:.1%} from baseline")
                                    elif risk_level == "MEDIUM":
                                        st.warning("🟡 **Model Degrading**")
                                        st.warning(f"Degradation: {overall_deg:.1%} from baseline")
                                    else:
                                        st.success("🟢 **Model Healthy**")
                                        st.success(f"Degradation: {overall_deg:.1%} from baseline")
                                    
                                    st.progress(min(1.0, overall_deg if overall_deg > 0 else result["confidence"]))
                                    
                                    # Show degradation details
                                    col_d1, col_d2, col_d3 = st.columns(3)
                                    with col_d1:
                                        st.metric(
                                            "Confidence Drop",
                                            f"{degradation.get('confidence_drop', 0):.2%}",
                                            help="How much confidence decreased from baseline"
                                        )
                                    with col_d2:
                                        st.metric(
                                            "PSI Increase",
                                            f"{degradation.get('psi_increase', 0):.2%}",
                                            help="How much drift increased from baseline"
                                        )
                                    with col_d3:
                                        st.metric(
                                            "Risk Level",
                                            risk_level,
                                            help="Overall failure risk"
                                        )
                                else:
                                    # Fallback to confidence-based
                                    confidence = result["confidence"]
                                    if confidence > 0.75:
                                        st.success("🟢 **Model Healthy** - High confidence prediction")
                                    elif confidence > 0.5:
                                        st.warning("🟡 **Model Risky** - Medium confidence, monitor closely")
                                    else:
                                        st.error("🔴 **Model Likely to Collapse** - Very low confidence!")
                                    st.progress(confidence)
                                    
                                    col_h1, col_h2, col_h3 = st.columns(3)
                                    with col_h1:
                                        st.metric("Confidence Score", f"{confidence:.2%}")
                                    with col_h2:
                                        health_status = "Healthy" if confidence > 0.75 else "Risky" if confidence > 0.5 else "Critical"
                                        st.metric("Health Status", health_status)
                                    with col_h3:
                                        risk_level = "Low" if confidence > 0.75 else "Medium" if confidence > 0.5 else "High"
                                        st.metric("Risk Level", risk_level)
                        except:
                            # Fallback if API fails
                            confidence = result["confidence"]
                            if confidence > 0.75:
                                st.success("🟢 **Model Healthy** - High confidence prediction")
                            elif confidence > 0.5:
                                st.warning("🟡 **Model Risky** - Medium confidence, monitor closely")
                            else:
                                st.error("🔴 **Model Likely to Collapse** - Very low confidence!")
                            st.progress(confidence)
                            
                            col_h1, col_h2, col_h3 = st.columns(3)
                            with col_h1:
                                st.metric("Confidence Score", f"{confidence:.2%}")
                            with col_h2:
                                health_status = "Healthy" if confidence > 0.75 else "Risky" if confidence > 0.5 else "Critical"
                                st.metric("Health Status", health_status)
                            with col_h3:
                                risk_level = "Low" if confidence > 0.75 else "Medium" if confidence > 0.5 else "High"
                                st.metric("Risk Level", risk_level)
                        
                        # Detailed response
                        with st.expander("📋 View Full Response"):
                            st.json(result)
                    
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        st.code(response.text)
                
                except requests.exceptions.ConnectionError:
                    st.error(f"❌ Connection failed! Is the API running at {API_BASE_URL}?")
                    st.info("Start the API with: `cd backend && uvicorn app:app --reload`")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.subheader("📝 Input Summary")
        
        # Display input summary
        model_class = "good-model" if model_choice == "good" else "bad-model"
        
        st.markdown(f"""
        <div class="prediction-box {model_class}">
            <h4>Current Configuration</h4>
            <ul>
                <li><strong>Model:</strong> {model_choice.upper()}</li>
                <li><strong>Traffic Volume:</strong> {traffic_volume}</li>
                <li><strong>Time:</strong> {time_of_day}:00</li>
                <li><strong>Day:</strong> {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][day_of_week]}</li>
                <li><strong>Weather Risk:</strong> {['Low', 'Medium', 'High'][weather_risk]}</li>
                <li><strong>Road Risk:</strong> {['Low', 'Medium', 'High'][road_risk]}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Model Comparison Section
        st.subheader("⚖️ Model Comparison")
        
        # Fetch failure risk data for comparison
        try:
            failure_risk_response = requests.get(f"{API_BASE_URL}/failure-risk", timeout=5)
            if failure_risk_response.status_code == 200:
                failure_data = failure_risk_response.json()
                
                col_comp1, col_comp2 = st.columns(2)
                
                with col_comp1:
                    st.markdown("**🟢 Good Model**")
                    st.metric(
                        "Expected Confidence",
                        "High (>75%)",
                        help="Good model typically maintains high confidence"
                    )
                    st.caption("✅ Stable performance")
                
                with col_comp2:
                    st.markdown("**🔴 Bad Model**")
                    st.metric(
                        "Expected Confidence",
                        "Low (<60%)",
                        help="Bad model typically shows lower confidence"
                    )
                    st.caption("⚠️ May degrade faster")
                
                # Show current system health
                st.markdown("**📊 Current System Health**")
                avg_confidence = failure_data.get("metrics", {}).get("avg_confidence", 0)
                failure_prob = failure_data.get("failure_probability", 0)
                
                col_sys1, col_sys2 = st.columns(2)
                with col_sys1:
                    st.metric("Avg Confidence", f"{avg_confidence:.2%}")
                with col_sys2:
                    st.metric("Failure Risk", f"{failure_prob:.2%}")
                
                # Health indicator
                if failure_prob < 0.3:
                    st.success("✅ System Healthy")
                elif failure_prob < 0.7:
                    st.warning("⚠️ System at Risk")
                else:
                    st.error("🚨 System Critical")
            else:
                # Fallback if API not available
                col_comp1, col_comp2 = st.columns(2)
                
                with col_comp1:
                    st.markdown("**🟢 Good Model**")
                    st.metric("Confidence", "High")
                    st.caption("✅ Stable")
                
                with col_comp2:
                    st.markdown("**🔴 Bad Model**")
                    st.metric("Confidence", "Low")
                    st.caption("⚠️ Risky")
        
        except Exception as e:
            # Simple comparison if API fails
            col_comp1, col_comp2 = st.columns(2)
            
            with col_comp1:
                st.markdown("**🟢 Good Model**")
                st.metric("Confidence", "High")
            
            with col_comp2:
                st.markdown("**🔴 Bad Model**")
                st.metric("Confidence", "Low")
        
        st.markdown("---")
        
        st.subheader("ℹ️ Tips")
        st.info("""
        **Model Comparison:**
        - Try the same inputs with both models
        - Compare confidence scores
        - Observe prediction differences
        
        **Best Practices:**
        - Use realistic traffic volumes
        - Consider time of day patterns
        - Account for weather conditions
        """)

if __name__ == "__main__":
    main()
