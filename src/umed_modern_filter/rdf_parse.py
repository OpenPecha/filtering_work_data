from rdflib import Graph


def parse_file(file_content, file_path):
    # Create an RDF graph
    g = Graph()

    # Parse the file content
    g.parse(data=file_content, format="turtle")

    # Now you can work with the RDF data
    # For example, you can iterate through the triples in the graph
    for subject, predicate, obj in g:
        print(f"Subject: {subject}, Predicate: {predicate}, Object: {obj}")
