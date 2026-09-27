import streamlit as st
from main import generate_report, save_report, MODEL
from openai import APIStatusError, APIConnectionError

st.set_page_config(page_title="AI Research Agent", page_icon="🔎")

st.title("🔎 AI Research Agent")
st.caption(f"Powered by Grok — model: {MODEL}")

topic = st.text_input("Enter a research topic:")

if st.button("Generate Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Connecting to Grok and generating your report..."):
            try:
                report = generate_report(topic)
                if report:
                    filepath = save_report(topic, report)
                    st.success(f"Report generated and saved to `{filepath}`")
                    st.markdown(report)
                    st.download_button(
                        "Download report (.md)",
                        data=report,
                        file_name=filepath.name,
                        mime="text/markdown",
                    )
                else:
                    st.error("No report was generated. Please try again.")

            except APIStatusError as error:
                st.error(f"Grok API error (HTTP {error.status_code})")
                if error.status_code == 401:
                    st.info("Check your XAI_API_KEY.")
                elif error.status_code == 429:
                    st.info("Rate limit or usage quota reached.")
                else:
                    st.info(str(error))

            except APIConnectionError:
                st.error("Could not connect to the xAI API. Check your internet connection.")

            except Exception as error:
                st.error(f"Unexpected error: {error}")
