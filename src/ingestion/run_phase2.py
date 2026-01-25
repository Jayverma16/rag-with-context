from pathlib import Path
from markdown_parser import parse_markdown
from chunkers import flat_chunker, hierarchy_aware_chunker


def main():
    md_path = Path("../docs/admin_guide.md")
    md_text = md_path.read_text()

    nodes = parse_markdown(md_text)

    flat_chunks = flat_chunker(nodes)
    hierarchy_chunks = hierarchy_aware_chunker(nodes)

    print("\n================ FLAT CHUNKS ================\n")
    for i, chunk in enumerate(flat_chunks, 1):
        print(f"[Flat Chunk {i}]")
        print(chunk["embedding_text"])
        print("-" * 50)

    print("\n============ HIERARCHY-AWARE CHUNKS ============\n")
    for i, chunk in enumerate(hierarchy_chunks, 1):
        print(f"[Hierarchy Chunk {i}]")
        print(chunk["embedding_text"])
        print("-" * 50)


if __name__ == "__main__":
    main()
