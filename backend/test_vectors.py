from app.services.pinecone_store import get_pinecone_service

stats = get_pinecone_service().index.describe_index_stats()

print(stats)
