import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    damping_prob = 1 / len(corpus)
    if len(corpus[page]) == 0:  # If page has no links, all pages have equal prob
        distribution = {ipage: damping_prob for ipage in corpus}
    else:
        linked_prob = 1 / len(corpus[page])
        distribution = {ipage: damping_prob * (1 - damping_factor) for ipage in corpus}
        for ipage in corpus[page]:  # Add links probabilities
            distribution[ipage] += damping_factor * linked_prob


    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {ipage: 0 for ipage in corpus}  # Initialize counter for each page
    curr_page = random.sample(corpus.keys(), 1)[0]  # Initial page

    pages = sorted(list(corpus.keys()))  # Get ordered list of keys

    for _ in range(n):
        distribution = transition_model(corpus, curr_page, damping_factor)
        weights = [distribution[page] for page in pages]  # Get ordered list of weights
        curr_page = random.choices(population=pages, weights=weights)[0]
        pagerank[curr_page] += 1 / n  # Normalize continuously

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    convergence = 0.0001
    n = len(corpus)

    # Handle pages with no links
    for page, links in corpus.items():
        if len(links) == 0:
            corpus[page] = list(corpus.keys())

    pagerank = {page: 1 / n for page in corpus}  # Initialize scores
    refs = get_references(corpus)

    scores = np.array(list(pagerank.values()))
    while True:
        for page in corpus:
            this_sum = 0
            for ref in refs[page]:
                this_sum += pagerank[ref] / len(corpus[ref])
            pagerank[page] = (1 - damping_factor) / n + damping_factor * this_sum

        new_scores = np.array(list(pagerank.values()))
        if (abs((scores - new_scores)/scores) < convergence).all():
            return pagerank
        else:
            scores = new_scores


def get_references(corpus):
    """
    Return dictionary with pages that link to a given page
    """
    refs = {page: [] for page in corpus}
    for page, links in corpus.items():
        for link in links:
            refs[link].append(page)

    return refs


if __name__ == "__main__":
    main()
