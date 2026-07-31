import requests
import streamlit as st 
if "result" not in st.session_state:
    st.session_state.result = None
st.title("LinkedIn Multi-Agent AI System")
st.text("Let's start drafting your LinkedIn post!")
st.text_input("Enter the topic", key="topic")
topic = st.session_state.topic
if st.button("Generate"):
    response = requests.post("http://127.0.0.1:8000/generate", json={"topic": topic})
    data = response.json()
    if response.status_code == 200:
        st.session_state.result = data
    else:
        st.error(f"Generation failed: {data.get('detail', 'Unknown error')}")
if st.session_state.result:
    result = st.session_state.result
    
    # hooks
    st.subheader("5 Hooks")
    for i, hook in enumerate(result["hooks"]):
        st.markdown(f"**{i+1}.** {hook}")
    
    # drafts
    st.subheader("Drafts")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Draft A**")
        st.write(result["drafts"][0])
    with col_b:
        st.markdown("**Draft B**")
        st.write(result["drafts"][1])
    
    # scores
    st.subheader("Critic scores")
    scores = result["scores"]
    st.markdown(f"**Recommended:** {scores['comparison']['better_draft']}")
    st.markdown(f"**Why:** {scores['comparison']['reason']}")
    st.markdown(f"**Suggested use:** {scores['comparison']['suggested_use']}")