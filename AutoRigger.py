import maya.cmds as base
import Locators
import Joints
import SecondaryLocators
import Controller
import Constraints

# we reload all classes when this file is executed, else we would need to restart Maya after every change
Locators = reload(Locators)
Joints = reload(Joints)
SecondaryLocators = reload(SecondaryLocators)
Controller = reload(Controller)
Constraints = reload(Constraints)

global selected
global prefix

class AutoRigger():
    
    def __init__(self):
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
        #base.rowColumnLayout(nc = 2, columnWidth=[(1,175), (2, 225)])
        base.columnLayout(adj = True)

        settingsText = base.text('Settings', l = 'Rig Settings')
        base.separator(st = 'none')       
        base.text(l = 'Prefix', w = 100)
        prefix = base.textFieldGrp(w = 100, text = 'test', editable = True)
        base.text(l = "Amount of Spines", w = 100)
        spineCount = base.intField(minValue = 1, maxValue = 10, value = 4)
        spineValue = base.intField(spineCount, query = True, value = True)
        base.text(l = "Amount of Fingers", w = 100)
        fingerCount = base.intField(minValue = 0, maxValue = 10, value = 5)
        base.separator(h = 10, st = 'none')    
        doubleElbow = base.checkBox(l = 'Double Elbow', align = 'left' )
        base.separator(h = 10, st = 'none')           
        base.button(l = "Create Base Locators", w = 200, c = "Locators.CreateLocators("+str(base.intField(spineCount, query = True, value = True))+","+str(base.intField(fingerCount, query = True, value = True))+ ", "+str(base.checkBox(doubleElbow,query = True, value = True))+")")
        base.separator(st = 'none')
        base.button(l = "Create Secondary Locators", w = 200, c = "SecondaryLocators.CreateSecLocatorWindows()")
        base.separator(st = 'none')
        base.button(l = "Delete All Locators", w = 200, c = "Locators.deleteLocators()")
        base.separator(st = 'none')        
        base.button(l = "Mirror L->R", w = 200, c = "Locators.mirrorLocators()")
        base.separator(st = 'none')    
        base.button(l = "Joints Window", w = 200, c = "Joints.CreateJointsWindow()")
        base.separator(st = 'none')    
        base.button(l = "Controllers", w = 200, c = "Controller.CreateController("+str(base.intField(spineCount, query = True, value = True))+","+str(base.intField(fingerCount, query = True, value = True))+")")
        base.separator(st = 'none')    
        base.button(l = "Add Constraints", w = 200, c = "Constraints.CreateConstraints("+str(base.intField(fingerCount, query = True, value = True))+")")
        # show the actual window
        base.showWindow()

