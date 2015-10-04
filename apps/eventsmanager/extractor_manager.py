import imp
import os

ExtractorFolder = os.path.join(os.path.dirname(__file__), 'extractors')
EntryPoint = "__init__"

#Looks for extractors in extractors folder and return a list of them
def getExtractors():
    extractors = []
    p_extractors = os.listdir(ExtractorFolder)
    for i in p_extractors:
        location = os.path.join(ExtractorFolder, i)
        if not os.path.isdir(location) or not EntryPoint + ".py" in os.listdir(location):
            continue
        info = imp.find_module(EntryPoint, [location])
        extractors.append({"name": i, "info": info})
    return extractors

#returns an instance of a given extractor
def loadExtractor(extractor):
    return imp.load_module(EntryPoint, *extractor["info"])