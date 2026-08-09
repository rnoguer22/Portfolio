from RAG.code.indexing import Indexing 
from RAG.code.retrieval import Retrieval
from RAG.code.augmentation_generation import AugmentationGeneration
from config import DIR_PATH, COLLECTION_NAME, OLLAMA_MODEL, GROQ_MODEL, HUGGINGFACE_EMBEDDINGS
from helpers.pretty_terminal import PrettyTerminal





if __name__ == '__main__':


    pretty_terminal = PrettyTerminal()
    pretty_terminal.show_rag_init_info(GROQ_MODEL, HUGGINGFACE_EMBEDDINGS)

    # 1) Indexing 
    indexing = Indexing(DIR_PATH, COLLECTION_NAME, debug=False)
    vectorstore = indexing.load_vectorstore()
    dense_retriever = indexing.get_dense_retriever(vectorstore)
    sparse_retriever = indexing.get_sparse_retriever(vectorstore)

    # 2) Retrieval 
    retrieval = Retrieval(dense_retriever, sparse_retriever)  

    # 3) Augmentation 
    augmentation_generation = AugmentationGeneration(local=False)
    rag_chain_with_source = augmentation_generation.define_chain(retrieval)

    # Bucle infinito para que el usuario haga las preguntas que quiera 
    while True:
        try:
            # Obtenemos la query del usuario 
            user_query = pretty_terminal.get_user_query(name='Obsidian RAG')
            if user_query:
                # 4) Generation 
                context, answer = augmentation_generation.generate_response(rag_chain_with_source, user_query)
                augmentation_generation.save_context_in_file(context)

        except KeyboardInterrupt:
            print('\nBye!')
            break
