import click
import pcbnew
import csv
import os
import shutil
from pathlib import Path
from kikit.eeshema import extractComponents, getField
from kikit.defs import MODULE_ATTR_T
from kikit.fab.common import hasNonSMDPins
from kikit.common import *
from kikit.export import gerberImpl

def layerToSide(layer):
    if layer == pcbnew.F_Cu:
        return "T"
    if layer == pcbnew.B_Cu:
        return "B"
    raise RuntimeError(f"Got component with invalid layer {layer}")

def collectPosData(board, forceSmd):
    modules = []
    for module in board.GetModules():
        if module.GetAttributes() & MODULE_ATTR_T.MOD_VIRTUAL:
            continue
        # We can use module.HasNonSMDPins() in KiCAD 6
        if module.GetAttributes() & MODULE_ATTR_T.MOD_CMS or (forceSmd and not hasNonSMDPins(module)):
            modules.append(module)
    return [(module.GetReference(),
             (-1 if module.GetLayer() == pcbnew.B_Cu else 1) * toMm(module.GetPosition()[0]),
             -toMm(module.GetPosition()[1]),
             layerToSide(module.GetLayer()),
             module.GetOrientation() / 10) for module in modules]

def collectBom(components):
    bom = {}
    for c in components:
        reference = getField(c, "Reference")
        if reference.startswith("#PWR") or reference.startswith("#FL"):
            continue
        cType = (
            getField(c, "Value"),
            getField(c, "Footprint"),
            getField(c, "LCSC")
        )
        bom[cType] = bom.get(cType, []) + [reference]
    return bom

def posDataToFile(posData, filename):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        for line in sorted(posData, key=lambda x: x[0]):
            writer.writerow(line)

def bomToCsv(bomData, filename):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Comment", "Designator", "Footprint", "LCSC"])
        for cType, references in bomData.items():
            value, footprint, lscs = cType
            writer.writerow([value, ",".join(references), footprint, lscs])

@click.command()
@click.argument("board", type=click.Path(dir_okay=False))
@click.argument("outputdir", type=click.Path(file_okay=False))
@click.option("--assembly/--no-assembly", help="Generate files for SMT assembly (schematics is required)")
@click.option("--schematic", type=click.Path(dir_okay=False), help="Board schematics (required for assembly files)")
@click.option("--forceSMD", is_flag=True, help="Force include all components having only SMD pads")
@click.option("--ignore", type=str, default="", help="Comma separated list of designators to exclude from SMT assembly")
def jlcpcb(board, outputdir, assembly, schematic, forcesmd, ignore):
    """
    Prepare fabrication files for JLCPCB including their assembly service
    """
    loadedBoard = pcbnew.LoadBoard(board)
    refs = parseReferences(ignore)
    removeComponents(loadedBoard, refs)
    Path(outputdir).mkdir(parents=True, exist_ok=True)

    gerberdir = os.path.join(outputdir, "gerber")
    shutil.rmtree(gerberdir, ignore_errors=True)
    gerberImpl(board, gerberdir)
    shutil.make_archive(os.path.join(outputdir, "gerbers"), "zip", outputdir, "gerber")

    if not assembly:
        return
    if schematic is None:
        raise RuntimeError("When outputing assembly data, schematic is required")
    components = extractComponents(schematic)
    posDataToFile(collectPosData(loadedBoard, forcesmd), os.path.join(outputdir, "pos.csv"))
    bomToCsv(collectBom(components), os.path.join(outputdir, "bom.csv"))