index: index.py
	@rm -rf dict_dir 2>/dev/null || true
	@rm -rf doc_weights.txt 2>/dev/null || true
	python index.py -i /Users/rahij/nltk_data/corpora/reuters/training/ -d dictionary.txt -p postings.txt
	# python index.py -i test_sample/ -d dictionary.txt -p postings.txt
search: search.py
	@rm results.txt 2>/dev/null || true
	python -m cProfile -o ~/bm.profile search.py -d dictionary.txt -p postings.txt -q query_file -o results.txt