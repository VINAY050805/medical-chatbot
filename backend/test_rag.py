from app.services.rag_chain import get_rag_service

result = get_rag_service().ask(
    "What is diabetes?"
)

print("\nANSWER\n")
print(result["answer"])

print("\nSOURCES\n")

for src in result["sources"]:
    print(src)
