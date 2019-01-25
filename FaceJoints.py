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
        base.button(l = "Add Controllers", w = 200, c = self.AddConstraints)
        base.separator(st = 'none')
        
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
        
        base.group(em = True, n = "grpFACE_JOINTS")
        base.parent(base.ls("FACERIG_*"), "grpFACE_JOINTS")
       
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
            
            base.ikHandle(n = "FACE_IK_FACERIG_"+side+"_EyeAim", sj = "FACERIG_"+side+"_EyeAim_rotateJoint", ee = "FACERIG_"+side+"_EyeAim", sol = 'ikSCsolver')
        
        grpIK = base.group(em = True, n = "grpFACEIK")
        base.parent(base.ls("FACE_IK*"), "grpFACEIK")    
            
        self.AddControllers(self)                         
                    
    def AddControllers(self, void):
        
        sides = ['L', 'R']
        l_eyeCtrlPos = []
        r_eyeCtrlPos = []
        
        for side in sides:
            allJoints = base.ls("FACERIG_"+side+"_*")
            
            for jo in allJoints:
                ctrl = base.polyCylinder(r = 0.0015, h = 0.001, ax = [0,0,1], n = "FACE_CTRL_"+str(jo).split("FACERIG_")[1])
                ctrlGrp = base.group(em = True, n = "GRP_FACE_CTRL_"+str(jo).split("FACERIG_")[1])
                
                jointPos = base.xform(jo, q = True, t = True, ws = True)
                
                base.move(jointPos[0], jointPos[1], jointPos[2] + 0.001, ctrl)
                base.move(jointPos[0], jointPos[1], jointPos[2] + 0.001, ctrlGrp)
                base.parent(base.ls(ctrl, type = 'transform')[0], ctrlGrp)
                
                if "EyeLid" in jo:
                    if "_rotateJoint" in jo:
                        pass
                    else:
                        if "_L_" in jo:
                            l_eyeCtrlPos.append([(jointPos[0]), (jointPos[1]), (0.25)])    
                        else:
                            r_eyeCtrlPos.append([(jointPos[0]), (jointPos[1]), (0.25)])                                    
                        base.pointConstraint(ctrl, "FACE_IK_"+str(jo))    
                    
                   
            if (len(l_eyeCtrlPos) > 0 and not base.objExists("FACE_MAIN_CTRL_L_EYE_AIM")):                
                eyeCtrl = base.curve(p = [(l_eyeCtrlPos[0]), (l_eyeCtrlPos[1]), (l_eyeCtrlPos[2]), (l_eyeCtrlPos[3]), (l_eyeCtrlPos[4]), (l_eyeCtrlPos[9]), (l_eyeCtrlPos[8]), (l_eyeCtrlPos[7]), (l_eyeCtrlPos[6]), (l_eyeCtrlPos[5]), (l_eyeCtrlPos[0])], degree = 1, n = "FACE_MAIN_CTRL_L_EYE_AIM")    
                base.xform(eyeCtrl, cp = True)
            if (len(r_eyeCtrlPos) > 0):                    
                eyeCtrl = base.curve(p = [(r_eyeCtrlPos[0]), (r_eyeCtrlPos[1]), (r_eyeCtrlPos[2]), (r_eyeCtrlPos[3]), (r_eyeCtrlPos[4]), (r_eyeCtrlPos[9]), (r_eyeCtrlPos[8]), (r_eyeCtrlPos[7]), (r_eyeCtrlPos[6]), (r_eyeCtrlPos[5]), (r_eyeCtrlPos[0])], degree = 1, n = "FACE_MAIN_CTRL_R_EYE_AIM")    
                base.xform(eyeCtrl, cp = True)
                
            # mouth corner    
            upperCtrlPos1 = base.xform(base.ls("FACERIG_"+side+"_UpperMouth_3"), q = True, t = True, ws = True)            
            upperCtrlPos2 = base.xform(base.ls("FACERIG_"+side+"_SmileMuscle_2"), q = True, t = True, ws = True)
            upperMouthCtrl = base.polyCylinder(r = 0.003, h = 0.001, ax = [0,0,1], n = "FACE_MAIN_CTRL_"+side+"_MouthCorner")
            upperMouthDistance = [(upperCtrlPos2[0] - upperCtrlPos1[0]), (upperCtrlPos2[1] - upperCtrlPos1[1]),(upperCtrlPos2[2] - upperCtrlPos1[2])]
            base.move(upperCtrlPos1[0] + (upperMouthDistance[0] / 2), upperCtrlPos1[1] + (upperMouthDistance[1] / 2), upperCtrlPos1[2] + 0.003,upperMouthCtrl) 
            upperCtrlGrp = base.group(em = True, n = "GRP_FACE_CTRL_"+side+"_MouthCorner")
            base.move(upperCtrlPos1[0] + (upperMouthDistance[0] / 2), upperCtrlPos1[1] + (upperMouthDistance[1] / 2), upperCtrlPos1[2] + 0.003,upperCtrlGrp) 
            base.parent(base.ls(upperMouthCtrl, type = 'transform')[0], upperCtrlGrp)
            
            # cheek
            cheekCtrlPos1 = base.xform(base.ls("FACERIG_"+side+"_SmileMuscle_1"), q = True, t = True, ws = True)
            cheekCtrlPos2 = base.xform(base.ls("FACERIG_"+side+"_CheekLocator"), q = True, t = True, ws = True)
            upperCheekCtrl = base.polyCylinder(r = 0.003, h = 0.001, ax = [0,0,1], n = "FACE_MAIN_CTRL_"+side+"_UpperCheek") 
            cheekDistance = [(cheekCtrlPos2[0] - cheekCtrlPos1[0]), (cheekCtrlPos2[1] - cheekCtrlPos1[1]),(cheekCtrlPos2[2] - cheekCtrlPos1[2])] 
            base.move(cheekCtrlPos1[0] + (cheekDistance[0] / 2), cheekCtrlPos1[1] + (cheekDistance[1] / 2), cheekCtrlPos1[2] + cheekDistance[2] + 0.003, upperCheekCtrl) 
            upperCheekCtrlGRP = base.group(em = True, n = "GRP_FACE_CTRL_"+side+"_UpperCheek")
            base.move(cheekCtrlPos1[0] + (cheekDistance[0] / 2), cheekCtrlPos1[1] + (cheekDistance[1] / 2), cheekCtrlPos1[2] + cheekDistance[2] + 0.003, upperCheekCtrlGRP) 
            base.parent(base.ls(upperCheekCtrl, type = 'transform'), upperCheekCtrlGRP) 
            
            # eyebrow
            upperEyeBrowCtrlPos1 = base.xform(base.ls("FACERIG_"+side+"_EyeBrow_0"), q = True, t = True, ws = True)
            upperEyeBrowCtrlPos2 = base.xform(base.ls("FACERIG_"+side+"_EyeBrow_1"), q = True, t = True, ws = True)            
            upperEyeBrowDistance = [(upperEyeBrowCtrlPos2[0] - upperEyeBrowCtrlPos1[0]), (upperEyeBrowCtrlPos2[1] - upperEyeBrowCtrlPos1[1]),(upperEyeBrowCtrlPos2[2] - upperEyeBrowCtrlPos1[2])]     
            upperEyeBrownCtrl = base.polyCylinder(r = 0.003, h = 0.001, ax = [0,0,1], n = "FACE_MAIN_CTRL_"+side+"_UpperEyeBrow_1")            
            base.move(upperEyeBrowCtrlPos1[0] + (upperEyeBrowDistance[0] / 2), upperEyeBrowCtrlPos1[1] + (upperEyeBrowDistance[1] / 2), upperEyeBrowCtrlPos1[2] + upperEyeBrowDistance[2] + 0.003, upperEyeBrownCtrl)  
            base.makeIdentity(upperEyeBrownCtrl, apply = True, t = 1, r = 1, s = 1)
            
            upperEyeBrowCtrlGRP = base.group(em = True, n = "GRP_FACE_CTRL_"+side+"_UpperEyeBrow_1")
            base.parent(base.ls(upperEyeBrownCtrl, type = 'transform'), upperEyeBrowCtrlGRP) 
            
            upperEyeBrowCenterCtrlPos1 = base.xform(base.ls("FACERIG_"+side+"_EyeBrow_1"), q = True, t = True, ws = True)
            upperEyeBrowCenterCtrlPos2 = base.xform(base.ls("FACERIG_"+side+"_EyeBrow_2"), q = True, t = True, ws = True)            
            upperEyeBrowCenterDistance = [(upperEyeBrowCenterCtrlPos2[0] - upperEyeBrowCenterCtrlPos1[0]), (upperEyeBrowCenterCtrlPos2[1] - upperEyeBrowCenterCtrlPos1[1]),(upperEyeBrowCenterCtrlPos2[2] - upperEyeBrowCenterCtrlPos1[2])]     
            upperEyeBrownCenterCtrl = base.polyCylinder(r = 0.003, h = 0.001, ax = [0,0,1], n = "FACE_MAIN_CTRL_"+side+"_UpperEyeBrow_2")            
            base.move(upperEyeBrowCenterCtrlPos1[0] + (upperEyeBrowCenterDistance[0] / 2), upperEyeBrowCenterCtrlPos1[1] + (upperEyeBrowCenterDistance[1] / 2), upperEyeBrowCenterCtrlPos1[2] + upperEyeBrowCenterDistance[2] + 0.003, upperEyeBrownCenterCtrl)  
            base.makeIdentity(upperEyeBrownCenterCtrl, apply = True, t = 1, r = 1, s = 1)
        
        mainEyeCtrl = base.curve(p = [(r_eyeCtrlPos[4][0] - 0.01, r_eyeCtrlPos[6][1] -0.02, 0.25), (r_eyeCtrlPos[4][0] - 0.01, r_eyeCtrlPos[3][1] + 0.02, 0.25), (l_eyeCtrlPos[4][0] + 0.01, l_eyeCtrlPos[3][1] + 0.02, 0.25), (l_eyeCtrlPos[4][0] + 0.01, l_eyeCtrlPos[3][1] - 0.01, 0.25), (r_eyeCtrlPos[4][0] - 0.01, r_eyeCtrlPos[6][1] -0.02, 0.25)], degree = 1, n = "FACE_MAIN_CTRL_PARENT_EYES")
        base.xform(mainEyeCtrl, cp = True)
        
        faceCtrl = base.curve(p = [(0,0,0), (0, 0.1, 0), (0.1, 0.1, 0), (0.1, 0.2, 0), (0, 0.2, 0), (0, 0.3, 0), (-0.1, 0.3, 0), (-0.1, 0.2,0), (-0.2,0.2, 0), (-0.2, 0.1,0), (-0.1, 0.1,0), (-0.1, 0,0), (0,0,0)], degree = 1, name = "MASTER_FACE_CTRL")
        base.addAttr(shortName = "SC", longName = "Show_Secondary", attributeType = 'enum', en = 'False:True', keyable = True)
        base.xform(faceCtrl, cp = True) 
    
        base.scale(0.3,0.3, 0.3, faceCtrl)
        
        headLocPos = base.xform(base.ls("Loc_Head"), q = True, t = True, ws = True)
        base.move(headLocPos[0] + 0.05, headLocPos[1] + 0.04, headLocPos[2], faceCtrl)   
        base.makeIdentity(faceCtrl, apply = True, t = 1, r = 1, s = 1)
    
    
        self.AddUtilities(self)
        
    def AddUtilities(self, void):
        
        allCtrlGrps = base.ls("GRP_FACE_CTRL_*")
        base.parent(allCtrlGrps, "MASTER_FACE_CTRL")
        
        base.connectAttr("FACE_MAIN_CTRL_PARENT_EYES.translate", "FACE_MAIN_CTRL_L_EYE_AIM.translate")
        base.connectAttr("FACE_MAIN_CTRL_PARENT_EYES.translate", "FACE_MAIN_CTRL_R_EYE_AIM.translate")        
           
    
        for i, grp in enumerate(allCtrlGrps):
            base.makeIdentity(grp, apply = True, t = 1, r = 1, s = 1)
            
            multDiv = base.shadingNode("multiplyDivide", asUtility = True, n = "Face_Node_"+str(i))
            unitConv1 = base.shadingNode("unitConversion", asUtility = True, n = "Face_Node_UnitConversionIn_"+str(i))
            unitConv2 = base.shadingNode("unitConversion", asUtility = True, n = "Face_Node_UnitConversionOut_"+str(i))
            base.setAttr(multDiv+".operation", 1)            
            
            if "UpperEyeLid" in grp:
                if "0" in grp:
                    base.setAttr(multDiv+".input2X", 0.001)
                    base.setAttr(multDiv+".input2Y", 0.01)
                    base.setAttr(multDiv+".input2Z", 0)
                elif "1" in grp:
                    base.setAttr(multDiv+".input2X", 0.002)
                    base.setAttr(multDiv+".input2Y", 0.035)
                    base.setAttr(multDiv+".input2Z", 0)                                    
                    
                elif "2" in grp:
                    base.setAttr(multDiv+".input2X", 0.005)
                    base.setAttr(multDiv+".input2Y", 0.05)
                    base.setAttr(multDiv+".input2Z", 0)                      

                elif "3" in grp:
                    base.setAttr(multDiv+".input2X", 0.0015)
                    base.setAttr(multDiv+".input2Y", 0.03)
                    base.setAttr(multDiv+".input2Z", 0)  
                else:
                    base.setAttr(multDiv+".input2X", 0.001)
                    base.setAttr(multDiv+".input2Y", 0.01)
                    base.setAttr(multDiv+".input2Z", 0)                      
                        
                if "_L_" in grp:
                    base.connectAttr("FACE_MAIN_CTRL_L_EYE_AIM.translate", unitConv1+".input")
                else:
                    base.connectAttr("FACE_MAIN_CTRL_R_EYE_AIM.translate", unitConv1+".input")
                
                base.connectAttr(unitConv1+".output", multDiv+".input1")
                base.connectAttr(multDiv+".output", unitConv2+".input")
                base.connectAttr(unitConv2+".output", grp+".translate")
            
            if "LowerEyeLid" in grp:
                if "0" in grp:
                    base.setAttr(multDiv+".input2X", 0.001)
                    base.setAttr(multDiv+".input2Y", 0.005)
                    base.setAttr(multDiv+".input2Z", 0)
                elif "1" in grp:
                    base.setAttr(multDiv+".input2X", 0.002)
                    base.setAttr(multDiv+".input2Y", 0.0125)
                    base.setAttr(multDiv+".input2Z", 0)                                    
                    
                elif "2" in grp:
                    base.setAttr(multDiv+".input2X", 0.005)
                    base.setAttr(multDiv+".input2Y", 0.02)
                    base.setAttr(multDiv+".input2Z", 0)                      

                elif "3" in grp:
                    base.setAttr(multDiv+".input2X", 0.0015)
                    base.setAttr(multDiv+".input2Y", 0.01)
                    base.setAttr(multDiv+".input2Z", 0)  
                else:
                    base.setAttr(multDiv+".input2X", 0.001)
                    base.setAttr(multDiv+".input2Y", 0.005)
                    base.setAttr(multDiv+".input2Z", 0)                      
                        
                if "_L_" in grp:
                    base.connectAttr("FACE_MAIN_CTRL_L_EYE_AIM.translate", unitConv1+".input")
                else:
                    base.connectAttr("FACE_MAIN_CTRL_R_EYE_AIM.translate", unitConv1+".input")
                
                base.connectAttr(unitConv1+".output", multDiv+".input1")
                base.connectAttr(multDiv+".output", unitConv2+".input")
                base.connectAttr(unitConv2+".output", grp+".translate")
                
                
            if "EyeAim" in grp:
                base.setAttr(multDiv+".input2X", 0.1)
                base.setAttr(multDiv+".input2Y", 0.1)
                base.setAttr(multDiv+".input2Z", 0.1)
                
                if "_L_" in grp:
                    base.connectAttr("FACE_MAIN_CTRL_L_EYE_AIM.translate", unitConv1+".input")
                else:
                    base.connectAttr("FACE_MAIN_CTRL_R_EYE_AIM.translate", unitConv1+".input")
                
                base.connectAttr(unitConv1+".output", multDiv+".input1")
                base.connectAttr(multDiv+".output", unitConv2+".input")
                base.connectAttr(unitConv2+".output", grp+".translate")
                    
            if "Brow" in grp:
                if "ForeHead" in grp:
                    if "0" in grp:
                        base.setAttr(multDiv+".input2X", 0.2)
                        base.setAttr(multDiv+".input2Y", 0.2)
                        base.setAttr(multDiv+".input2Z", 0.2)                        
                        
                        if "_L_" in grp:
                            base.connectAttr("FACE_MAIN_CTRL_L_UpperEyeBrow_1.translate", unitConv1+".input")
                        else:
                            base.connectAttr("FACE_MAIN_CTRL_R_UpperEyeBrow_1.translate", unitConv1+".input")                                
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                    elif "1" in grp:
                        base.setAttr(multDiv+".input2X", 0.15)
                        base.setAttr(multDiv+".input2Y", 0.15)
                        base.setAttr(multDiv+".input2Z", 0.15)                        
                        
                        if "_L_" in grp:
                            base.connectAttr("FACE_MAIN_CTRL_L_UpperEyeBrow_1.translate", unitConv1+".input")
                        else:
                            base.connectAttr("FACE_MAIN_CTRL_R_UpperEyeBrow_1.translate", unitConv1+".input")                                
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                        
                    elif "2" in grp:
                        base.setAttr(multDiv+".input2X", 0.2)
                        base.setAttr(multDiv+".input2Y", 0.2)
                        base.setAttr(multDiv+".input2Z", 0.2)                        
                        
                        if "_L_" in grp:
                            base.connectAttr("FACE_MAIN_CTRL_L_UpperEyeBrow_2.translate", unitConv1+".input")
                        else:
                            base.connectAttr("FACE_MAIN_CTRL_R_UpperEyeBrow_2.translate", unitConv1+".input")                                
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                        
                    else:
                        base.setAttr(multDiv+".input2X", 0.1)
                        base.setAttr(multDiv+".input2Y", 0.1)
                        base.setAttr(multDiv+".input2Z", 0.1)                        
                        
                        if "_L_" in grp:
                            base.connectAttr("FACE_MAIN_CTRL_L_UpperEyeBrow_2.translate", unitConv1+".input")
                        else:
                            base.connectAttr("FACE_MAIN_CTRL_R_UpperEyeBrow_2.translate", unitConv1+".input")                                
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                else:
                    if "0" in grp:
                        base.setAttr(multDiv+".input2X", 0.8)
                        base.setAttr(multDiv+".input2Y", 0.8)
                        base.setAttr(multDiv+".input2Z", 0.8)                        
                        
                        if "_L_" in grp:
                            base.connectAttr("FACE_MAIN_CTRL_L_UpperEyeBrow_1.translate", unitConv1+".input")
                        else:
                            base.connectAttr("FACE_MAIN_CTRL_R_UpperEyeBrow_1.translate", unitConv1+".input")                                
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                    elif "1" in grp:
                        base.setAttr(multDiv+".input2X", 0.6)
                        base.setAttr(multDiv+".input2Y", 0.6)
                        base.setAttr(multDiv+".input2Z", 0.6)                        
                        
                        if "_L_" in grp:
                            base.connectAttr("FACE_MAIN_CTRL_L_UpperEyeBrow_1.translate", unitConv1+".input")
                        else:
                            base.connectAttr("FACE_MAIN_CTRL_R_UpperEyeBrow_1.translate", unitConv1+".input")                                
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                        
                    elif "2" in grp:
                        base.setAttr(multDiv+".input2X", 0.6)
                        base.setAttr(multDiv+".input2Y", 0.6)
                        base.setAttr(multDiv+".input2Z", 0.6)                        
                        
                        if "_L_" in grp:
                            base.connectAttr("FACE_MAIN_CTRL_L_UpperEyeBrow_2.translate", unitConv1+".input")
                        else:
                            base.connectAttr("FACE_MAIN_CTRL_R_UpperEyeBrow_2.translate", unitConv1+".input")                                
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                        
                    else:
                        base.setAttr(multDiv+".input2X", 0.3)
                        base.setAttr(multDiv+".input2Y", 0.3)
                        base.setAttr(multDiv+".input2Z", 0.3)                        
                        
                        if "_L_" in grp:
                            base.connectAttr("FACE_MAIN_CTRL_L_UpperEyeBrow_2.translate", unitConv1+".input")
                        else:
                            base.connectAttr("FACE_MAIN_CTRL_R_UpperEyeBrow_2.translate", unitConv1+".input")                                
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")                                     
            
            if "Cheek" in grp:
                if "Upper" in grp:
                    if "_L_" in grp:
                        base.setAttr(multDiv+".input2X", 0.15)
                        base.setAttr(multDiv+".input2Y", 0.15)
                        base.setAttr(multDiv+".input2Z", 0.15)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_L_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate") 
                    else:
                        base.setAttr(multDiv+".input2X", 0.15)
                        base.setAttr(multDiv+".input2Y", 0.15)
                        base.setAttr(multDiv+".input2Z", 0.15)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_R_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")     
                else:
                    if "_L_" in grp:
                        base.setAttr(multDiv+".input2X", 0.5)
                        base.setAttr(multDiv+".input2Y", 0.5)
                        base.setAttr(multDiv+".input2Z", 0.5)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_L_UpperCheek.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate") 
                    else:
                        base.setAttr(multDiv+".input2X", 0.5)
                        base.setAttr(multDiv+".input2Y", 0.5)
                        base.setAttr(multDiv+".input2Z", 0.5)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_R_UpperCheek.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                    
            if "Smile" in grp:
                if "_L_" in grp:
                    if "0" in grp:
                        base.setAttr(multDiv+".input2X", 0.15)
                        base.setAttr(multDiv+".input2Y", 0.15)
                        base.setAttr(multDiv+".input2Z", 0.15)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_L_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                    elif "1" in grp:
                        base.setAttr(multDiv+".input2X", 0.4)
                        base.setAttr(multDiv+".input2Y", 0.4)
                        base.setAttr(multDiv+".input2Z", 0.4)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_L_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                    
                    elif "2" in grp:
                        base.setAttr(multDiv+".input2X", 0.7)
                        base.setAttr(multDiv+".input2Y", 0.7)
                        base.setAttr(multDiv+".input2Z", 0.7)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_L_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                        

                    else:
                        base.setAttr(multDiv+".input2X", 0.35)
                        base.setAttr(multDiv+".input2Y", 0.35)
                        base.setAttr(multDiv+".input2Z", 0.35)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_L_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")    
                if "_R_" in grp:
                    if "0" in grp:
                        base.setAttr(multDiv+".input2X", 0.15)
                        base.setAttr(multDiv+".input2Y", 0.15)
                        base.setAttr(multDiv+".input2Z", 0.15)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_R_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                    elif "1" in grp:
                        base.setAttr(multDiv+".input2X", 0.4)
                        base.setAttr(multDiv+".input2Y", 0.4)
                        base.setAttr(multDiv+".input2Z", 0.4)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_R_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                    
                    elif "2" in grp:
                        base.setAttr(multDiv+".input2X", 0.7)
                        base.setAttr(multDiv+".input2Y", 0.7)
                        base.setAttr(multDiv+".input2Z", 0.7)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_R_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                        

                    else:
                        base.setAttr(multDiv+".input2X", 0.35)
                        base.setAttr(multDiv+".input2Y", 0.35)
                        base.setAttr(multDiv+".input2Z", 0.35)                        
                    
                        base.connectAttr("FACE_MAIN_CTRL_R_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate") 
            if "Mouth" in grp:
                if "MouthCorner" in grp:
                    pass
                else:
                    grpValue = str(allCtrlGrps[i]).split("Mouth_")
                    base.setAttr(multDiv+".input2X", float(grpValue[1]) * 0.3)    
                    base.setAttr(multDiv+".input2Y", float(grpValue[1]) * 0.3)
                    base.setAttr(multDiv+".input2Z", float(grpValue[1]) * 0.3)                        
    
                    if "_L_" in grp:
                        base.connectAttr("FACE_MAIN_CTRL_L_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
                        
                        
                    else:
                        base.connectAttr("FACE_MAIN_CTRL_R_MouthCorner.translate", unitConv1+".input")
                        base.connectAttr(unitConv1+".output", multDiv+".input1")
                        base.connectAttr(multDiv+".output", unitConv2+".input")
                        base.connectAttr(unitConv2+".output", grp+".translate")
        
        
        allCtrls = base.ls("FACE_CTRL_*", type = 'transform')
        allJoints = base.ls("FACERIG_*", type = 'joint')
        
        
        ctrlGrps = []
        jointFiltered = []
        
        for ctrl in allCtrls:
            base.connectAttr("MASTER_FACE_CTRL.Show_Secondary", ctrl+".visibility")
        
            if "_rotateJoint" in ctrl:
                pass
            elif "EyeLid" in ctrl:
                pass
            elif "EyeAim" in ctrl:
                pass
            else:
                ctrlGrps.append(ctrl)
        
        for j in allJoints:
            if "_rotateJoint" in j:
                pass
            elif "Head_Dummy" in j:
                pass
            elif "EyeLid" in j:
                pass
            elif "EyeAim" in j:
                pass
            else:
                jointFiltered.append(j)
                
                
        for i, grps in enumerate(ctrlGrps):
            base.pointConstraint(grps, jointFiltered[i], mo = True)                        
            
            
            
            
            
            
        
        
        
        
        
        
        
        
        
        
    
    
                 