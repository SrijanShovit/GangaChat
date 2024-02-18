from langchain.document_loaders import PyPDFLoader, DirectoryLoader, PDFMinerLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os
from constants import CHROMA_SETTINGS

persist_directory = "db"

def main():
    for root,dirs,files in os.walk("src_docs"):
        for file in files:
            if file.endswith(".pdf"):
                print(file)
                loader = PDFMinerLoader(os.path.join(root,file))
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024,chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    #create embeddings here
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    #create vector store here
    db = Chroma.from_documents(texts,embeddings,persist_directory=persist_directory,client_settings=CHROMA_SETTINGS)

    db.persist()
    db = None


if __name__ == "__main__":
    main()