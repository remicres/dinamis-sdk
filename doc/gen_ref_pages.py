"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

processed_paths = ["dinamis_sdk"]

paths = []
for processed_path in processed_paths:
    paths += Path(processed_path).rglob("*.py")
    
for path in paths:
    module_path = path.relative_to(".").with_suffix("")
    doc_path = path.relative_to(".").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)
    print("\n---")
    print(f"path: {path}")
    print(f"module path: {module_path}")
    print(f"doc path:{doc_path}")

    parts = tuple(module_path.parts)
    print(f"parts: {parts}")

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    print(f"new doc path:{doc_path}")
    print(f"new parts: {parts}")
    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
