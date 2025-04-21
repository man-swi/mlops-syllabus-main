# Modules/streamlit/Assignments/problem3_sentiment.py

import streamlit as st
from textblob import TextBlob
import time # To simulate delay for spinner

# --- Page Configuration ---
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🎭",
    layout="centered"
)

# --- Function for Sentiment Analysis ---
def analyze_sentiment(text):
    """
    Performs sentiment analysis using TextBlob.
    Returns sentiment label, polarity score, and subjectivity score.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Classify polarity
    if polarity > 0.1: # Threshold can be adjusted
        sentiment = "Positive"
        emoji = "😊"
    elif polarity < -0.1: # Threshold can be adjusted
        sentiment = "Negative"
        emoji = "😠"
    else:
        sentiment = "Neutral"
        emoji = "😐"

    return sentiment, polarity, subjectivity, emoji

# --- Streamlit App Layout ---
st.title("🎭 Problem 3: Basic Sentiment Analysis")
st.markdown("""
Enter some text below and click 'Analyze' to determine its sentiment
(Positive, Negative, or Neutral).
""")

user_input = st.text_area("Enter Text Here:", height=150, placeholder="Type or paste your text...")

if st.button("Analyze Sentiment", key="sentiment_button"):
    if user_input:
        # Show a spinner while processing
        with st.spinner("Analyzing..."):
            # Simulate a short delay (optional, makes spinner more noticeable)
            # time.sleep(0.5)
            sentiment_label, polarity_score, subjectivity_score, sentiment_emoji = analyze_sentiment(user_input)

        st.subheader("Analysis Result")
        st.markdown(f"**Sentiment:** {sentiment_label} {sentiment_emoji}")

        # Display scores with explanations
        st.metric(label="Polarity Score", value=f"{polarity_score:.3f}")
        st.caption("Ranges from -1 (Negative) to +1 (Positive). Near 0 is Neutral.")

        st.metric(label="Subjectivity Score", value=f"{subjectivity_score:.3f}")
        st.caption("Ranges from 0 (Objective) to 1 (Subjective).")

        # Provide a simple interpretation bar (optional visualization)
        st.progress((polarity_score + 1) / 2) # Map -1 to 1 -> 0 to 1 for progress bar
        st.caption("Visual representation of polarity.")

    else:
        st.warning("Please enter some text to analyze.", icon="✍️")


# --- Optional: Add Footer ---
st.markdown("---")
st.text("Assignment 3 - Sentiment analysis using TextBlob.")