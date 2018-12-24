import maya.cmds as base

class FaceJoints():

    def __init__(self):
        self.CreateFaceWindow(self)
        
    
    def CreateFaceWindow(self, void):
        
        self.sides = ['L', 'R']
        
        base.window("Facial Rig")
        base.rowColumnLayout(nc = 2)
        base.button(l = "Create Face Locators", w = 200, c = self.Locators)
        base.separator(st = 'none')
        base.button(l = "Mirror L -> R", w = 200, c = self.MirrorLocators)
        base.separator(st = 'none', h = 30)
        base.button(l = "Add Joints", w = 200, c = self.CreateJoints)
        base.separator(st = 'none', h = 30)    
        base.button(l = "Add Constraints", w = 200, c = self.AddConstraints)
        base.separator(st = 'none')
        base.button(l = "Add Controllers", w = 200, c = self.AddControllers)
        base.showWindow()
    
    def Locators(self, void):
        
        base.group(em = True, n = "FACE_LOC")
        self.sideMultiplier = 1
        # eyelids
        self.EyeLocators(self)
        # mouth
        self.MouthLocators(self)
        # eyebrows
        self.EyeBrowLocators(self)
        # smiling muscle
        self.SmileMuscles(self)
        
        #add spaceLocators
        self.AddLocators(self)
        
        
   
    def EyeLocators(self, void):
        
        
        if (base.objExists("L_Eye")):
            
          for side in self.sides:
            
                eyeCenterLoc = base.spaceLocator(n = "Loc_Face"+side+"_EyeCenter")
                base.scale(0.01, 0.01, 0.01, eyeCenterLoc)
                eyePos = base.xform(base.ls(side+"_Eye.rotatePivot"), q = True, t = True, ws = True)
                base.move(eyePos[0], eyePos[1], eyePos[2], eyeCenterLoc)
                base.parent(eyeCenterLoc, "FACE_LOC")                 

                eyeAimLoc = base.spaceLocator(n = "Loc_Face"+side+"_EyeAim")
                base.scale(0.01, 0.01, 0.01, eyeAimLoc) 
                base.move(eyePos[0] - (0.004 * self.sideMultiplier), eyePos[1], eyePos[2]+0.025, eyeAimLoc)
                base.parent(eyeAimLoc, "FACE_LOC")
                
                upperLid = base.curve(p = [(0,0,0), (0.05 * self.sideMultiplier, 0.02, 0), (0.1 * self.sideMultiplier, 0.04,0), (0.15 * self.sideMultiplier, 0.02, 0), (0.2 * self.sideMultiplier,0,0)], n = "CV_"+side+"_UpperEyeLid")
                base.scale(0.1, 0.1, 0.1, upperLid)
                base.parent(upperLid, "FACE_LOC")                
                eyeAimPos = base.xform(eyeAimLoc, q = True, t = True, ws = True)                
                base.move(eyeAimPos[0], eyeAimPos[1] + 0.005, eyeAimPos[2], upperLid)
                
                lowerLid = base.curve(p = [(0,0,0), (0.05 * self.sideMultiplier, -0.02, 0), (0.1 * self.sideMultiplier, -0.04,0), (0.15 * self.sideMultiplier, -0.02, 0), (0.2 * self.sideMultiplier,0,0)], n = "CV_"+side+"_LowerEyeLid")
                base.scale(0.1, 0.1, 0.1, lowerLid)
                base.move(eyeAimPos[0] - (0.004 * self.sideMultiplier), eyeAimPos[1] - 0.005, eyeAimPos[2], lowerLid)
                base.parent(lowerLid, "FACE_LOC")   
                sideMultiplier = -1
                               
        else:
            base.confirmDialog(title = "Eyes missing", message = "The eyes ( L_Eye - R_Eye ) could not be found", button = ['Ok'])       
            
    def MouthLocators(self, void):
        for side in self.sides:
            
            jawLoc = base.xform(base.ls("Loc_Jaw_End", type = 'transform'), q = True, t = True, ws = True)
            
            upperMouth = base.curve(p = [(0,0,0), (0.02 * self.sideMultiplier,-0.001, -0.001), (0.04 * self.sideMultiplier, -0.002,-0.002), (0.06 * self.sideMultiplier,-0.004,-0.003)], n = "CV_"+side+"_UpperMouth")
            base.scale(0.3, 0.3, 0.3, upperMouth)
            base.move(jawLoc[0], jawLoc[1] + 0.05, jawLoc[2]+0.02, upperMouth)
            base.parent(upperMouth, "FACE_LOC")
            
            lowerMouth = base.curve(p = [(0,0,0), (0.02 * self.sideMultiplier,0.001, -0.001), (0.04 * self.sideMultiplier, 0.002,-0.002), (0.06 * self.sideMultiplier,0.004,-0.003)], n = "CV_"+side+"_LowerMouth")
            base.scale(0.3, 0.3, 0.3, lowerMouth)
            base.move(jawLoc[0], jawLoc[1] + 0.03, jawLoc[2]+0.02, lowerMouth)
            base.parent(lowerMouth, "FACE_LOC")
            self.sideMultiplier = -1
            
            
    def EyeBrowLocators(self, void):
        self.sideMultiplier = 1
        for side in self.sides:

            eyeLocPos = base.xform(base.ls("Loc_"+side+"_EyeAim"), q = True, t = True, ws = True)
            
            eyeBrow = base.curve(p = [(0,0,0), (0.1 * self.sideMultiplier, 0.1, 0), (0.2 * self.sideMultiplier, 0.15, 0), (0.3 * self.sideMultiplier, 0.1,0)], n = "CV_"+side+"_EyeBrow")
            base.scale(0.1, 0.1, 0.1, eyeBrow)
            base.move(eyeLocPos[0] - (0.02 * self.sideMultiplier) , eyeLocPos[1] + 0.004, eyeLocPos[2] + 0.01, eyeBrow)
            base.parent(eyeBrow, "FACE_LOC")
        
            foreheadBrow = base.curve(p = [(0,0,0), (0.1 * self.sideMultiplier, 0.1, 0), (0.25 * self.sideMultiplier, 0.15, 0), (0.4 * self.sideMultiplier, 0.1,0)], n = "CV_"+side+"_ForeHeadBrow")
            base.scale(0.1, 0.1, 0.1, foreheadBrow)
            base.move(eyeLocPos[0] - (0.02 * self.sideMultiplier) , eyeLocPos[1] + 0.03, eyeLocPos[2] + 0.007, foreheadBrow)
            base.parent(foreheadBrow, "FACE_LOC")
        
            self.sideMultiplier = -1
            
            
    def SmileMuscles(self, void):
        self.sideMultiplier = 1
        for side in self.sides:
            jawLoc = base.xform(base.ls("Loc_Jaw_End", type = 'transform'), q = True, t = True, ws = True)
            smileMuscle = base.curve(p = [(0,0,0), (0.15 * self.sideMultiplier, -0.2, 0), (0.2 * self.sideMultiplier, -0.4, 0), (0.25 * self.sideMultiplier, -0.6,0)], n = "CV_"+side+"_SmileMuscle")
            base.scale(0.1, 0.1, 0.1, smileMuscle)
            base.move(jawLoc[0] + (0.01 * self.sideMultiplier), jawLoc[1] + 0.1, jawLoc[2] + 0.015, smileMuscle)
            base.parent(smileMuscle, "FACE_LOC")
        
            self.sideMultiplier = -1
            
   
    def AddLocators(self, void):
        allCurves = base.ls("CV_*")
        
        
        dummyLoc = base.spaceLocator(n = "Loc_Face_Head_Dummy")
        if (base.objExists("Loc_Neck_End")):
            neckPos = base.xform(base.ls("Loc_Neck_End", type = 'transform'), q = True, t = True, ws = True)
            base.scale(0.01, 0.01, 0.01, dummyLoc)
            base.move(neckPos[0], neckPos[1] + 0.02, neckPos[2] + 0.04, dummyLoc)                    
        else:
            base.confirmDialog(title = "Body First", message = "Create Body Locators First", button = ['Ok'])
        base.parent(dummyLoc, "FACE_LOC")
        
        for side in self.sides:
            cheekBone = base.spaceLocator(n = "Loc_Face_"+side+"_CheekLocator")
            eyePos = base.xform(base.ls("Loc_"+side+"_EyeAim", type = 'transform'), q = True, t = True, ws = True)
            base.scale(0.01, 0.01, 0.01, cheekBone)
            base.move(eyePos[0] + 0.007, eyePos[1] - 0.02, eyePos[2], cheekBone)
            base.parent(cheekBone, "FACE_LOC")
        
        
        for cv in allCurves:
            curveCV = base.ls(cv+".cv[0:]", fl = True)   
            for i, xCV in enumerate(curveCV):
                    
                tmpName = str(xCV).split("CV_")
                locName = tmpName[1].rsplit(".cv")[0]
                
                faceCluster = base.cluster(xCV, xCV, n = "Cluster_Face_"+locName+"_"+str(i))  
                
                if (xCV == "CV_R_UpperMouth.cv[0]" or xCV == "CV_R_LowerMouth.cv[0]"):
                    pass
                else:
                    faceLoc = base.spaceLocator(n = "Loc_Face_"+locName+"_"+str(i))
                    base.scale(0.004, 0.004, 0.004, faceLoc)
                    clusterPos = base.xform(xCV, q = True, t = True, ws = True)
                    base.move(clusterPos[0], clusterPos[1], clusterPos[2], faceLoc)
                    base.parent(faceLoc, "FACE_LOC")
                
                
                if(faceCluster[0] == "Cluster_Face_R_UpperMouth_0"):
                    base.parent(faceCluster[1], "Loc_Face_L_UpperMouth_0")
                elif(faceCluster[0] == "Cluster_Face_R_LowerMouth_0"):
                    base.parent(faceCluster[1], "Loc_Face_L_LowerMouth_0")
                else:            
                    base.parent(faceCluster[1], "Loc_Face_"+locName+"_"+str(i))  
                    
                                                      
    def MirrorLocators(self, void):
        l_loc = base.ls("Loc_Face_L_*", type = 'transform')
        r_loc = base.ls("Loc_Face_R_*", type = 'transform')

        leftLocators = []
        
        for i, x in enumerate(l_loc):
            
            if(x ==  "Loc_Face_L_UpperMouth_0" or x == "Loc_Face_L_LowerMouth_0"):
                pass
            else:    
                leftLocators.append(l_loc[i])
                
        for i, loc in enumerate(leftLocators):
            
            pos = base.xform(loc, q = True, t = True, ws = True)
            base.move(-pos[0], pos[1], pos[2], r_loc[i])
        
    def CreateJoints(self, void):
        allLocators = base.ls("Loc_Face_*", type = 'transform')
        
        for loc in allLocators:
            locPos = base.xform(loc, q = True, t = True, ws = True)
            if loc == "Loc_Face_Head_Dummy":
                base.select(deselect = True)
                base.joint(radius = 1, p = locPos, n = "FACERIG_Head_Dummy")
            
           
            else:
                base.select(deselect = True)
                base.joint(radius = 1, p = locPos, n = "FACERIG_"+str(loc).split("Loc_Face_")[1])
                
        
        if base.objExists("RIG_Neck_End"):
            base.parent("FACERIG_Head_Dummy", "RIG_Neck_End")
        
        sides = ['L', 'R']
        
        for side in sides:
            allEyeJoints = base.ls("FACERIG_"+side+"_*Lid_*")

            centerLocPos = base.xform(base.ls("FACERIG_"+side+"_EyeCenter"), q = True, t = True, ws = True)
            for eyeJoint in allEyeJoints:
         
                base.select(deselect = True)
                rotateJoint = base.joint(radius = 0.5, p = centerLocPos, n = str(eyeJoint)+"_rotateJoint")           
                base.parent(eyeJoint, rotateJoint)
                base.parent(rotateJoint, "FACERIG_"+side+"_EyeCenter")
               
            eyeAimRotate = base.joint(radius = 0.7, p = centerLocPos, n = "FACERIG_"+side+"_EyeAim.rotateJoint")
            
            base.parent("FACERIG_"+side+"_EyeAim", eyeAimRotate)
            base.parent(eyeAimRotate, "FACERIG_"+side+"_EyeCenter")
            base.parent("FACERIG_"+side+"_EyeCenter", "FACERIG_Head_Dummy")       
           
        
        allSmileJoints = base.ls("FACERIG_*_Smile*")
        allBrowJoints = base.ls("FACERIG_*_*Brow*")
        allMouthJoints = base.ls("FACERIG_*_*Mouth*")
        allCheekJoints = base.ls("FACERIG_*_*Cheek*")

        for mouth in allMouthJoints:
            base.select(deselect = True)
            base.parent(mouth, "FACERIG_Head_Dummy")
       
        
        for brow in allBrowJoints:
            base.select(deselect = True)
            base.parent(brow, "FACERIG_Head_Dummy")
       
        for cheek in allCheekJoints:
            base.select(deselect = True)
            base.parent(cheek, "FACERIG_Head_Dummy")        
       
        for smile in allSmileJoints:
            base.select(deselect = True)
            base.parent(smile, "FACERIG_Head_Dummy")


        base.select("FACERIG_Head_Dummy")
        base.joint(e = True, ch = True, oj = 'xyz', secondaryAxisOrient = 'xup')       
       
       
       
    def AddConstraints(self, void):
        sides = ['L', 'R']
        
        for side in sides:
            
            allEyeJoints = base.ls("FACERIG_"+side+"_*Lid_*")            
            
            rotators = []
            endJoint = []
    
            for jo in allEyeJoints:
                if "_rotateJoint" in jo:
                    rotators.append(jo)
                else:
                    endJoint.append(jo)
                    
            
            for i, ik in enumerate(endJoint):
                 base.ikHandle(n = "FACE_IK_"+str(ik), sj = rotators[i], ee = ik, sol = 'ikSCsolver')
                         
                    
    def AddControllers(self, void):
        sides = ['L', 'R']
    
    
        for side in sides:
            allJoints = base.ls("FACERIG_"+side+"_*")
            
            for jo in allJoints:
                jointPos = base.xform(jo, q = True, t = True, ws = True)
                ctrl = base.polyCylinder(r = 0.0015, h = 0.001, ax = [0,0,1], n = "FACE_CTRL_"+str(jo).split("FACERIG_")[1])
                base.move(jointPos[0], jointPos[1], jointPos[2] + 0.001, ctrl)
            
                if "Eye" in jo:
                    if "_rotateJoint" in jo:
                        pass
                    else:    
                        base.pointConstraint(ctrl, "FACE_IK_"+str(jo))
                else:
                    base.pointConstraint(ctrl, jo, mo = True)    
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
           