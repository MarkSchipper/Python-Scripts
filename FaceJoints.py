import maya.cmds as base

def CreateFaceWindow():
    base.window("Facial Rig")
    base.rowColumnLayout(nc = 1)
    base.button(l = "Create Face Locators", w = 200, c = "FaceJoints.Locators()")
    hideLocs = base.checkBox(l = "Hide Body Locators", align = 'left')
    base.showWindow()
    
    
def Locators():
    pass    