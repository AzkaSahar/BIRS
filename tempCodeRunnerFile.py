import os
import json
import chardet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import customtkinter as ctk
from tkinter import filedialog, messagebox, Canvas
from PIL import Image, ImageTk
import time


# ------------------- Preprocessing & Indexing Functions ------------------- #

# Function to preprocess text
def preprocess_text(text, stopwords):
    text = text.replace("-", " ").replace("/", " ")
    ps = PorterStemmer()
    tokens = word_tokenize(text.lower())
    return [ps.stem(word) for word in tokens if word.isalnum() and word not in stopwords]

# Load stopwords
def load_stopwords(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        return set(file.read().splitlines())

# Read & preprocess documents
def read_documents(folder_path, stopwords):
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as f:
                encoding = chardet.detect(f.read())['encoding'] or 'utf-8'
            with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                words = preprocess_text(file.read(), stopwords)
                documents[filename.split(".")[0]] = words
    return documents

# Build Inverted & Positional Index
def build_inverted_index(documents):
    inverted_index = {}
    for doc_id, words in documents.items():
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = set()
            inverted_index[word].add(doc_id)

    return {word: sorted(docs, key=int) for word, docs in inverted_index.items()}

def build_positional_index(documents):
    positional_index = {}
    for doc_id, words in documents.items():
        for pos, word in enumerate(words):
            if word not in positional_index:
                positional_index[word] = set()
            positional_index[word].add(doc_id)

    return positional_index

# Save & Load Indexes
def save_indexes(inverted_index, positional_index, filename="indexes.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({"inverted_index": inverted_index, "positional_index": positional_index}, f, indent=4)

def load_indexes(filename="indexes.json"):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["inverted_index"], data["positional_index"]
    return None, None

# Boolean Query Processing

def boolean_query(query, inverted_index, stopwords):
    ps = PorterStemmer()
    terms = query.lower().split()
    processed_terms = [ps.stem(word) for word in terms if word.isalnum() and word not in stopwords]

    if not processed_terms:
        return set(), 0, 0.0  # No result, 0 count, 0 time

    result_set = set()
    operation = None

    start_time = time.perf_counter()  # Start time

    for word in processed_terms:
        if word.lower() in ["and", "or", "not"]:
            operation = word.lower()
        else:
            stemmed_word = ps.stem(word)
            doc_set = set(inverted_index.get(stemmed_word, set()))

            if operation is None:
                result_set = doc_set
            elif operation == "and":
                result_set &= doc_set
            elif operation == "or":
                result_set |= doc_set
            elif operation == "not":
                result_set = {doc for docs in inverted_index.values() for doc in docs} - doc_set


            operation = None  # Reset operation after use

    execution_time = time.perf_counter() - start_time  # End time
    result_count = len(result_set)  # Count the results

    return sorted(result_set, key=int), result_count, execution_time


# Proximity Query Processing
def proximity_query(query, positional_index, stopwords):
    ps = PorterStemmer()
    try:
        parts = query.rsplit("/", 1)
        if len(parts) != 2:
            raise ValueError("Invalid proximity query format. Use: word1 word2 /k")

        words_part, k = parts[0].strip(), int(parts[1].strip())
        word1, word2 = words_part.split()
        word1, word2 = ps.stem(word1.lower()), ps.stem(word2.lower())

        start_time = time.perf_counter()  # Start time

        docs = set(positional_index.get(word1, {}).keys()) & set(positional_index.get(word2, {}).keys())
        result_docs = set()

        for doc in docs:
            positions_word1 = positional_index[word1][doc]
            positions_word2 = positional_index[word2][doc]

            for p1 in positions_word1:
                for p2 in positions_word2:
                    if abs(p1 - p2) <= k:
                        result_docs.add(doc)
                        break  # Stop checking once one match is found

        execution_time = time.perf_counter() - start_time  # End time
        result_count = len(result_docs)  # Count the results

        return sorted(result_docs), result_count, execution_time

    except ValueError:
        return set(), 0, 0.0  # No result, 0 count, 0 time



# ------------------- Tkinter GUI with Canvas Background ------------------- #

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1000x660")
app.title("Boolean Information Retrieval System")

# Canvas for Background Image
canvas = Canvas(app, width=1000, height=660)
canvas.pack(fill="both", expand=True)

# Background Image
bg_image = Image.open("Artboard 2.png")
bg_image = bg_image.resize((1000, 660), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Side Image
seo_img = Image.open("SEO analytics team-amico (2).png")  # SEO Illustration
seo_img = ImageTk.PhotoImage(seo_img)

canvas.create_image(680, 50, image=seo_img, anchor="nw")  # Adjust position as needed

# Main heading 
canvas.create_text(250, 65, text="Boolean Information\nRetrieval System", 
                   font=("Quicksand", 30, "bold"), fill="#FFD700")


canvas.create_text(
    210, 160,
    text="Perform Boolean and Proximity\nQueries on indexed abstracts.",
    font=("Quicksand", 16),
    fill="white"
)




# Frames on Canvas
query_frame = ctk.CTkFrame(app,  fg_color="#FFD700")
query_frame.place(relx=0.4, rely=0.45, anchor="center")

results_frame = ctk.CTkFrame(app, fg_color="#FFD700", width=700, height=300)
results_frame.place(relx=0.4, rely=0.75, anchor="center")

# Labels

boolean_label = ctk.CTkLabel(query_frame, text="Boolean Query", font=("Quicksand", 16,"bold"), text_color="#545c54")
boolean_label.grid(row=0, column=0, padx=20, pady=5)

proximity_label = ctk.CTkLabel(query_frame, text="Proximity Query", font=("Quicksand", 16,"bold"), text_color="#545c54")
proximity_label.grid(row=0, column=1, padx=20, pady=5)


def clear_other_inputs(event):
    results_text.delete("1.0", "end")  # Clear results when switching queries

# Boolean Entry
boolean_entry = ctk.CTkEntry(query_frame, width=200, fg_color="white", text_color="#646464",
                             font=("Quicksand", 16), justify="center")
boolean_entry.grid(row=1, column=0, padx=20, pady=5)
boolean_entry.bind("<FocusIn>", clear_other_inputs)  # Bind focus event

# Proximity Entry
proximity_entry = ctk.CTkEntry(query_frame, width=200, fg_color="white", text_color="#646464",
                               font=("Quicksand", 16), justify="center")
proximity_entry.grid(row=1, column=1, padx=20, pady=5)
proximity_entry.bind("<FocusIn>", clear_other_inputs)  # Bind focus event

# Textbox for Results 
results_label = ctk.CTkLabel(results_frame, text="", font=("Quicksand", 14,"bold"), text_color="#646464")
results_label.pack()

results_text = ctk.CTkTextbox(
    results_frame, width=650, height=200, font=("Quicksand", 20, "bold"), 
    fg_color="white", text_color="#646464"
)
results_text.pack(padx=10, pady=(0, 10), fill="both", expand=True)



# Load Data
stopwords = load_stopwords("Stopword-List.txt")
inverted_index, positional_index = load_indexes()

if inverted_index is None or positional_index is None:
    folder = filedialog.askdirectory(title="Select Abstracts Folder")
    if folder:
        documents = read_documents(folder, stopwords)
        inverted_index = build_inverted_index(documents)
        positional_index = build_positional_index(documents)
        save_indexes(inverted_index, positional_index)
        messagebox.showinfo("Indexing", "Indexes built and saved successfully!")

# Printing 
def display_results(results, results_count, time_taken):
    time_display = f"{time_taken:.6f} sec" if time_taken >= 0.001 else f"{time_taken * 1_000_000:.2f} μs"
    results_label.configure(text=f"{results_count} results returned in {time_display}")
    formatted_results = "\n".join(f"• Document {doc}" for doc in results)
    results_text.insert("0.0", f"Matching Documents:\n{formatted_results}\n\n")



# Search Functions
def search_boolean():
    query = boolean_entry.get().strip()
    if query:
        results_text.delete("0.0", "end")
        results, results_count, time_taken = boolean_query(query, inverted_index, stopwords)


        display_results(results, results_count, time_taken)


    

def search_proximity():
    query = proximity_entry.get().strip()
    if query:
        results_text.delete("0.0", "end")
        results, results_count, time_taken = proximity_query(query, positional_index, stopwords)

        
        display_results(results, results_count, time_taken)



# Buttons
ctk.CTkButton(query_frame, text="Search Boolean", command=search_boolean, 
              fg_color="#535354", hover_color="#6b6b6c").grid(row=2, column=0, padx=20, pady=10)

ctk.CTkButton(query_frame, text="Search Proximity", command=search_proximity, 
              fg_color="#535354", hover_color="#6b6b6c").grid(row=2, column=1, padx=20, pady=10)


app.mainloop()
