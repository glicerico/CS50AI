import math
import os
import string
import sys

import nltk
from nltk import word_tokenize
import numpy as np

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    corpus = dict()
    cwd = os.getcwd()
    dir_path = os.path.join(cwd, directory)
    if os.path.isdir(dir_path):  # Confirm directory
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            with open(file_path, 'r') as fi:
                corpus[file] = fi.read()

    return corpus


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    filter_words = nltk.corpus.stopwords.words("english")
    filter_words.extend(string.punctuation)
    tokenized = word_tokenize(document.lower())
    tokenized_filtered = [word for word in tokenized if word not in filter_words]

    return tokenized_filtered


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()

    # Get unique vocabulary
    unique = []
    for vocab in documents.values():
        unique.extend(set(vocab))
    unique = set(unique)

    # calculate idf's'
    num_docs = len(documents)
    for word in unique:
        doc_count = 0
        for vocab in documents.values():
            if word in vocab:
                doc_count += 1
        idfs[word] = math.log(num_docs / doc_count)

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Calculate tf-idf values
    tf_idfs = []
    for vocab in files.values():
        current_calc = []
        for word in query:
            occurrences = vocab.count(word)
            current_calc.append(occurrences * idfs.get(word, 0))
        tf_idfs.append(sum(current_calc))

    indexes = np.argsort(tf_idfs)
    indexes = indexes[::-1]
    name_list = list(files.keys())  # Get file names
    ordered_names = [name_list[index] for index in indexes]  # Sort filenames
    return ordered_names[:n]  # Only return first n values


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Calculate matching word measures and query term densities
    value_list = []
    for id, tokens in enumerate(sentences.values()):
        mwm = 0
        words_match = 0
        sent_len = len(tokens)
        for word in query:
            if word in tokens:
                mwm += idfs[word]
                words_match += 1 / sent_len  # Track number of matched words
        value_list.append((mwm, words_match, id))  # Use sort's tuple ordering to break ties

    sorted_list = sorted(value_list)
    sorted_list = sorted_list[::-1]
    sentence_list = list(sentences.keys())  # Get sentences
    ordered_sentences = [sentence_list[index[2]] for index in sorted_list]  # Sort sentences
    return ordered_sentences[:n]  # Only return first n values


if __name__ == "__main__":
    main()
