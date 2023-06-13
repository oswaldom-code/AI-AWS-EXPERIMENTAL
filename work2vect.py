from gensim.models import KeyedVectors
import numpy as np

# Carga el modelo desde el archivo .model
model = KeyedVectors.load("word2vec-google-news-300.model")

# Obtiene el vector para una palabra específica
word_vector = model['football']

# Imprime el vector
print("Vector de la palabra 'football':")
print(word_vector)

# Calcula la similitud entre dos palabras
similarity = model.similarity('football', 'soccer')

# Imprime la similitud
print("\nSimilitud entre 'football' y 'soccer':")
print(similarity)

# Encuentra las palabras más similares a una dada
similar_words = model.most_similar('football')

# Imprime las palabras más similares
print("\nPalabras más similares a 'football':")
for word, similarity in similar_words:
    print(f"{word}: {similarity}")
