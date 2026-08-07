from app.services.embeddings import get_embedding_service

embedding = get_embedding_service().get_embeddings()

vector = embedding.embed_query("What is diabetes?")

print(len(vector))

print(vector[:10])
