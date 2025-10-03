from langchain_community.document_loaders import WebBaseLoader
import bs4
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_community.vectorstores import Chroma
from langchain_experimental.text_splitter import SemanticChunker



def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)



# Fase 1: Indexing

webPage = 'https://lilianweng.github.io/posts/2023-06-23-agent/'

loader = WebBaseLoader(
    web_path = webPage,
    bs_kwargs = dict(
        parse_only = bs4.SoupStrainer(
            class_ = ('post-title', 'post-header', 'post-content')
        )
    ),
)

docs = loader.load()

embeddings = OllamaEmbeddings(model='nomic-embed-text')
text_splitter = SemanticChunker(embeddings)
splits = text_splitter.split_documents(docs)

vector_store = Chroma.from_documents(
    documents = splits,
    embedding = OllamaEmbeddings(model='nomic-embed-text')
)



# Fase 2: Retriever y Generation

retriever = vector_store.as_retriever()

rag_prompt = hub.pull('jclemens24/rag-prompt')

llm = ChatOllama(model='qwen3:8b', temperature=0)

rag_chain_from_docs = (
    RunnablePassthrough.assign(context=(
        lambda x: format_docs(x['context'])
    ))
        | rag_prompt
        | llm
        | StrOutputParser()
)

rag_chain_with_source = RunnableParallel(
    {'context': retriever,
    'question': RunnablePassthrough()}
).assign(answer=rag_chain_from_docs)

response = rag_chain_with_source.invoke('What are the advantajes of using RAG?')

print(response)