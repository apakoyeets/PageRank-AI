# PageRank Algorithm Implementation

This project implements the **PageRank algorithm**, a foundational algorithm originally developed by Google to rank web pages by their importance based on the structure of links between pages.

---

## 🚀 Project Overview

The goal is to write an AI that can compute the importance of web pages in a given corpus using two approaches:

- **Sampling (Random Surfer Model):** Simulate a random surfer clicking links, using a damping factor to occasionally jump to any page at random.
- **Iterative Calculation:** Repeatedly apply the PageRank formula until the page ranks converge to stable values.

The program reads a corpus of web pages (HTML files with links), builds a graph of the linking structure, and outputs the PageRank of each page.

---

## 📖 Background

- A page is considered important if many other important pages link to it.
- The **random surfer model** imagines a person randomly clicking links with probability *d* (damping factor, usually 0.85), and randomly jumping to any page with probability *(1 - d)*.
- The algorithm is modeled as a Markov Chain, and the PageRank value for each page corresponds to the steady-state probability of the surfer visiting that page.
- This project implements both the **sampling** method and the **iterative formula** method for calculating PageRank.

---

## 🛠 Features

- Parse a corpus of HTML pages and build a graph of links.
- Compute transition probabilities for the random surfer.
- Estimate PageRank by simulating many random samples.
- Compute PageRank iteratively until convergence.
- Handles pages with no outbound links by treating them as linking to all pages.

