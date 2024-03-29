#!/usr/bin/python
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import sys
import getopt
import math
import os.path
import shutil

TOKEN_FILES_DIR='dict_dir/'
DOC_WEIGHTS_FILE = 'doc_weights.txt'
NUM_FILES_TO_INDEX = -1
LOG_BASE = 10

def create_dict_dir():
  """
  Creates a directory(TOKEN_FILES_DIR) to store files with name as token and content as doc_ids.
  """
  if not os.path.exists(TOKEN_FILES_DIR):
    os.makedirs(TOKEN_FILES_DIR)

def stem_and_normalize_tokens(token_list):
  """
  Stems and normalizes tokens, gets rid of slashes to not interfere with file names
  """
  stemmer = nltk.stem.porter.PorterStemmer()
  normalized_list = []
  for i in xrange(len(token_list)):
    token = stemmer.stem(token_list[i])
    if "/" in token:
      for t in token.split('/'):
        normalized_list.append(t)
    else:
      normalized_list.append(token)
  return [x for x in normalized_list if x]

def get_tokens_from_line(line):
  """
  Converts a line into tokens by sent_tokenize, word_tokenize, case folding and normalizing special characters
  """
  token_list = map(lambda x: x.lower(),filter(lambda word: word not in ',-...:!$&()\"\'', [word for sent in sent_tokenize(line) for word in word_tokenize(sent)]))
  token_list = stem_and_normalize_tokens(token_list)
  return token_list

def create_term_freq(l):
  """
  Splits a comma separated doc_id, term frequency pair and stores it in a dictionary to compute doc_weights.
  """
  l = l.split()
  tf = {}
  for term in l:
    doc_id, freq = term.split(',')
    tf[doc_id] = int(freq)
  return tf

def write_doc_id_to_file(token, doc_id):
  """
  Appends doc_id to file with name as the token inside TOKEN_FILES_DIR
  """
  token_file_path=TOKEN_FILES_DIR + token
  if not os.path.isfile(token_file_path):
    dict_token_writer = open(token_file_path, "w")
    dict_token_writer.write(doc_id + ",1")
  else:
    dict_token_reader = open(token_file_path, "r")
    tf = create_term_freq(dict_token_reader.readline())
    if doc_id not in tf:
      dict_token_writer = open(token_file_path, "a")
      dict_token_writer.write(" " + doc_id + ",1")
    else:
      dict_token_writer = open(token_file_path, "w")
      tf[doc_id] += 1
      to_write = ''
      doc_ids = tf.keys()
      doc_ids.sort(key=int)
      for doc_key in doc_ids:
        to_write += doc_key+','+str(tf[doc_key])+' '
      dict_token_writer.write(to_write)


def get_list_of_files_to_index():
  """
  Gets list of files to be indexed in order
  """
  file_list = os.listdir(documents_dir)
  file_list.sort(key=int)
  global total_files
  total_files = len(file_list)
  if NUM_FILES_TO_INDEX == -1:
    return file_list
  else:
    return file_list[0:NUM_FILES_TO_INDEX]

def get_list_of_token_files():
  """
  Returns list of files in TOKEN_FILES_DIR
  """
  file_list = os.listdir(TOKEN_FILES_DIR)
  return file_list

def split_string_to_doc_ids(l):
  """
  Splits the comma separated string of doc_ids into tokens.
  """
  l = l.split()
  num_docs = len(l)
  return ' '.join(l), num_docs

def compute_doc_weights(token, doc_ids, idf):
  """
  Calculates the weight of each doc_id and stores in a dictionary.
  This is done by incrementing the dictionary of index doc_id if it is already present
  or initialized to 0.
  """
  doc_ids = doc_ids.split()
  for term in doc_ids:
    doc_id, tf = term.split(',')
    if doc_id not in doc_weights:
      doc_weights[doc_id] = 0
    doc_weights[doc_id] += math.pow(idf * float(tf), 2)

def append_all_files_to_dict():
  """
  Gets all files from TOKEN_FILES_DIR and writes it to dictionary and postings files. It then deletes TOKEN_FILES_DIR
  """
  dict_file_writer = open(dict_file, "w")
  postings_file_writer = open(postings_file, "w")
  postings_file_writer.write(" ".join(get_list_of_files_to_index()) + "\n")
  token_file_list = get_list_of_token_files()
  for token_file_name in token_file_list:
    in_file = TOKEN_FILES_DIR + token_file_name
    with open(in_file) as f:
      file_pointer = postings_file_writer.tell()
      doc_ids, num_docs = split_string_to_doc_ids(f.readline())
      postings_file_writer.write(doc_ids + "\n")
      idf = math.log(float(total_files)/num_docs, LOG_BASE)
      dict_file_writer.write(token_file_name + " " + str(idf) + " " + str(file_pointer) + "\n")
      compute_doc_weights(token_file_name, doc_ids, idf)
  shutil.rmtree(TOKEN_FILES_DIR)

def write_doc_weights_to_file():
  """
  Writes the dictionary with weights of each doc_id to a file.
  """
  for doc_id in doc_weights:
    weight = math.pow(doc_weights[doc_id], 0.5)
    if os.path.isfile(DOC_WEIGHTS_FILE):
      doc_file_writer = open(DOC_WEIGHTS_FILE, "a")
      doc_file_writer.write('\n' + doc_id + " " + str(weight))
    else:
      doc_file_writer = open(DOC_WEIGHTS_FILE, "w")
      doc_file_writer.write(doc_id + " " + str(weight))

def index_docs(documents_dir, dict_file, postings_file):
  create_dict_dir()
  indexer = {}
  file_list = get_list_of_files_to_index()
  for file_name in file_list:
    print file_name
    in_file = documents_dir + file_name
    with open(in_file) as f:
      for l in f.readlines():
        token_list = get_tokens_from_line(l)
        for token in token_list:
          write_doc_id_to_file(token, file_name)

  append_all_files_to_dict()
  write_doc_weights_to_file()

def usage():
  print "usage: " + sys.argv[0] + " -i training-doc-directory -d out-file-for-dictionary -p output-file-for-postings-list"

documents_dir = dict_file = postings_file = None
try:
  opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
  usage()
  sys.exit(2)
for o, a in opts:
  if o == '-i':
    documents_dir = a
  elif o == '-d':
    dict_file = a
  elif o == '-p':
    postings_file = a
  else:
    assert False, "unhandled option"
if documents_dir == None or dict_file == None or postings_file == None:
  usage()
  sys.exit(2)

total_files = 0
doc_weights = {}
index_docs(documents_dir, dict_file, postings_file)