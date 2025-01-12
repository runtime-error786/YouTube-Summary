import streamlit as st
from utils import load_config
from transcript_handler import fetch_transcript, get_full_transcript, summarize_text_with_groq

def main():
    load_config()

    st.title("YouTube Video Transcript and Summary")
    st.write("Provide a YouTube video URL and select the transcript language.")

    video_url = st.text_input("YouTube Video URL", "")
    language = st.selectbox(
        "Select Transcript Language",
        ["en", "hi", "es", "fr", "auto-generated (Hindi)"],
        index=0,
    )

    if st.button("Fetch and Summarize"):
        if not video_url:
            st.error("Please provide a YouTube video URL.")
        else:
            lang_code = "hi" if language == "auto-generated (Hindi)" else language
            result = fetch_transcript(video_url, lang_code)
            if "error" in result:
                st.error(result["error"])
            else:
                full_transcript = get_full_transcript(result)
                st.subheader("Full Transcript")
                st.write(full_transcript)

                summary = summarize_text_with_groq(full_transcript)
                st.subheader("Summary")
                st.write(summary)

if __name__ == "__main__":
    main()
