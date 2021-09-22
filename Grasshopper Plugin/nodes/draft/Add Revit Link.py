

from System import Enum, Action

import rhinoscriptsyntax as rs
import Rhino
import RhinoInside
import Grasshopper
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
from RhinoInside.Revit import Revit, Convert
# add extensions methods as well
# this allows calling .ToXXX() convertor methods on Revit objects
clr.ImportExtensions(Convert.Geometry)
from Autodesk.Revit import DB

# access the active document object
doc = Revit.ActiveDBDocument
app = Revit.ActiveDBApplication

# a few utility methods
def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)

#This is for converting single items to list so we can loop through it.
FilePath = FilePath if isinstance(FilePath, list) else [FilePath]
LinkInstance = []

# write your code here

with DB.Transaction(doc, "Give it a descriptive name") as t:
    t.Start()
    if RUN:
        try:
            for file in FilePath:
                modelpath = DB.ModelPathUtils.ConvertUserVisiblePathToModelPath(file)
                linkoptions = DB.RevitLinkOptions(False)
                revitlinktype = DB.RevitLinkType.Create(doc, modelpath, linkoptions)
                placement = DB.ImportPlacement(1)
                instance = DB.RevitLinkInstance.Create(doc, revitlinktype.ElementId, placement)
                LinkInstance.append(instance)
            t.Commit()
        except Exception as txn_err:
            show_error(str(txn_err))
            t.RollBack()

