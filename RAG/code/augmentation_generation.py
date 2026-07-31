from indexing import Indexing 
from retrieval import Retrieval
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from config import DIR_PATH, CONTEXT_FILE_PATH, COLLECTION_NAME, OLLAMA_MODEL



# Augmentation -> Los chunks recuperados se añaden al prompt del modelo junto con la query del usuario
# Generation -> El LLM finalmente genera la respuesta utilizando el contexto que le hemos dado en el prompt 
class AugmentationGeneration:

    def __init__(self):
        # Usamos mi modelo local de ollama para generar la respuesta (de momento)
        # Importante tener ollama corriendo en local con: ollama serve
        self.llm = ChatOllama(model=OLLAMA_MODEL)
        # Necesitamos un prompt para el RAG. De momento vamos a dejar algo simple 
        self.prompt = ChatPromptTemplate.from_messages([
            ('system', 'Responde en español, intentando ser lo más breve posible pero respondiendo con mucha claridad. Responde únicamente en función del siguiente contexto (si no encuentras la respuesta en el contexto, hazlo saber al usuario):\n\n{context}'),
            ('human', '{question}')
        ])
        self.str_output_parser = StrOutputParser()

    
    # Metodo para definir la cadena a traves de la cual se va a generar la respuesta 
    # En este caso necesitamos recibir una instancia de Retriever para acceder a sus metodos 
    def define_chain(self, retrieval_instance):
        # La primera cadena se encarga de recibir el contexto y el prompt del usuario y pasarselo al llm 
        # No da la respuesta del modelo, pero sirve para establecer la estructura 
        rag_chain_from_docs = self.prompt | self.llm | self.str_output_parser
        # Finalmente creamos la segunda cadena con los chunks devueltos por el retriever 
        # Esta ya si le pasa los datos al llm y genera la respuesta siguiendo la estructura de la primera cadena 
        # prompt -> llm -> str_output_parser(string de texto)
        print(f'Iniciando {OLLAMA_MODEL}...')
        rag_chain_with_source = RunnableParallel(
        {
            'context': retrieval_instance.hybrid_search,
            'question': RunnablePassthrough()
        }).assign(answer=rag_chain_from_docs)
        return rag_chain_with_source


    # Metodo para generar la respuesta en el terminal. Devuelve el contexto para la funcion save_context_in_file
    def generate_response(self, rag_chain_with_source, user_query): 
        print('\n')
        context = []
        # Iteramos sobre cada chunk que el llm va generando, para mostrar el texto poco a poco en el terminal (me gusta mas asi)
        for chunk in rag_chain_with_source.stream(user_query):
            # Añadimos el contexto si retrieved_docs esta vacio, para añadir todo el contexto una sola vez 
            if 'context' in chunk and not context:
                context = chunk['context']
            if 'answer' in chunk:
                # Mostramos la respuesta
                print(chunk['answer'], end='', flush=True)
        return context 


    # Metodo para volcar el contexto en un fichero, para comprobar que el retriever funciona correctamente 
    def save_context_in_file(self, context):
        with open(CONTEXT_FILE_PATH, 'w', encoding='utf-8') as f:
            for i, doc in enumerate(context, start=1):
                doc_id = doc.metadata['id']
                doc_source = doc.metadata['source']
                # Al usar EnsembleRetriever no tengo control (no genero) estos parametros
                # doc_score = doc.metadata.get('score', 'N/A')
                # doc_rank = doc.metadata.get('rank', 'N/A')
                # doc_retriever = doc.metadata.get('retriever', 'N/A')
                f.write(f"\n\nDocument {i}: Document ID: {doc_id} Source: {doc_source}\n")
                f.write('-'*100)
                f.write(f"\nContent: \n{doc.page_content}\n\n")
        f.close()
        print(f"\n\nFichero '{CONTEXT_FILE_PATH}' creado correctamente!")





if __name__ == '__main__':

    # Indexing 
    indexing = Indexing(DIR_PATH, COLLECTION_NAME)
    vectorstore = indexing.load_vectorstore()
    print('Base de datos cargada correctamente!')
    dense_retriever = indexing.get_dense_retriever(vectorstore)
    sparse_retriever = indexing.get_sparse_retriever(vectorstore)


    # Retrieval 
    retrieval = Retrieval(dense_retriever, sparse_retriever)  


    # Augmentation and Generation 
    augmentation_generation = AugmentationGeneration()
    rag_chain_with_source = augmentation_generation.define_chain(retrieval)
    user_query = 'Como puedo cambiar la configuración de input de mi teclado?'
    context = augmentation_generation.generate_response(rag_chain_with_source, user_query)
    augmentation_generation.save_context_in_file(context)
