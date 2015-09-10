import imp
import os

PluginFolder = os.path.join(os.path.dirname(__file__), 'extractors')
MainModule = "__init__"

def getExtractors():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    return plugins

def loadExtractor(plugin):
    return imp.load_module(MainModule, *plugin["info"])