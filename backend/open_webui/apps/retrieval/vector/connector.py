from open_webui.config import VECTOR_DB

if VECTOR_DB == "qdrant":
    from open_webui.apps.retrieval.vector.dbs.qdrant import QdrantClient

    VECTOR_DB_CLIENT = QdrantClient()
else:
    from open_webui.apps.retrieval.vector.dbs.pgvector import PgvectorClient

    VECTOR_DB_CLIENT = PgvectorClient()
