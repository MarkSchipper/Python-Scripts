import maya.cmds as base
import Locators
import Joints
import SecondaryLocators

# we reload all classes when this file is executed, else we would need to restart Maya after every change
reload(Locators)
Joints = reload(Joints)
SecondaryLocators = reload(SecondaryLocators)
global selected

class AutoRigger():
    
    def __init__(self):
        self.widgets = {}
        self.BuildUI()
       # spineValue = 0
        
        
    def BuildUI(self): 
        #global spineValue 
        ###########################################
        #         Create the basic window        ##
        ###########################################
        
        # Create a window with the name Auto Rigger
        
        base.window("Auto Rigger")

        # set the layout of the window
        base.rowColumnLayout(nc = 2, columnWidth=[(1,175), (2, 225)])

        settingsText = base.text('Settings', l = 'Rig Settings')
        base.separator(st = 'none')       
        base.text(l = 'Prefix', w = 100)
        base.textField(w = 100)
        base.text(l = "Amount of Spines", w = 100)
        spineCount = base.intField(minValue = 1, maxValue = 10, value = 4)
        spineValue = base.intField(spineCount, query = True, value = True)
        print spineValue
        base.text(l = "Amount of Fingers", w = 100)
        fingerCount = base.intField(minValue = 0, maxValue = 10, value = 5)    
        
        base.button(l = "Create Base Locators", w = 200, c = "Locators.CreateLocators("+str(base.intField(spineCount, query = True, value = True))+","+str(base.intField(fingerCount, query = True, value = True))+ ")")
        base.separator(st = 'none')
        base.button(l = "Create Secondary Locators", w = 200, c = "SecondaryLocators.CreateSecLocatorWindows()")
        base.separator(st = 'none')
        base.button(l = "Delete All Locators", w = 200, c = "Locators.deleteLocators()")
        base.separator(st = 'none')        
        base.button(l = "Mirror L->R", w = 200, c = "Locators.mirrorLocators()")
        base.separator(st = 'none')        
        base.button(l = "Create Joints", w = 200, c = "Joints.CreateJointsWindow()")
        # show the actual window
        base.showWindow()
