import pandas as pd
import chromadb
import uuid
import csv


class Portfolio:

    # Constructor
    def __init__(self, path) -> None:
        self.path = path
        self.data = self.read_csv_file(self.path)
        # Chromadb Setup
        self.chroma_client = chromadb.PersistentClient('vectorstorealt')
        self.collection = self.chroma_client.get_or_create_collection(name= "portfolio")


    # This function reads and formats the data in portfolio so that the LLM can understand
    def read_csv_file(self, path):
        current = []
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for line in csv_reader:
                # Formatting data
                skills = tuple(line[:-1])
                link = line[-1]
                current.append((skills, link))
            return current
    

    # This function inserts data into Vector Database
    def load_portfolio(self):
        if not self.collection.count():
            for skills, links in self.data:
                self.collection.add(
                    documents= str(skills),
                    metadatas= {'portfolio_url': links},
                    ids= [str(uuid.uuid4())]
                )

    
    def query_links(self, skills):
        return self.collection.query(query_texts= skills, n_results= 2).get("metadatas", [])
