import streamlit as st
import pandas as pd
import pdfplumber
from textblob import TextBlob
import re

st.set_page_config(page_title="Extracto", page_icon="📄", layout="wide")

st.title("📄🔍 Extracto")
st.caption("Upload documents. Ask questions. Get insights instantly.")

uploaded_file = st.file_uploader(
    "Upload PDF, CSV, or Excel file",
    type=["pdf", "csv", "xlsx"]
)

query = st.text_input("Enter your query")

def correct_query(user_query):
    try:
        return str(TextBlob(user_query).correct())
    except:
        return user_query

def detect_intent(user_query):
    q = user_query.lower()

    if any(word in q for word in ["summarize", "summary", "about", "overview", "explain"]):
        return "Summary"

    elif any(word in q for word in ["key points", "main points", "important points", "highlights"]):
        return "Key Points"

    elif any(word in q for word in ["how many", "count", "total"]):
        return "Count"

    elif any(word in q for word in ["top", "highest", "largest", "maximum"]):
        return "Sorting"

    elif any(word in q for word in ["above", "greater than", "more than"]):
        return "Filter"

    elif any(word in q for word in ["find", "search", "list", "show"]):
        return "Search"

    else:
        return "Summary"

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def simple_summary(text, limit=1200):
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r'(?<=[.!?]) +', text)

    if len(sentences) <= 5:
        return text[:limit]

    return " ".join(sentences[:6])[:limit]

def key_points(text):
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r'(?<=[.!?]) +', text)

    points = []
    for sentence in sentences:
        if len(sentence.split()) > 6:
            points.append(sentence)

    return points[:7]

def search_text(text, query):
    words = query.lower().split()
    useful_words = [w for w in words if w not in ["find", "search", "show", "list", "me", "the", "this", "pdf", "file", "document"]]

    if not useful_words:
        return "Please enter a specific word to search."

    keyword = useful_words[-1]

    lines = text.split("\n")
    matches = [line for line in lines if keyword.lower() in line.lower()]

    return matches[:10], keyword

def search_dataframe(df, query):
    words = query.lower().split()
    ignore = ["find", "search", "show", "list", "me", "the", "rows", "related", "to"]
    keywords = [w for w in words if w not in ignore]

    if not keywords:
        return pd.DataFrame()

    keyword = keywords[-1]

    result = df[
        df.astype(str).apply(
            lambda row: row.str.contains(keyword, case=False, na=False).any(),
            axis=1
        )
    ]
    return result

if uploaded_file and query:
    corrected_query = correct_query(query)
    intent = detect_intent(query)

    st.subheader("Structured Output")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**File Name:**", uploaded_file.name)
        st.write("**File Type:**", uploaded_file.type)
        st.write("**Original Query:**", query)

    with col2:
        st.write("**Corrected Query:**", corrected_query)
        st.write("**Detected Intent:**", intent)

    st.divider()

    if uploaded_file.name.endswith(".pdf"):
        text = read_pdf(uploaded_file)

        if not text.strip():
            st.error("No readable text found in this PDF.")
        else:
            if intent == "Summary":
                st.subheader("Document Summary")
                st.write(simple_summary(text))

            elif intent == "Key Points":
                st.subheader("Key Points")
                points = key_points(text)
                for i, point in enumerate(points, start=1):
                    st.write(f"{i}. {point}")

            elif intent == "Count":
                words = text.split()
                st.success(f"Total words in PDF: {len(words)}")

            elif intent == "Search":
                result, keyword = search_text(text, query)

                st.subheader(f"Search Results for: {keyword}")

                if isinstance(result, str):
                    st.warning(result)
                elif result:
                    for line in result:
                        st.write("- " + line)
                else:
                    st.warning("No matching text found.")

            else:
                st.subheader("Document Preview")
                st.write(text[:1500])

    elif uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

        st.subheader("Uploaded Data")
        st.dataframe(df)

        if intent == "Summary":
            st.subheader("Dataset Summary")
            st.write(f"This file contains **{len(df)} rows** and **{len(df.columns)} columns**.")
            st.write("Columns:", ", ".join(df.columns))

        elif intent == "Count":
            st.success(f"Total rows: {len(df)}")

        elif intent == "Search":
            result = search_dataframe(df, query)
            st.subheader("Search Result")
            if not result.empty:
                st.dataframe(result)
            else:
                st.warning("No matching rows found.")

        elif intent == "Sorting":
            numeric_columns = df.select_dtypes(include="number").columns
            if len(numeric_columns) > 0:
                column = numeric_columns[0]
                result = df.sort_values(by=column, ascending=False).head(5)
                st.subheader(f"Top 5 records based on {column}")
                st.dataframe(result)
            else:
                st.warning("No numeric column found for sorting.")

    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

        st.subheader("Uploaded Data")
        st.dataframe(df)

        if intent == "Summary":
            st.subheader("Dataset Summary")
            st.write(f"This file contains **{len(df)} rows** and **{len(df.columns)} columns**.")
            st.write("Columns:", ", ".join(df.columns))

        elif intent == "Count":
            st.success(f"Total rows: {len(df)}")

        elif intent == "Search":
            result = search_dataframe(df, query)
            st.subheader("Search Result")
            if not result.empty:
                st.dataframe(result)
            else:
                st.warning("No matching rows found.")

        elif intent == "Sorting":
            numeric_columns = df.select_dtypes(include="number").columns
            if len(numeric_columns) > 0:
                column = numeric_columns[0]
                result = df.sort_values(by=column, ascending=False).head(5)
                st.subheader(f"Top 5 records based on {column}")
                st.dataframe(result)
            else:
                st.warning("No numeric column found for sorting.")

else:
    st.info("Upload a file and enter a query to start using Extracto.")