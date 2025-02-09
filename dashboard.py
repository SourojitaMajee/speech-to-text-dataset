import streamlit as st
import pandas as pd
import json
import string
import altair as alt
import plotly.express as px

# Set Streamlit page config
st.set_page_config(
    page_title="Speech Dataset Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.header("Upload Your JSONL File")
uploaded_file = st.sidebar.file_uploader("Upload a JSONL file", type=["jsonl"])

if uploaded_file is not None:
    # Read and load the JSONL file
    data = [json.loads(line) for line in uploaded_file]
    df = pd.DataFrame(data)

    # Compute statistics
    total_hours = df["duration"].sum() / 3600  # Convert seconds to hours
    total_utterances = len(df)
    all_text = " ".join(df["text"]).lower()
    unique_words = set(all_text.split())
    vocab_size = len(unique_words)  # Unique words
    alphabet = sorted(set(all_text) & set(string.ascii_lowercase))  # Unique characters
    alphabet_size = len(alphabet)

    # Compute words and characters per file
    df["word_count"] = df["text"].apply(lambda x: len(x.split()))
    df["char_count"] = df["text"].apply(len)

    # Display Key Statistics
    st.markdown("### **Key Statistics**")
    col1, col2, col3, col4 = st.columns(4)
    
    def styled_metric(label, value):
        st.markdown(
            f"""
            <div style='background-color: #f0f0f0; padding: 15px; border-radius: 10px; text-align: center;'>
                <h6 style='color: #004d00;'>{label}</h6>
                <h4 style='color: black;'>{value}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col1:
        styled_metric("Total Hours", f"{total_hours:.2f}")
    with col2:
        styled_metric("Total Utterances", total_utterances)
    with col3:
        styled_metric("Vocabulary Size", vocab_size)
    with col4:
        styled_metric("Alphabet Size", alphabet_size)

    # alphabet
    st.markdown("### **Alphabet in the Dataset**")
    st.write("   ".join(alphabet))

    # Histograms using Altair
    st.markdown("### **Data Distribution**")
    col1, col2, col3 = st.columns(3)

    with col1:
        chart1 = alt.Chart(df).mark_bar(color="#FF8080").encode(
            alt.X("duration:Q", bin=True, title="Duration (s)"),
            alt.Y("count()", title="Frequency")
        ).properties(title="Duration per File", width=250, height=250)
        st.altair_chart(chart1)

    with col2:
        chart2 = alt.Chart(df).mark_bar(color="#808080").encode(
            alt.X("word_count:Q", bin=True, title="Words per File"),
            alt.Y("count()", title="Frequency")
        ).properties(title="Words per File", width=250, height=250)
        st.altair_chart(chart2)

    with col3:
        chart3 = alt.Chart(df).mark_bar(color="#FE7B00").encode(
            alt.X("char_count:Q", bin=True, title="Characters per File"),
            alt.Y("count()", title="Frequency")
        ).properties(title="Characters per File", width=250, height=250)
        st.altair_chart(chart3)

    # Donut Charts using Plotly 
    st.markdown("### **Observation**")
    col1, col2 = st.columns(2)

    with col1:
        vocab_chart = px.pie(
            values=[vocab_size, alphabet_size],
            names=["Unique Words", "Unique Characters"],
            hole=0.5,
            color_discrete_sequence=["#FF8080", "#808080"]
        )
        vocab_chart.update_layout(title="Vocabulary vs Alphabet Size")
        st.plotly_chart(vocab_chart)

    with col2:
        duration_chart = px.pie(
            values=[total_hours, total_utterances],
            names=["Total Hours", "Total Utterances"],
            hole=0.5,
            color_discrete_sequence=["#FE7B00", "#60A0FF"]
        )
        duration_chart.update_layout(title="Total Hours vs Utterances")
        st.plotly_chart(duration_chart)

# Run with: `streamlit run dashboard.py`
