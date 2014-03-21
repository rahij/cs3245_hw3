Matric number: A0091539X
Email: a0091539@nus.edu.sg

Index:

This is started with my HW2 as the base. During indexing, the inverse document frequencies are pre computed for each term and written to the dictionary bu using a bunch of temporary files which are erased at the end of the process. After that, for each term in the postings list, the term frequencies are also computed and written to a file 'doc_weights.txt' which is basically a list of documents and their 'weights' used to normalize the vectors during search.

Search:
Each query is split into tokens and stemmed using porter stemmer. Then the standard cosine normalization procedure is done as described in the lecture slides of w7. During processing each token, the query weight is automatically incremented by the tf. At the end of all terms in the query, each score is divided by both the query weight and the doc_id's weight which was pre computed and stored in doc_weights.txt. The top 10 are then written to a file.

Sources:
1. This was started with HW2 code that I had submitted with another student. This time, I am doing it alone, so some of the code was written by my teammate last time (very insignifant since he wrote most of the search and that had been almost rewritten for this assignment)

2. http://www.slideshare.net/hellangel13/cosine-tf-idfexample

3. StackOverflow