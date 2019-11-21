import json
import ast
# import requests
import sys
import argparse
# from string import Template 
import os
from jinja2 import Template
# req = requests.get("url")
# route["sampleResponse"] = req.content.decode('utf-8')

def getData(resources):
    routes = []
    folders = []
    workspace = {}
    varsEnv = None

    for data in resources:
        if(data["_type"] == "request_group"):
            folder = {}
            folder["_id"] = data["_id"]
            folder["name"] = data["name"]
            folder["routes"] = []

            folders.append(folder)

        elif(data["_type"] == "workspace"):
            workspace["name"] = data["name"]

        elif(data["_type"] == "environment"):
            if(data["data"]):
                varsEnv = data["data"]

    for data in resources:  
        if(data["_type"] == "request"):
            route = { "url": data["url"], "methods" : []}
            methodData = {}
            methodData["parentId"] = data["parentId"]
            methodData["name"] = data["name"]
            methodData["method"] = data["method"]

            try:
                methodData["contentType"] = data["body"]["mimeType"]
                methodData["sampleRequest"] = ast.literal_eval(data["body"]["text"])
            except KeyError:
                methodData["sampleRequest"] = False

            if(data["headers"]):
                methodData["headers"] = data["headers"]
            else:
                methodData["headers"] = False

            if(data["authentication"]):
                methodData["authentication"] = data["authentication"]
            else:
                methodData["authentication"] = False

            if(data["description"]):
                methodData["description"] = data["description"]
            else:
                methodData["description"] = False
            localized = False
            for folder in folders:
                if(folder["_id"] == methodData["parentId"]):
                    for routeFolder in folder["routes"]:      
                        if(routeFolder["url"] == route["url"]):
                            routeFolder["methods"].append(methodData)
                            localized = True

                    if(not localized):
                        route["methods"].append(methodData)
                        folder["routes"].append(route)

    #print(folders)
    return workspace, folders, varsEnv

def generateYAML(workspace, folders, varsEnv):
    with open(os.path.dirname(os.path.abspath(__file__))+"/templates/base.yaml") as file:  
        base = file.read() 
    
    baseT = Template(base, trim_blocks= True, lstrip_blocks= True)

    final = baseT.render(workspace = workspace, folders = folders, varsEnv = varsEnv)

    #print(final)

    f = open("test.yaml", "w")
    f.write(final)
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","-insomnia", type=str)
    parser.add_argument("-o","-output", type=str)
    args = parser.parse_args()

    with open(args.i) as json_file:
        data = json.load(json_file)

    resources = data["resources"]

    workspace, folders, varsEnv = getData(resources)

    if("yaml" in args.o): 
        generateYAML(workspace, folders, varsEnv)