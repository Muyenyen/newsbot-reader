
import streamlit as st
from email_reader import fetch_filtered_emails

st.set_page_config(page_title="📥 Filtered Gmail Reader", layout="wide")
st.title("📥 Read Gmail with Sender Filtering + Link/Text Options")

email_address = st.text_input("Your Gmail address")
app_password = st.text_input("Gmail App Password", type="password")
senders_filter = st.text_area("Only fetch emails from these senders (comma-separated)", "alerts@industryinsights.com, news@hotelsource.com")
allowed_senders = [s.strip() for s in senders_filter.split(",") if s.strip()]

# Extraction options
extract_links = st.checkbox("Extract links", value=True)
extract_text = st.checkbox("Extract plain text", value=True)

if st.button("Fetch Emails"):
    if not extract_links and not extract_text:
        st.warning("Please select at least one extraction option.")
    else:
        with st.spinner("Connecting to Gmail and fetching messages..."):
            results = fetch_filtered_emails(
                username=email_address,
                app_password=app_password,
                allowed_senders=allowed_senders,
                extract_links=extract_links,
                extract_text=extract_text,
                num_emails=15
            )

            if not results:
                st.info("No matching emails found.")
            else:
                for idx, item in enumerate(results, 1):
                    st.markdown(f"### ✉️ Email #{idx} — From: `{item['from']}`")
                    if extract_links and item["links"]:
                        st.markdown("**🔗 Links Found:**")
                        for link in item["links"]:
                            st.markdown(f"- {link}")
                    if extract_text and item["text"]:
                        st.markdown("**📝 Text:**")
                        st.text_area("", item["text"], height=150)
