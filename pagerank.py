import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    # Ensure the user specifies a corpus folder
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    # Load the corpus
    corpus = crawl(sys.argv[1])

    # Calculate ranks using sampling
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    # Calculate ranks using iteration
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
    probability_distribution = {}
    links = corpus[page]
    n_pages = len(corpus)

    if links:
        for linked_page in corpus:
            probability_distribution[linked_page] = (1 - damping_factor) / n_pages
        for linked_page in links:
            probability_distribution[linked_page] += damping_factor / len(links)
    else:
        for linked_page in corpus:
            probability_distribution[linked_page] = 1 / n_pages

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        page_rank[current_page] += 1
        model = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            population=list(model.keys()),
            weights=list(model.values()),
            k=1
        )[0]

    total = sum(page_rank.values())
    for page in page_rank:
        page_rank[page] /= total

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n_pages = len(corpus)
    page_rank = {page: 1 / n_pages for page in corpus}
    new_rank = page_rank.copy()

    convergence = False
    while not convergence:
        convergence = True
        for page in corpus:
            total = 0
            for possible_page in corpus:
                if page in corpus[possible_page]:
                    total += page_rank[possible_page] / len(corpus[possible_page])
                elif not corpus[possible_page]:
                    total += page_rank[possible_page] / n_pages

            new_rank[page] = (1 - damping_factor) / n_pages + damping_factor * total

        for page in page_rank:
            if abs(new_rank[page] - page_rank[page]) > 0.001:
                convergence = False

        page_rank = new_rank.copy()

    return page_rank


if __name__ == "__main__":
    main()
