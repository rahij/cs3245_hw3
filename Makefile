index: index.py
	rm -rf dict_dir
	python index.py -i /Users/rahij/nltk_data/corpora/reuters/training/ -d dictionary.txt -p postings.txt
search: search.py
	rm results.txt
	python -m cProfile -o ~/bm.profile search.py -d dictionary.txt -p postings.txt -q queries/queries_perf6_braces.txt -o results.txt