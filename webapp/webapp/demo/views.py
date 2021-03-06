from django.shortcuts import render
from medcat.cat import CAT
from medcat.cdb import CDB
from medcat.utils.helpers import doc2html
from medcat.utils.vocab import Vocab
from urllib.request import urlretrieve
from .models import *
import os

vocab_path = os.getenv('VOCAB_PATH', '/tmp/vocab.dat')
cdb_path = os.getenv('CDB_PATH', '/tmp/cdb.dat')

try:
    if not os.path.exists(vocab_path):
        vocab_url = os.getenv('VOCAB_URL')
        urlretrieve(vocab_url, vocab_path)

    if not os.path.exists(cdb_path):
        cdb_url = os.getenv('CDB_URL')
        print("*"*399)
        print(cdb_url)
        urlretrieve(cdb_url, cdb_path)

    vocab = Vocab()
    vocab.load_dict(vocab_path)
    cdb = CDB()
    cdb.load_dict(cdb_path)
    cat = CAT(cdb=cdb, vocab=vocab)
except Exception as e:
    print(str(e))

def get_html_and_json(text):
    doc = cat(text)
    doc_json = cat.get_json(text)

    uploaded_text = UploadedText()
    uploaded_text.text = str(text)
    uploaded_text.save()

    return doc2html(doc), doc_json


def train_annotations(request):
    context = {}

    if request.POST and 'text' in request.POST:
        doc_html, doc_json = get_html_and_json(request.POST['text'])

        context['doc_html'] = doc_html
        context['doc_json'] = doc_json
        context['text'] = request.POST['text']
    return render(request, 'train_annotations.html', context=context)
