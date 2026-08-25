import requests
import streamlit as st 
import json
 
if "result" not in st.session_state:
    st.session_state.result = None
if "profile" not in st.session_state:
    st.session_state.profile = None

st.set_page_config(layout="wide")
st.title("LinkedIn Multi-Agent AI System")

tab1, tab2 = st.tabs(["Brand Profile", "Generate Content"])

with tab1:
    st.subheader("Extract Your Brand Profile")
    st.text("Paste your company website URL to extract brand voice, pillars, and tone")
    
    website_url = st.text_input("Website URL", placeholder="https://example.com", key="website_url")
    
    if st.button("Extract Profile"):
        if not website_url:
            st.error("Please enter a website URL")
        else:
            with st.spinner("Scraping website and extracting profile..."):
                try:
                    response = requests.post(
                        "https://saloon-frosted-twins.ngrok-free.dev/extract-profile",
                        json={"website_url": website_url},
                        timeout=60
                    )
                    data = response.json()
                    if response.status_code == 200:
                        st.session_state.profile = data
                        st.success("✓ Profile extracted!")
                    else:
                        st.error(f"Failed to extract profile: {data.get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    if st.session_state.profile:
        profile = st.session_state.profile
        st.markdown("---")
        st.subheader("Extracted Profile")
        st.markdown(f"**Brand Name:** {profile['brand_name']}")
        st.markdown(f"**Voice:** {profile['voice']}")
        st.markdown(f"**Key Pillars:** {', '.join(profile['key_pillars'])}")
        st.markdown(f"**Tone Examples:**")
        for example in profile['tone_examples']:
            st.markdown(f"- *{example}*")
        
        st.download_button(
            label="Download Profile as JSON",
            data=json.dumps(profile, indent=2),
            file_name="brand_profile.json",
            mime="application/json"
        )

with tab2:
    st.subheader("Generate Branded LinkedIn Content")
    
    if not st.session_state.profile:
        st.warning("⚠️ Please extract a brand profile first (go to Brand Profile tab)")
    else:
        st.markdown(f"**Using profile:** {st.session_state.profile['brand_name']}")
        
        topic = st.text_input("Enter the topic for your post", key="topic", placeholder="e.g., 'luxury travel for solo explorers'")
        
        if st.button("Generate"):
            if not topic:
                st.error("Please enter a topic")
            else:
                with st.spinner("Running agents... this takes about 60 seconds"):
                    try:
                        response = requests.post(
                            "https://saloon-frosted-twins.ngrok-free.dev/generate",
                            json={"topic": topic, "profile": st.session_state.profile},
                            timeout=120
                        )
                        data = response.json()
                        if response.status_code == 200:
                            st.session_state.result = data
                            st.success("✓ Content generated!")
                        else:
                            st.error(f"Generation failed: {data.get('detail', 'Unknown error')}")
                    except requests.exceptions.JSONDecodeError:
                        st.error(f"Server returned an unexpected response (Status {response.status_code}).")
                        st.error(response.text)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    if st.session_state.result:
        result = st.session_state.result

        st.subheader("5 Hooks")
        for i, hook in enumerate(result["hooks"]):
            st.markdown(f"**{i+1}.** {hook}")

        st.subheader("Drafts")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Draft A**")
            st.write(result["drafts"][0])
        with col_b:
            st.markdown("**Draft B**")
            st.write(result["drafts"][1])

        st.subheader("Critic Scores")
        scores = result["scores"]
        st.markdown(f"**Recommended:** {scores['comparison']['better_draft']}")
        st.markdown(f"**Why:** {scores['comparison']['reason']}")
        st.markdown(f"**Suggested use:** {scores['comparison']['suggested_use']}")# deployed
# deployed
