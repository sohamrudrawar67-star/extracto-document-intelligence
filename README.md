🔍 Extracto
AI-Powered Document Intelligence System

Extracto is a Document Intelligence System that enables users to upload PDF, CSV, and Excel files and interact with them using natural language queries. The system processes uploaded documents, understands user intent, and returns meaningful insights such as summaries, key points, search results, and statistical information.

Problem Statement

Organizations deal with large volumes of documents and datasets every day. Extracto simplifies document analysis by allowing users to ask questions in plain English and receive relevant information without manually reading the entire file.

Features
Upload PDF, CSV, and Excel files
Natural language query processing
Query correction using TextBlob
Intent detection
Document summarization
Key point extraction
Keyword search
Word and row counting
Structured output display
Tech Stack
Frontend
Streamlit
Backend
Python
Libraries
Pandas
PyMuPDF / PDFPlumber
TextBlob
OpenPyXL
Project Structure
Extracto/
│
├── app.py
├── requirements.txt
├── README.md
├── sample_files/
└── screenshots/
Installation
Clone the repository
git clone <repository-link>
Navigate to project directory
cd extracto-document-intelligence
Install dependencies
pip install -r requirements.txt
Run the application
python3 -m streamlit run app.py
Sample Queries
Summarize this document
What is this file about?
Give me key points
Count words
Search for World War
Show top 5 records
Count rows
Sample Output
Query
Summarize this document
Output

The system generates a concise summary of the uploaded document.

Query
Give me key points
Output

The system extracts important points and presents them in a readable format.

Future Improvements
OCR support for scanned PDFs
Advanced NLP-based summarization
More file format support
Better query understanding
Interactive visualizations
AI-powered recommendations
Limitations
Works best with text-based PDFs
Limited support for scanned/image PDFs
Rule-based intent detection
Basic summarization approach
Author

Soham Rudrawar

Second-Year AI & Data Science Student

MIT World Peace University, Pune