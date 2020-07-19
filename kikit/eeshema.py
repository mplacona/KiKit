# Simple, rather hacky parser for eeshema files (.sch)

import shlex

class EeschemaException(Exception):
    pass

def getField(component, field):
    for f in component["fields"]:
        n = f["number"]
        if field == "Reference" and n == 0:
            return f["text"]
        if field == "Value" and n == 1:
            return f["text"]
        if field == "Footprint" and n == 2:
            return f["text"]
        if "name" in f and field == f["name"]:
            return f["text"]
    return None

def readEeschemaLine(file):
    line = file.readline()
    if not line:
        raise EeschemaException("Cannot parse EEschema, line expected, got EOF")
    return line.strip()

def readHeader(file):
    VERSION_STRING = "EESchema Schematic File Version"
    DESCR_STRING = "$Descr "
    header = {}
    while True:
        line = readEeschemaLine(file)
        if line == "$EndDescr":
            return header

        if line.startswith(VERSION_STRING):
            header["version"] = line[len(VERSION_STRING):].strip()
        elif line.startswith("LIBS:"):
            header["libs"] = header.get("libs", []) + [line[len("LIBS:"):].strip()]
        elif line.startswith("EELAYER"):
            pass
        elif line.startswith(DESCR_STRING):
            header["size"] = line[len(DESCR_STRING):].split()
        elif line.startswith("Sheet"):
            items = line.split(maxsplit=3)
            header["sheet"] = (int(items[1]), int(items[2]))
        elif line.startswith("Title"):
            header["title"] = line.split(maxsplit=2)[1]
        elif line.startswith("Date"):
            header["date"] = line.split(maxsplit=2)[1]
        elif line.startswith("Comp"):
            header["company"] = line.split(maxsplit=2)[1]
        elif line.startswith("Rev"):
            header["revision"] = line.split(maxsplit=2)[1]
        elif line.startswith("Comment1"):
            header["comment1"] = line.split(maxsplit=2)[1]
        elif line.startswith("Comment2"):
            header["comment2"] = line.split(maxsplit=2)[1]
        elif line.startswith("Comment3"):
            header["comment3"] = line.split(maxsplit=2)[1]
        elif line.startswith("Comment4"):
            header["comment4"] = line.split(maxsplit=2)[1]
        elif line.startswith("encoding"):
            header["encoding"] = line.split(maxsplit=2)[1]
        else:
            raise EeschemaException(f"Unexpected line: '{line}'")

def readComponent(file):
    component = {}
    while True:
        line = readEeschemaLine(file)
        if line == "$EndComp":
            return component

        if line.startswith("L"):
            items = line.split()
            component["reference"] = items[1]
            component["name"] = items[0]
        elif line.startswith("U"):
            component["u"] = line.split()[1:]
        elif line.startswith("P"):
            items = line.split()
            component["position"] = (int(items[1]), int(items[2]))
        elif line.startswith("F"):
            items = shlex.split(line)
            field = {
                "number": int(items[1]),
                "text": items[2],
                "orientation": items[3],
                "position": (int(items[4]), int(items[5])),
                "size": items[6],
                "flags": items[7],
                "justify": items[8],
                "style": items[9]
            }
            if field["number"] >= 4:
                field["name"] = items[10]
            component["fields"] = component.get("fields", []) + [field]
        else:
            items = shlex.split(line)
            try:
                int(items[0])
                if len(items) == 3 and items[0] == "1":
                    # Duplicate position entry
                    pass
                if len(items) == 4:
                    component["orientation"] = [int(x) for x in items[1:]]
            except ValueError:
                raise EeschemaException(f"Unexpected line: '{line}'")

def extractComponents(filename):
    """
    Extract all components from the schematics
    """
    components = []
    with open(filename, "r", encoding="utf-8") as file:
        header = readHeader(file)
        while True:
            line = file.readline()
            if not line:
                return components
            line = line.strip()
            if line.startswith("$Comp"):
                components.append(readComponent(file))

