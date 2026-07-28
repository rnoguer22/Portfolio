


# Fase de Retrieval 
# El usuario hace una pregunta y se buscan los chunks mas relevantes
# (esto se puede hacer por similitud, BM25, busqueda hibrida, etc.)
class Retrieval:

    # En una busqueda densa se usan vectores que buscan por significado y contexto los chunks que contienen la informacion
    # Ventaja: Relaciona conceptos equivalentes y sinonimos aunque no sea la misma palabra (vehiculo - coche)
    def dense_search(self, query, k=10, dense_weight=0.5):
        dense_docs = dense_retriever.invoke(query)[:k]
        dense_docs_ids = [doc.metadata['id'] for doc in dense_docs]
        print('Dense IDs: ', dense_docs_ids)
        return dense_docs


    # La busqueda dispersa busca coincidencias exactas con las palabras clave de la query (eliminando articulos, preposiciones, etc.)
    # Ventaja: Muy util para nombre propios, codigos, siglas, aspectos tecnicos, etc.
    def sparse_search(self, query, k=10, sparse_weight=0.5):
        sparse_docs = sparse_retriever.invoke(query)[:k]
        sparse_docs_ids = [doc.metadata['id'] for doc in sparse_docs]
        print('Sparse IDs: ', sparse_docs_ids)
        return sparse_docs


    # La busqueda hibrida combina ambas busquedas (densa y dispersa) aplicando RRF (Reciprocal Rank Fusion) para combinar los resultados
    # (se usa RRF para saber cual es mas importante, ya que el 4 denso puede ser mas importante que el 1 disperso)
    # Elimina chunks duplicados y los reordena dandoles una puntuacion en funcion de su importancia 
    def hybrid_search(self, query, k=10, dense_weight=0.5, sparse_weight=0.5):
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
