from tinydb import TinyDB, Query

db = TinyDB('db.json')
query = Query()
def add_context(content,namespace):
    #here goes pinecone upserting to this namespace
    # print(content)
    db.insert({'namespace':namespace})

def remove_context(namespace):
    #here goes pinecone namespace removal
    db.remove(query.namespace ==namespace)

def get_all_context():
    entries = db.all()
    namespaces = [value for entry in entries for value in entry.values()]
    return namespaces

def remove_all_context():
    db.remove(Query().namespace.exists())
