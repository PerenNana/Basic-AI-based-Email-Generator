import streamlit as st
import requests
import streamlit.components.v1 as components

API_URL = "http://127.0.0.1:8000/generate_email"

st.set_page_config(page_title="Basic Email Generator", page_icon=":email:", layout="centered")

if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

if "sender_name" not in st.session_state:
    st.session_state.sender_name = ""

if "receiver_name" not in st.session_state:
    st.session_state.receiver_name = ""

if "subject" not in st.session_state:
    st.session_state.subject = ""

if "details" not in st.session_state:
    st.session_state.details = ""

st.title("📧 Basic Email Generator")

st.divider()

#Instructions
with st.expander("**📘 How to use it?**"):
    st.markdown("""
    1. Select the email category.
    2. Enter the receiver's name, subject, and details.
    3. Click the "Generate Email" button to get your generated email.
    """)

st.markdown("---")

st.header("Email category")

st.markdown("##### Select Email Category")

# 1. Email Category Selection

category = st.radio(
        "Choose a category for your Email",
        options=["Inquiry", "Complaint", "Thank you", "Request", "Information", "Confirmation", "Apology", "Reminder", "Invitation", "Other"],
        index=4,
        horizontal=True,
        help="Select one category."
    )

st.divider()

# 2. Input fields
col1, col2 = st.columns([6, 1])

with col2:
    clear_input = st.button("Clear", type="secondary")
    if clear_input:
        st.session_state.sender_name = ""
        st.session_state.receiver_name = ""
        st.session_state.subject = ""
        st.session_state.details = ""
        st.success("Input fields cleared.")

with col1:
    sender_name = st.text_input("From:", placeholder="Enter your name", key="sender_name")

    receiver_name = st.text_input("To:", placeholder="Enter the receiver's name", key="receiver_name")

    subject = st.text_input("Subject:", placeholder="Enter the subject", key="subject")

    details = st.text_area("Details:",
                           placeholder="Enter structured key information",
                           height= 200,
                           key="details"
                           )

st.divider()

# 3. Generate Button
generate = st.button("Generate Email", type="primary")

generate_email = ""

if generate:
    if not sender_name:
        st.warning("Please enter your name.")
    if not receiver_name:
        st.warning("Please enter a receiver's name.")
    elif not subject:
        st.warning("Please enter a subject.")
    elif not details:
        st.warning("Please enter details.")
    else:
        with st.spinner("Generating email..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "sender_name": sender_name,
                        "receiver_name": receiver_name,
                        "subject": subject,
                        "details": details,
                        "category": category
                    }
                )
                generated = response.json().get("generated_email", "No generation received")
                st.session_state.generated_email = generated
            except Exception as e:
                st.session_state.generated_email = f"Error generating email: {str(e)}"


        if "generated_email" in st.session_state:
            generate_email = st.session_state.generated_email
            st.header("🤖 Generated Email")

            col1, col2 = st.columns([6, 1])

            with col1:
                st.text_area(
                    label="Generated Email",
                    value=generate_email,
                    height=200,
                    key="generated_email",
                    help="Copy your generated Email with the button beneath."
                )

            with col2:
                # ⏩ Right-align the copy button using columns
                st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
                components.html(f"""
                                            <script>
                                            function copyToClipboard() {{
                                                navigator.clipboard.writeText(document.getElementById("copyTarget").innerText);
                                                alert("📋 Copied to clipboard!");
                                            }}
                                            </script>
                                            <div style="text-align:right;">
                                                <button onclick="copyToClipboard()" style="
                                                    background-color: #262730;
                                                    color: white;
                                                    border: 1px solid #5c5c5c;
                                                    border-radius: 10px;
                                                    padding: 8px 16px;
                                                    font-size: 14px;
                                                    cursor: pointer;
                                                ">Copy</button>
                                            </div>
                                            <div id="copyTarget" style="display:none;">{generate_email}</div>
                                        """, height=60)


st.divider()