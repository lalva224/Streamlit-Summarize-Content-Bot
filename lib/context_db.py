from tinydb import TinyDB, Query
from lib.pinecone import upsert_context_pinecone, remove_context_pinecone
db = TinyDB('db.json')
query = Query()

def add_context(content,namespace):
    #here goes pinecone upserting to this namespace
    upsert_context_pinecone(content,namespace)
    db.insert({'namespace':namespace})

def remove_context(namespace):
    #here goes pinecone namespace removal
    remove_context_pinecone(namespace)
    db.remove(query.namespace ==namespace)

def get_all_context():
    entries = db.all()
    namespaces = [value for entry in entries for value in entry.values()]
    return namespaces

def remove_all_context():
    db.remove(Query().namespace.exists())
