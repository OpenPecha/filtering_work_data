from rdflib import Graph

from umed_modern_filter.web_request import get_ttl


def parse_turtle_file(turtle_file_data):
    # Create a new RDF graph
    g = Graph()

    try:
        # Load the Turtle file into the graph
        g.parse(data=turtle_file_data, format="turtle")
        return g  # Return the parsed RDF graph
    except Exception as e:
        print(f"An error occurred while parsing the Turtle file: {e}")
        return None


# Example usage:
if __name__ == "__main__":
    turtle_file_data = get_ttl(
        "W00KG01589"
    )  # Replace with the path to your Turtle file
    rdf_graph = parse_turtle_file(turtle_file_data)

    if rdf_graph:
        # You can now work with 'rdf_graph' to extract information or query the RDF data.
        for subject, predicate, obj in rdf_graph:
            print(
                f"\n Subject (s): {subject}, Predicate: {predicate}, Object: {obj} \n"
            )
