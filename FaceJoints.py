import maya.cmds as base

class FaceJoints():

    def __init__(self):
        self.CreateFaceWindow(self)
        
    
    def CreateFaceWindow(self, void):
        base.window("Facial Rig")
        base.rowColumnLayout(nc = 2)
        base.button(l = "Create Face Locators", w = 200, c = self.Locators)
        base.showWindow()
    
    def Locators(self, void):
        # eyelids
        self.EyeLocators(self)
        # mouth
        
        # eyebrows
        
        # smiling muscle
   
   
    def EyeLocators(self, void):
        
        if (base.objExists("L_Eye")):
            sides = ['L', 'R']
            sideMultiplier = 1
        
            for side in sides:
            
                eyeCenterLoc = base.spaceLocator(n = "Loc_"+side+"_EyeCenter")
                base.scale(0.01, 0.01, 0.01, eyeCenterLoc)
                eyePos = base.xform(base.ls(side+"_Eye.rotatePivot"), q = True, t = True, ws = True)
                base.move(eyePos[0], eyePos[1], eyePos[2], eyeCenterLoc)
                
                eyeAimLoc = base.spaceLocator(n = "Loc_"+side+"_EyeAim")
                base.scale(0.01, 0.01, 0.01, eyeAimLoc) 
                base.move(eyePos[0], eyePos[1], eyePos[2]+0.025, eyeAimLoc)
                
                upperLid = base.curve(p = [(0,0,0), (0.05 * sideMultiplier, 0.02, 0), (0.1 * sideMultiplier, 0.04,0), (0.15 * sideMultiplier, 0.02, 0), (0.2 * sideMultiplier,0,0)], n = "CV_"+side+"_UpperEyeLid")
                base.scale(0.1, 0.1, 0.1, upperLid)
                
                eyeAimPos = base.xform(eyeAimLoc, q = True, t = True, ws = True)                
                base.move(eyeAimPos[0], eyeAimPos[1] + 0.005, eyeAimPos[2], upperLid)
                
                lowerLid = base.curve(p = [(0,0,0), (0.05 * sideMultiplier, -0.02, 0), (0.1 * sideMultiplier, -0.04,0), (0.15 * sideMultiplier, -0.02, 0), (0.2 * sideMultiplier,0,0)], n = "CV_"+side+"_LowerEyeLid")
                base.scale(0.1, 0.1, 0.1, lowerLid)
                base.move(eyeAimPos[0], eyeAimPos[1] - 0.005, eyeAimPos[2], lowerLid)
                
                sideMultiplier = -1
                               
        else:
            base.confirmDialog(title = "Eyes missing", message = "The eyes ( L_Eye - R_Eye ) could not be found", button = ['Ok'])        