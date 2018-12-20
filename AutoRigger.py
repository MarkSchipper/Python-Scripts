import maya.cmds as base
import Locators
import Joints
import SecondaryLocators
import Controller
import Constraints
import CreateIK

## TODO: FOOTROLL


# we reload all classes when this file is executed, else we would need to restart Maya after every change
Locators = reload(Locators)
Joints = reload(Joints)
SecondaryLocators = reload(SecondaryLocators)
Controller = reload(Controller)
Constraints = reload(Constraints)
CreateIK = reload(CreateIK)

global selected
global prefix

class AutoRigger():
   
    def __init__(self):
        base.currentUnit(linear = 'meter')
        base.grid(size = 12, spacing = 5, divisions = 5)
        
        self.BuildUI()
       
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
        self.prefix = base.textFieldGrp(w = 100, text = 'test', editable = True)
        self.spineCount = base.intSliderGrp(l = "Spine Count", min = 1, max = 10, value = 4, step = 1, field = True)
        #spineCount = base.intField(minValue = 1, maxValue = 10, value = 4)
        self.fingerCount = base.intSliderGrp(l = "Finger Count", min = 1, max = 10, value = 5, step = 1, field = True)
        #fingerCount = base.intField(minValue = 0, maxValue = 10, value = 5)
        base.separator(h = 10, st = 'none')    
        self.doubleElbow = base.checkBox(l = 'Double Elbow', align = 'left' )
        base.separator(h = 10, st = 'none') 
        base.button(l = "Create Base Locators", w = 200, c = self.DoLocators)          
        base.separator(st = 'none')
        base.button(l = "Create Secondary Locators", w = 200, c = "SecondaryLocators.CreateSecLocatorWindows()")
        base.separator(st = 'none')
        base.button(l = "Delete All Locators", w = 200, c = "Locators.deleteLocators()")
        base.separator(st = 'none')        
        base.button(l = "Mirror L->R", w = 200, c = "Locators.mirrorLocators()")
        base.separator(st = 'none')    
        base.button(l = "Joints Window", w = 200, c = "Joints.CreateJointsWindow()")
        base.separator(st = 'none')    
        base.button(l = "Finalize Rig", w = 200, c = self.FinalizeRig)
        base.separator(st = 'none')    
        base.button(l = "Bind Skin", w = 200, c = "Constraints.BindSkin()")

        
        # show the actual window
        base.showWindow()
        
    def DoLocators(self, void):
        _spineCount = base.intSliderGrp(self.spineCount, q = True, v = True)
        _fingerCount = base.intSliderGrp(self.fingerCount, q = True, v = True)
        _doubleElbow = base.checkBox(self.doubleElbow, q = True, v = True)
        Locators.CreateLocators(_spineCount, _fingerCount, _doubleElbow)

    def FinalizeRig(self, void):
        
        _spineCount = base.intSliderGrp(self.spineCount, q = True, v = True)
        _fingerCount = base.intSliderGrp(self.fingerCount, q = True, v = True) 
        Controller.CreateController(_spineCount, _fingerCount)
        CreateIK.IKHandles()
        Constraints.CreateConstraints(_fingerCount, _spineCount)       



        