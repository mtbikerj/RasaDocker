import glob
import os
import ast

domainDir = "domain/"

def writeSubFile(outfile, subfileName, spacer):
    with open (subfileName) as infile:
        for line in infile.readlines():
            outfile.write(spacer + line)

def intents(outfile):
    outfile.write("\n\nintents:\n")
    writeSubFile(outfile, domainDir + "intents.yml", "  ")

def entities(outfile):
    outfile.write("\n\nentities:\n")
    writeSubFile(outfile, domainDir + "entities.yml", "  ")

def slots(outfile):
    outfile.write("\n\nslots:\n")
    writeSubFile(outfile, domainDir + "slots.yml", "  ")

def templates(outfile):
    outfile.write("\n\ntemplates:")
    utterance_files = glob.glob(domainDir + "utterances/*.yml")
    for fname in utterance_files:
        outfile.write("\n  utter_" + os.path.basename(fname)[:-4] + ":\n")
        writeSubFile(outfile, fname, "    ")

def actions(outfile):
    outfile.write("\n\nactions:")
    files = glob.glob(domainDir + "utterances/*.yml")
    for fname in files:
        outfile.write("\n  - utter_" + os.path.basename(fname)[:-4])
    
    files = glob.glob(domainDir + "actions/*.py")
    for fname in files:
        str = ""
        with open(fname) as infile:
            str = infile.read()
        
        p = ast.parse(str)
        classes = [node for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
        for item in classes:
            if item.bases[0].id == "Action":
                outfile.write("\n  - domain.actions."+ os.path.basename(fname)[:-3] + "." + item.name)

def build_domain():
    if os.path.split(os.getcwd())[1] == 'domain' :
        global domainDir
        domainDir = ""

    with open(domainDir + "domain.yml", "w") as outfile:
        intents(outfile)
        #entities(outfile) - comment out until entities are added to entities.yml
        #slots(outfile) - comment out until slots are added to slots.yml
        templates(outfile)
        actions(outfile)
        

if __name__ == '__main__':
    build_domain()