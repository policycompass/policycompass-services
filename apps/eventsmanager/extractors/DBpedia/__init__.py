from SPARQLWrapper import SPARQLWrapper, JSON


def run(start, end, keyword):
    print("DBpedia Extractor: " + start + end + keyword)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

        SELECT ?event ?date ?comment ?label ?startDate ?endDate {
            ?event a dbpedia-owl:Event ;
            rdfs:comment ?comment ;
            rdfs:label ?label ;
            dbpedia-owl:date ?date .
            FILTER (?date > \"""" + start + """\"^^xsd:date &&
            ?date < \"""" + end + """\"^^xsd:date &&
            langMatches(lang(?label),"en") &&
            langMatches(lang(?comment),"en") &&
            (regex(?label, \"""" + keyword + """\", "i") || regex(?comment, \"""" + keyword + """\", "i"))) .
        }
        limit 100
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    output = []
    for key in results["results"]["bindings"]:
        output.append({"title": key["label"]["value"], "description": key["comment"]["value"], "date": key["date"]["value"] + "T00:00:00Z", "url": key["event"]["value"]})
    return output
