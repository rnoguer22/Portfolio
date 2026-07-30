from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document 
from langchain_core.output_parsers import StrOutputParser 
from langchain_community.retrievers import BM25Retriever
import chromadb
from langchain_chroma import Chroma 
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate





# En una busqueda densa se usan vectores que buscan por significado y contexto los chunks que contienen la informacion
# Ventaja: Relaciona conceptos equivalentes y sinonimos aunque no sea la misma palabra (vehiculo - coche)
def dense_search(query, k=10, dense_weight=0.5):
    dense_docs = dense_retriever.invoke(query)[:k]
    dense_docs_ids = [doc.metadata['id'] for doc in dense_docs]
    print('Dense IDs: ', dense_docs_ids)
    return dense_docs


# La busqueda dispersa busca coincidencias exactas con las palabras clave de la query (eliminando articulos, preposiciones, etc.)
# Ventaja: Muy util para nombre propios, codigos, siglas, aspectos tecnicos, etc.
def sparse_search(query, k=10, sparse_weight=0.5):
    sparse_docs = sparse_retriever.invoke(query)[:k]
    sparse_docs_ids = [doc.metadata['id'] for doc in sparse_docs]
    print('Sparse IDs: ', sparse_docs_ids)
    return sparse_docs


# La busqueda hibrida combina ambas busquedas (densa y dispersa) aplicando RRF (Reciprocal Rank Fusion) para combinar los resultados
# (se usa RRF para saber cual es mas importante, ya que el 4 denso puede ser mas importante que el 1 disperso)
# Elimina chunks duplicados y los reordena dandoles una puntuacion en funcion de su importancia 
def hybrid_search(query, k=10, dense_weight=0.5, sparse_weight=0.5):
    # Devolvemos los top-k documentos mas importantes de la busqueda
    dense_docs = dense_retriever.invoke(query)[:k]
    dense_docs_ids = [doc.metadata['id'] for doc in dense_docs]
    print('\nCompare IDs:')
    print('dense IDs: ', dense_docs_ids)

    # Hacemos los mismo pero con sparse_retriever
    sparse_docs = sparse_retriever.invoke(query)[:k]
    sparse_docs_ids = [doc.metadata['id'] for doc in sparse_docs]
    print('sparse IDs: ', sparse_docs_ids)

    # Combinamos ambos 
    all_doc_ids = list(set(dense_docs_ids + sparse_docs_ids))
    # Inicializamos el ranking en 0 
    dense_reciprocal_ranks = {
        doc_id: 0.0 for doc_id in all_doc_ids
    }
    sparse_reciprocal_ranks = {
        doc_id: 0.0 for doc_id in all_doc_ids
    }
    # Calculamos el ranking de cada uno 
    for i, doc_id in enumerate(dense_docs_ids):
        dense_reciprocal_ranks[doc_id] = 1.0 / (i + 1) 
    for i, doc_id in enumerate(sparse_docs_ids):
        sparse_reciprocal_ranks[doc_id] = 1.0 / (i + 1) 

    # Combinamos los distintos rankings 
    combined_reprocical_ranks = {
        doc_id: 0.0 for doc_id in all_doc_ids
    }
    for doc_id in all_doc_ids:
        combined_reprocical_ranks[doc_id] = dense_weight + dense_reciprocal_ranks[doc_id] + sparse_weight + sparse_reciprocal_ranks[doc_id]

    # Ordenamos los doc_id en funcion de combined_reprocical_ranks en orden descendente
    sorted_docs_ids = sorted(all_doc_ids, key=lambda doc_id: combined_reprocical_ranks[doc_id], reverse=True)

    # Por ultimo iteramos sobre sorted_docs_ids y recuperamos los docs que nos ha dado el retriever
    sorted_docs = []
    all_docs = dense_docs + sparse_docs
    for doc_id in sorted_docs_ids:
        matching_docs = [
            doc for doc in all_docs if doc.metadata['id'] == doc_id
        ]
        if matching_docs:
            doc = matching_docs[0]
            doc.metadata['score'] = combined_reprocical_ranks[doc_id]
            doc.metadata['rank'] = sorted_docs_ids.index(doc_id) + 1
            # Añadimos cual es el retriever que ha encontrado la informacion
            if len(matching_docs) > 1:
                doc.metadata['retriever'] = 'both'
            elif doc in dense_docs:
                doc.metadata['retriever'] = 'dense'
            else:
                doc.metadata['retriever'] = 'sparse'
            sorted_docs.append(doc)

    return sorted_docs[:k]



pdf_path = 'code/pdf/google-2023-environmental-report.pdf'
collection_name = 'google_environmental_report'
str_output_parser = StrOutputParser()

pdf_reader = PdfReader(pdf_path)
text = ''
for page in pdf_reader.pages:
    text += page.extract_text()

# Tenemos un string muy grande con todo el contenido del archivo
# print(text)

# Entonces tenemos que separar el string en chunks mas manejables
# Muchas veces se usa OpenAIEmbeddings() en su lugar, pero asi no pagamos nada 
# text_splitter = SemanticChunker(OpenAIEmbeddings())
# splits = text_splitter.split_documents(docs)
character_splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n', '\n', '. ', ' ', ''],
    chunk_size=1000,
    chunk_overlap=200   # Solapamiento entre entre chunks, para evitar romper cosas importantes de repente
)
splits = character_splitter.split_text(text)

documents = [Document(page_content=text, metadata={
    'id': str(i)}) for i, text in enumerate(splits)
]

# Retriever 
# Estamos guardando los datos directamente en memoria. En un entorno mas sofisticado,
# deberiamos guardar los embeddings en una propia vectorstore mas permanente
chroma_client = chromadb.Client()
# Cargamos el modelo que nos va a hacer los embeddings (muy similar a embeddings.py)
embedding_function = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding_function,
    collection_name=collection_name,
    client=chroma_client
)
dense_retriever = vectorstore.as_retriever(
    search_kwargs={'k': 10}
)
sparse_retriever = BM25Retriever.from_documents(
    documents, 
    k=10
)

# Usamos mi modelo local de ollama para generar la respuesta
# Importante tener ollama corriendo en local con: ollama serve
llm = ChatOllama(model="qwen3")
# Necesitamos un prompt para el RAG. De momento vamos a dejar algo simple 
prompt = ChatPromptTemplate.from_messages([
    ("system", "Responde a la pregunta basándote únicamente en el siguiente contexto:\n\n{context}"),
    ("human", "{question}")
])
# La primera cadena se encarga de recibir el contexto y el prompt del usuario y pasarselo al llm 
# No da la respuesta del modelo, pero sirve para establecer la estructura 
rag_chain_from_docs = prompt | llm | str_output_parser
# Finalmente creamos la segunda cadena con los chunks devueltos por el retriever 
# Esta ya si le pasa los datos al llm y genera la respuesta siguiendo la estructura de la primera cadena 
# prompt -> llm -> str_output_parser(string de texto)
rag_chain_with_source = RunnableParallel(
    {
    'context': hybrid_search,
    'question': RunnablePassthrough()
    }).assign(answer=rag_chain_from_docs)

user_query = "What are Google's environmental initiatives?"
result = rag_chain_with_source.invoke(user_query)
print('\n', result, '\n')
final_answer = result['answer']
retrieved_docs = result['context']

print(f"\nOriginal question: {user_query}")
print(f"Final answer: \n{final_answer}")
print('\nRetrieved Documents:')
for i, doc in enumerate(retrieved_docs, start=1):
    doc_id = doc.metadata['id']
    doc_score = doc.metadata.get('score', 'N/A')
    doc_rank = doc.metadata.get('rank', 'N/A')
    doc_retriever = doc.metadata.get('retriever', 'N/A')
    print(f"Document {i}: Document ID: {doc_id} Score: {doc_score} Rank: {doc_rank} Retriever: {doc_retriever}\n")
    print(f"Content: \n{doc.page_content}\n")

'''
user_query = "What are Google's environmental initiatives?"
# Ejecutamos la búsqueda híbrida directamente, sin pasar por ninguna chain 
retrieved_docs = hybrid_search(user_query)
# retrieved_docs = dense_search(user_query)
# retrieved_docs = sparse_search(user_query)

print(f"\nOriginal question: {user_query}")
print('Retrieved Documents:')
for i, doc in enumerate(retrieved_docs, start=1):
    doc_id = doc.metadata['id']
    doc_score = doc.metadata.get('score', 'N/A')
    doc_rank = doc.metadata.get('rank', 'N/A')
    doc_retriever = doc.metadata.get('retriever', 'N/A')
    print(f"Document {i}: Document ID: {doc_id} Score: {doc_score} Rank: {doc_rank} Retriever: {doc_retriever}\n")
    print(f"Content: \n{doc.page_content}\n")
'''
