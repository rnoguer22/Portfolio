import numpy as np 
from sentence_transformers import SentenceTransformer 



def euclidean_distance(v1, v2):
    return np.linalg.norm(v1 - v2)

def cosine_distance(v1, v2):
    cosine = abs(np.dot(v1, v2) / 
        (np.linalg.norm(v1) * np.linalg.norm(v2)))
    return cosine 



sentences = [
    'This blanket has such a cozy temperature for me!', 
    'I am so much warmer and snug using this spread', 
    'Taylor Swift was 34 years old in 2024.'
]

model = SentenceTransformer('all-MiniLM-L6-v2')
# model = SentenceTransformer('all-mpnet-base-v2') # Este modelo se supone que es mejor pero bue
embeddings = model.encode(sentences)
# print(embeddings[0])
print(embeddings.shape)

# No es un vector (embedding) por palabra, si no 384 por cada frase 
# Primero se vectoriza cada token, y se funden en la dimensionalidad del modelo all-MiniLM-L6-v2 - 384

print('\n')
# Distancia euclidiana 
print("Euclidean distance between 0 and 1: ", euclidean_distance(embeddings[0], embeddings[1]))
print("Euclidean distance between 0 and 2: ", euclidean_distance(embeddings[0], embeddings[2]))
print("Euclidean distance between 1 and 2: ", euclidean_distance(embeddings[1], embeddings[2]))
# Vemos que la distancia entre 0 y 1 es menor, y es logico ya que hablan de estar calentito

print('\n')
# Producto escalar (proyeccion de un vector sobre otro)
print("Dot product between 0 and 1: ", np.dot(embeddings[0], embeddings[1]))
print("Dot product between 0 and 2: ", np.dot(embeddings[0], embeddings[2]))
print("Dot product between 0 and 2: ", np.dot(embeddings[0], embeddings[2]))
# Vemos que la proyeccion de 0 sobre 1 es 0.47, mucho mayor que sobre 2 que es 0.02

print('\n')
# Cosine distance (distancia del coseno) 
# Mide la direccion en la que apuntan - 1 misma direccion - 0 perpendiculares - -1 direcciones opuestas 
print("Cosine distance between 0 and 1: ", cosine_distance(embeddings[0], embeddings[1]))
print("Cosine distance between 0 and 2: ", cosine_distance(embeddings[0], embeddings[2]))
print("Cosine distance between 1 and 2: ", cosine_distance(embeddings[1], embeddings[2]))
