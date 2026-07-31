from indexing import Indexing
from langchain_classic.retrievers import EnsembleRetriever 
from config import DIR_PATH, COLLECTION_NAME, K  



# Fase de Retrieval 
# El usuario hace una pregunta y se buscan los chunks mas relevantes
# (esto se puede hacer por similitud, BM25, busqueda hibrida, etc.)
class Retrieval:

    def __init__(self, dense_retriever, sparse_retriever):
        self.dense_retriever = dense_retriever
        self.sparse_retriever = sparse_retriever


    # En una busqueda densa se usan vectores que buscan por significado y contexto los chunks que contienen la informacion
    # Ventaja: Relaciona conceptos equivalentes y sinonimos aunque no sea la misma palabra (vehiculo - coche)
    def dense_search(self, query):
        dense_docs = self.dense_retriever.invoke(query)[:K]
        dense_docs_ids = [doc.metadata['id'] for doc in dense_docs]
        return dense_docs, dense_docs_ids


    # La busqueda dispersa busca coincidencias exactas con las palabras clave de la query (eliminando articulos, preposiciones, etc.)
    # Ventaja: Muy util para nombre propios, codigos, siglas, aspectos tecnicos, etc.
    def sparse_search(self, query):
        sparse_docs = self.sparse_retriever.invoke(query)[:K]
        sparse_docs_ids = [doc.metadata['id'] for doc in sparse_docs]
        return sparse_docs, sparse_docs_ids


    # La busqueda hibrida combina ambas busquedas (densa y dispersa) aplicando RRF (Reciprocal Rank Fusion) para combinar los resultados
    # (se usa RRF para saber cual es mas importante, ya que el 4 denso puede ser mas importante que el 1 disperso)
    # Elimina chunks duplicados y los reordena dandoles una puntuacion en funcion de su importancia 
    def hybrid_search(self, query, dense_weight=0.5, sparse_weight=0.5, lang_ensemble_retriever=True):
        # Devolvemos los top-k documentos mas importantes de la busqueda
        dense_docs, dense_docs_ids = self.dense_search(query)
        sparse_docs, sparse_docs_ids = self.sparse_search(query)

        if lang_ensemble_retriever:
            # Usamos una clase de langchain que automatiza todo el procedimiento
            # Si no queremos usarla, indicamos lang_ensemble_retriever=False al llamar al metodo 
            ensemble_retriever = EnsembleRetriever(
                retrievers=[self.dense_retriever, self.sparse_retriever],
                weights=[dense_weight, sparse_weight]
            )
            return ensemble_retriever.invoke(query)[:K]

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

        return sorted_docs[:K]



if __name__ == '__main__':

    # Necesitamos hacer la fase de Indexing
    indexing = Indexing(DIR_PATH, COLLECTION_NAME)
    vectorstore = indexing.load_vectorstore()
    print('Base de datos cargada correctamente!')
    dense_retriever = indexing.get_dense_retriever(vectorstore)
    sparse_retriever = indexing.get_sparse_retriever(vectorstore)

    # Retrieval 
    user_query = 'Where can I find my file hyprland.lua?'
    retrieval = Retrieval(dense_retriever, sparse_retriever)
    dense_docs, dense_docs_ids = retrieval.dense_search(user_query)
    print('Dense IDs: ', dense_docs_ids)
    sparse_docs, sparse_docs_ids = retrieval.sparse_search(user_query)
    print('Sparse IDs: ', sparse_docs_ids)
    
    # (version sin usar modelo llm, ya que no hemos llegado a la fase todavia)
    # Con esto simplemente estamos mostrando los distintos chunks de la busqueda hibrida (RRF)
    hybrid_docs = retrieval.hybrid_search(user_query)
    print(f"\nOriginal question: {user_query}")
    print('Retrieved Documents:')
    for i, doc in enumerate(dense_docs, start=1):
        doc_id = doc.metadata['id']
        doc_score = doc.metadata.get('score', 'N/A')
        doc_rank = doc.metadata.get('rank', 'N/A')
        doc_retriever = doc.metadata.get('retriever', 'N/A')
        print(f"Document {i}: Document ID: {doc_id} Score: {doc_score} Rank: {doc_rank} Retriever: {doc_retriever}\n")
        print(f"Content: \n{doc.page_content}\n")
