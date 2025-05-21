Boolean Information Retrieval System
Overview
This project implements a Boolean Information Retrieval Model for a collection of computer science journal abstracts. It focuses on building:

Inverted Index: Maps terms to the documents containing them.

Positional Index: Tracks term positions within documents to support proximity queries.

The system supports Boolean queries with up to three terms connected by AND, OR, and NOT operators, and proximity queries to find documents where two terms appear within k words of each other.

Assignment Objective
Understand how inverted and positional indexes work in retrieving documents.

Implement preprocessing: tokenization, case folding, stop-word removal, and stemming.

Build efficient Boolean and proximity query processors.

Provide a user interface to demonstrate query execution.

Evaluate results against a provided gold standard.

Dataset
Abstracts.zip: Contains 448 abstracts in English (each file is a unique document).

Stopword-List.txt: List of stop words to filter during preprocessing.

Gold Standard: A set of 10 queries to evaluate correctness.

Features
Preprocessing pipeline with tokenization, stop words removal, and Porter stemming.

Construction and saving/loading of both inverted and positional indexes.

Query parser and executor for:

Boolean queries (AND, OR, NOT)

Proximity queries (e.g., "word1 word2 /k" for terms within k words).

Simple and intuitive GUI built with customtkinter to enter queries and display results.

Measures and displays query execution time.

Requirements
Python 3.7+

Packages:

nltk (for tokenization and stemming)

customtkinter (for GUI)

Pillow (for image handling)

chardet (for encoding detection)

Install dependencies via:

pip install nltk customtkinter pillow chardet

Make sure to download the NLTK tokenizer models:

import nltk
nltk.download('punkt')

Usage Instructions

Prepare your data:

Extract Abstracts.zip to a folder.

Place Stopword-List.txt in the same directory as the script.

Ensure background images (Artboard 2.png and SEO analytics team-amico (2).png) are available in the working directory for the GUI.

Run the script:

python birs.py


The program preprocesses the documents and builds indexes, then saves them for future use.

Using the GUI:

Enter a Boolean Query using up to three terms with AND, OR, and NOT (e.g., machine AND learning NOT neural).

Or enter a Proximity Query in the format "word1 word2 /k" (e.g., data science /3).

Click the corresponding Search button.

Results show the list of document IDs matching the query and the query execution time.

Code Structure
Preprocessing: Tokenizes text, applies stemming and stop-word removal.

Indexing: Builds inverted and positional indexes from preprocessed documents.

Query Processing:

boolean_query(): Evaluates Boolean expressions over the inverted index.

proximity_query(): Checks word proximity using the positional index.

GUI: Built with customtkinter and tkinter.Canvas to provide a user-friendly interface.


Notes
The system treats documents uniquely by filename (document ID).

Stop-words and stemming ensure better indexing and query matching.

Proximity queries require correct formatting: two terms followed by /k where k is an integer.

The code supports case folding and simple tokenization but does not handle phrases longer than two words for proximity queries.

