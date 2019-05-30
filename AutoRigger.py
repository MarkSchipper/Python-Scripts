import maya.cmds as base
import Locators
import Joints
import SecondaryLocators as SL
import Controller
import Constraints
import CreateIK
import FaceJoints as FJ
import os

## TODO: FOOTROLL


# we reload all classes when this file is executed, else we would need to restart Maya after every change
Locators = reload(Locators)
Joints = reload(Joints)
SL = reload(SL)
Controller = reload(Controller)
Constraints = reload(Constraints)
CreateIK = reload(CreateIK)
FJ  = reload(FJ)

class AutoRigger():
   
    def __init__(self):
        base.currentUnit(linear = 'meter')
        base.grid(size = 12, spacing = 5, divisions = 5)
        print os.path.dirname(os.path.realpath(__file__))
        self.BuildUI()
       
    def BuildUI(self): 
        #global spineValue 
        ###########################################
        #         Create the basic window        ##
        ###########################################
        
        # Create a window with the name Auto Rigger
        
        base.window("Auto Rigger")

        form = base.formLayout()
        tabs = base.tabLayout(imh = 5, imw = 5)
        
        base.formLayout(form, edit = True, attachForm=((tabs, 'top',0), (tabs,'left', 0), (tabs, 'right', 0), (tabs, 'bottom',0)))

        # set the layout of the window

        ch1 = base.rowColumnLayout(nc = 1, cal = (1, 'right'), adjustableColumn = True)
        
        base.image(w = 400, h = 100, image = os.path.dirname(os.path.realpath(__file__))+"\logo.jpg")
        settingsText = base.text('Settings', l = 'Rig Settings')
        base.separator(st = 'none')       
        #base.text(l = 'Prefix', w = 100)
        self.prefix = base.textFieldGrp(w = 100, text = 'test', editable = True)
        self.spineCount = base.intSliderGrp(l = "Spine Count", min = 1, max = 10, value = 4, step = 1, field = True)
        #spineCount = base.intField(minValue = 1, maxValue = 10, value = 4)
        self.fingerCount = base.intSliderGrp(l = "Finger Count", min = 1, max = 10, value = 5, step = 1, field = True)
        #fingerCount = base.intField(minValue = 0, maxValue = 10, value = 5)
        base.separator(h = 10, st = 'none')    
        self.doubleElbow = base.checkBox(l = 'Double Elbow', align = 'left' )
        
        base.setParent('..')
        
        ch2 = base.rowColumnLayout(nc = 1, cal = (1, 'right'), adjustableColumn = True)        
        base.separator(h = 10, st = 'none') 
        base.button(l = "Create Base Locators", w = 200, c = self.DoLocators)          
        base.separator(st = 'none')
        base.button(l = "Create Secondary Locators", w = 200, c = "SL.SecondaryLocators()")
        base.separator(st = 'none')
        base.button(l = "Mirror L->R", w = 200, c = "Locators.mirrorLocators()")
        base.separator(st = 'none', h = 20)
        base.button(l = "Create Facial Locators", w = 200, c = self.FaceLocators)
        base.separator(st = 'none')        
        base.button(l = "Delete All Locators", w = 200, c = "Locators.deleteLocators()")
        
        base.setParent('..')        
        ch3 = base.rowColumnLayout(nc = 1, cal = (1, 'right'), adjustableColumn = True)
        
        base.separator(st = 'none')    
        base.button(l = "Joints Window", w = 200, c = "Joints.CreateJointsWindow()")
        base.separator(st = 'none')    
        
        base.setParent('..')
        ch4 = base.rowColumnLayout(nc = 1, cal = (1, 'right'), adjustableColumn = True)
        base.button(l = "Add Facial Joints", w = 200, c = self.FaceJoints)
        base.separator(st = 'none')
        
        base.setParent('..')        
        ch5 = base.rowColumnLayout(nc = 1, cal = (1, 'right'), adjustableColumn = True)        
        
        base.button(l = "Finalize Rig", w = 200, c = self.FinalizeRig)
        base.separator(st = 'none')    
        base.button(l = "Bind Skin", w = 200, c = "Constraints.BindSkin()")
        base.separator(st = 'none')
        base.button(l = "Clear Locators", w = 200, c = self.ClearScene)

        base.setParent('..') 
        
        base.tabLayout(tabs, edit = True, tabLabel = ((ch1, 'Settings'), (ch2, 'Locators'), (ch3, 'Body Rig'), (ch4, 'Face Rig'), (ch5, 'Finalize') ))
               
        # show the actual window
        base.showWindow()
    
    def NextTab(self, void):
        base.tabLayout(edit = True, st = "2")
        
    def DoLocators(self, void):
        _spineCount = base.intSliderGrp(self.spineCount, q = True, v = True)
        _fingerCount = base.intSliderGrp(self.fingerCount, q = True, v = True)
        _doubleElbow = base.checkBox(self.doubleElbow, q = True, v = True)
        Locators.CreateLocators(_spineCount, _fingerCount, _doubleElbow)
    
    def FaceLocators(self, void):
        FJ.FaceJoints().CreateFaceWindow(self)
    
    def FaceJoints(self, void):
        FJ.FaceJoints().CreateJoints(self)
    
    def FinalizeRig(self, void):
        
        _spineCount = base.intSliderGrp(self.spineCount, q = True, v = True)
        _fingerCount = base.intSliderGrp(self.fingerCount, q = True, v = True) 
        Controller.CreateController(_spineCount, _fingerCount)
        CreateIK.IKHandles()
        Constraints.CreateConstraints(_fingerCount, _spineCount)  
        if(base.objExists("FACERIG_*")):        
            FJ.FaceJoints().AddConstraints(self)     

    def ClearScene(self, void):
        base.delete("Loc_Master")
        base.delete("SECONDARY")
        base.delete("FACE_LOC")


        