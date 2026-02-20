import streamlit as st
from groq import Groq

# 1. Browser ki tab ka naam aur icon
st.set_page_config(page_title="Wasif AI Bot", page_icon="🤖", layout="centered")

# 2. Sidebar mein extra features
with st.sidebar:
    st.title("⚙️ Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("Developed by **Wasif Pro Max**")

st.title("🤖 WASIF_PRO MAX ACADEMIC BOT")
st.caption("🚀 Powered by Llama 3.3 & Groq")
st.markdown("---")

# 3. Secure API Key Management
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("API Key nahi mili! Please Streamlit Secrets check karein.")
    st.stop()

client = Groq(api_key=api_key)

# 4. Chat History (Memory) set karna
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Purani chat screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User se input lena
if prompt := st.chat_input("Puchiye jo dil chahe (English or Roman Urdu)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot ka response
    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful academic assistant. Use English and Roman Urdu. Keep answers concise and helpful."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model="llama-3.3-70b-versatile",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            
            # Response ko history mein save karein
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Opps! Kuch masla hua hai: {e}")

