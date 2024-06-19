# TF-IDF Search Engine

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Functions](#functions)
- [Special Cases and Incorrect Input](#special-cases-and-incorrect-input)
- [Contributions](#contributions)

## Project Description

This project implements a TF-IDF (Term Frequency-Inverse Document Frequency) based search engine. It processes a collection of documents, calculates TF-IDF scores, and enables querying to find the most relevant document based on a given query. The project is implemented in Python and uses the NLTK library for text preprocessing.

## Features

- **Document Preprocessing**: Tokenization, stemming, and stop-word removal.
- **TF-IDF Calculation**: Computes TF-IDF scores for terms in each document.
- **Query Processing**: Processes user queries to find and rank relevant documents.
- **Handles Special Cases**: Gracefully handles missing files and incorrect inputs.

## Requirements

- Python 3.7 or higher
- NLTK library

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-repo/tfidf-search-engine.git
   cd tfidf-search-engine
   ```

2. **Install required packages**:
   ```sh
   pip install nltk
   ```

3. **Download NLTK data files**:
   Uncomment and run the following lines in the script:
   ```python
   #nltk.download()
   ```

4. **Prepare the corpus**:
   Place your text files in a directory named `US_Inaugural_Addresses`.

## Running the Application

1. **Execute the script**:
   ```sh
   python tfidf_search.py
   ```

## Usage

### Functions

1. **`preProcessDocuments`**: Preprocesses the documents in the corpus.
2. **`getidf`**: Calculates the inverse document frequency for each term.
3. **`tfidf`**: Calculates the TF-IDF score for each term in each document.
4. **`get_weight`**: Retrieves the TF-IDF weight for a specific term in a specific document.
5. **`get_idf`**: Retrieves the IDF value for a specific term.
6. **`query`**: Processes a query to find the most relevant document based on TF-IDF scores.
7. **`get_weight_q`**: Retrieves the weight of a term in the query.

### Example Usage

```python
search = TFIDFSearch("./US_Inaugural_Addresses") # change according to your folder
search.preProcessDocuments()
search.getidf()
search.tfidf()

print("%.12f" % search.get_idf('children'))
print("%.12f" % search.get_idf('foreign'))
print("%.12f" % search.get_idf('people'))
print("%.12f" % search.get_idf('honor'))
print("%.12f" % search.get_idf('great'))
print("--------------")
print("%.12f" % search.get_weight('19_lincoln_1861.txt', 'constitution'))
print("%.12f" % search.get_weight('23_hayes_1877.txt', 'public'))
print("%.12f" % search.get_weight('25_cleveland_1885.txt', 'citizen'))
print("%.12f" % search.get_weight('09_monroe_1821.txt', 'revenue'))
print("%.12f" % search.get_weight('05_jefferson_1805.txt', 'press'))
print("--------------")
print("(%s, %.12f)" % search.query("pleasing people"))
print("(%s, %.12f)" % search.query("war offenses"))
print("(%s, %.12f)" % search.query("british war"))
print("(%s, %.12f)" % search.query("texas government"))
print("(%s, %.12f)" % search.query("cuba government"))
print("--------------")
print("\n\nSpecial Cases, Incorrect input\n\n")
print("%.12f" % search.get_idf('AT&T'))
print("%.12f" % search.get_weight('007_JJ.txt', 'UTA'))
print("%.12f" % search.get_weight('05_jefferson_1805.txt', 'AT&T'))
print("(%s, %.12f)" % search.query("arlington texas"))
```

### Special Cases and Incorrect Input

The script includes handling for special cases and incorrect inputs. For example:
- Non-existent files are handled gracefully with error messages.
- Terms not found in the documents return a TF-IDF weight of -1.
- Incorrect or malformed input tokens are handled without causing crashes.

## Contributions

Contributions are welcome! Please create an issue or submit a pull request with your changes.
