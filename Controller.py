import maya.cmds as base
import maya.OpenMaya as om


def CreateController(spineCount, fingerCount):
    #arrow = base.curve(p = [(1,0,0),(1,0,2), (2,0,2),(0,0,6), (-2,0,2), (-1,0,2), (-1,0,0), (1,0,0)], degree = 1)
    CreateMaster()
    CreatePelvis()
    CreateWrists()

    CreateFeet()
    CreateSpines(spineCount)
    CreateClavicles(spineCount)
    CreateNeck(spineCount)
    CreateHead()
    if (base.objExists("RIG_BREATHING_START")):
        CreateBreathing(spineCount)
        
    CreateFingers(fingerCount)
    setColors()
    
def CreateMaster():
    ## master
    master_ctrl = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 16, name = "MASTER_CONTROLLER")
    selection = base.select("MASTER_CONTROLLER.cv[1]","MASTER_CONTROLLER.cv[3]","MASTER_CONTROLLER.cv[5]","MASTER_CONTROLLER.cv[7]","MASTER_CONTROLLER.cv[9]","MASTER_CONTROLLER.cv[11]","MASTER_CONTROLLER.cv[13]","MASTER_CONTROLLER.cv[15]")
    base.scale(0.7, 0.7, 0.7, selection)
    base.scale(1, 1, 1, master_ctrl)

    base.makeIdentity(master_ctrl, apply = True, t = 1, r = 1, s = 1)
    
def CreatePelvis():
    ## pelvis
    pelvis_ctrl = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 8, name = "CTRL_PELVIS")
    rootPos = base.xform(base.ls("RIG_ROOT", type = 'joint'), q = True, t = True, ws = True)
    base.move(rootPos[0],rootPos[1],rootPos[2], pelvis_ctrl) 
    base.scale(0.3, 0.3, 0.3, pelvis_ctrl)   
    base.makeIdentity(pelvis_ctrl, apply = True, t = 1, r = 1, s = 1)  
    base.parent(pelvis_ctrl, "MASTER_CONTROLLER")       
    
def CreateWrists():    
    sides = ['L', 'R']
    
    for side in sides:
        ctrl1 = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 16, name = "CTRL_"+side+ "_Wrist0")
        ctrl2 = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 16, name = "CTRL_"+side+ "_Wrist1")
        ctrl3 = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 16, name = "CTRL_"+side+ "_Wrist2")                
    
        wrist_ctrl = base.group(em = True, name ="CTRL_"+side+"_Wrist")
        curves = [ctrl1, ctrl2, ctrl3]
        for cv in curves:
            crvShape = base.listRelatives(cv, shapes = True)
            base.parent(crvShape, wrist_ctrl, s = True, r = True)
            base.delete(cv)
        base.select("CTRL_"+side+"_Wrist")    
        base.addAttr(shortName = "PV", longName = "Elbow_PV", attributeType = 'double', defaultValue = 0, minValue = -100, maxValue = 100, keyable = True)
        base.scale(0.07, 0.07, 0.07, wrist_ctrl)
        
        
        wristPos = base.xform(base.ls("RIG_"+side+"_Wrist"), q = True, t = True, ws = True)
        wristRot = base.joint(base.ls("RIG_"+side+"_Wrist"), q = True, o = True)
        if base.objExists("RIG_L_ArmTwist_*"):
            armTwists = base.ls("RIG_L_ArmTwist_*")
            print base.xform(base.ls("RIG_"+side+"_ArmTwist_"+str(len(armTwists) - 1)), q = True, ws = True, ro = True)
            wristRotation = base.xform(base.ls("RIG_"+side+"_ArmTwist_"+str(len(armTwists) - 1)), q = True, ws = True, ro = True)
        else:
            wristRotation = base.xform(base.ls("RIG_"+side+"_Elbow"), q = True, ws = True, ro = True)
        base.move(wristPos[0], wristPos[1], wristPos[2], wrist_ctrl)
        wristGrp = base.group(em = True, name = 'CTRL_GRP_'+side+'_Wrist')
        base.move(wristPos[0],wristPos[1],wristPos[2], wristGrp)
        base.parent(wrist_ctrl, wristGrp)
       # base.parent(wrist_ctrl, world = True)
       
        base.rotate(0,0, -wristRotation[2], wristGrp)
        base.parent(wristGrp, "MASTER_CONTROLLER")
    
def CreateClavicles(spineCount):
    l_clavicle = base.curve(p = [(1,0,0),(1,1,1), (1,1.5,2), (1,1.7,3), (1,1.5,4), (1,1,5), (1,0,6), (-1, 0,6), (-1,1,5), (-1,1.5,4), (-1,1.7,3), (-1,1.5,2), (-1,1,1), (-1,0,0) ], degree = 1, name = "CTRL_L_Clavicle")
    r_clavicle = base.curve(p = [(1,0,0),(1,1,1), (1,1.5,2), (1,1.7,3), (1,1.5,4), (1,1,5), (1,0,6), (-1, 0,6), (-1,1,5), (-1,1.5,4), (-1,1.7,3), (-1,1.5,2), (-1,1,1), (-1,0,0) ], degree = 1, name = "CTRL_R_Clavicle")
    
    base.scale(0.02, 0.02, 0.02, l_clavicle)    
    base.scale(0.02, 0.02, 0.02, r_clavicle)  
    
    l_ArmPos = base.xform(base.ls("RIG_L_UpperArm"), q = True, t = True, ws = True)  
    r_ArmPos = base.xform(base.ls("RIG_R_UpperArm"), q = True, t = True, ws = True)
    
    l_claviclePos = base.xform(base.ls("RIG_L_Clavicle"), q = True, t = True, ws = True)
    r_claviclePos = base.xform(base.ls("RIG_R_Clavicle"), q = True, t = True, ws = True)
    
    base.move(l_ArmPos[0], l_ArmPos[1] + 0.125, l_ArmPos[2] - 0.1, l_clavicle)
    base.move(r_ArmPos[0], r_ArmPos[1] + 0.125, r_ArmPos[2] - 0.1, r_clavicle)
    
    base.move(l_claviclePos[0],l_claviclePos[1],l_claviclePos[2], l_clavicle+".scalePivot", l_clavicle+".rotatePivot")    
    base.move(r_claviclePos[0],r_claviclePos[1],r_claviclePos[2], r_clavicle+".scalePivot", r_clavicle+".rotatePivot") 

    base.makeIdentity(l_clavicle, apply = True, t = 1, r = 1, s = 1)
    base.makeIdentity(r_clavicle, apply = True, t = 1, r = 1, s = 1)
    
    base.parent(l_clavicle, "CTRL_SPINE_"+str(spineCount - 1))
    base.parent(r_clavicle, "CTRL_SPINE_"+str(spineCount - 1))

def CreateSpines(spineCount):
    
    for i in range(0, spineCount):
        spinePos = base.xform(base.ls("RIG_SPINE_"+str(i)), q = True, t = True, ws = True)
        spine = base.curve(p =[(0, spinePos[1], spinePos[2]), (0, spinePos[1], spinePos[2] - 1), (0, spinePos[1] + 0.1, spinePos[2] - 1.1), (0, spinePos[1] + 0.1, spinePos[2] - 1.4), (0, spinePos[1] - 0.1, spinePos[2] - 1.4), (0, spinePos[1] - 0.1, spinePos[2] - 1.1), (0, spinePos[1], spinePos[2] - 1)], degree = 1, name = "CTRL_SPINE_"+str(i))
        base.move(spinePos[0], spinePos[1], spinePos[2], spine+".scalePivot", spine+".rotatePivot")
        base.scale(0.5, 0.5, 0.5, spine)
        if (i == 0):
            base.parent(spine, "CTRL_PELVIS")
        else:
            base.parent(spine, "CTRL_SPINE_"+str(i-1))    
      
def CreateNeck(spineCount):
    neck = base.curve(p = [(0.5,0,0), (0.25, -0.25, -0.5), (-0.25, -0.25, -0.5), (-0.5,0,0), (-0.25, -0.25, 0.5), (0.25, -0.25, 0.5), (0.5, 0,0)], degree = 1, name = "CTRL_NECK")
    neckPos = base.xform(base.ls("RIG_Neck_Start"), q = True, t = True, ws = True)
    base.scale(0.3, 0.3, 0.3, neck)
    base.move(neckPos[0], neckPos[1]+0.1, neckPos[2], neck)
    base.move(neckPos[0], neckPos[1], neckPos[2], neck+".scalePivot", neck+".rotatePivot")
    base.parent(neck, "CTRL_SPINE_"+str(spineCount-1))
    
    base.makeIdentity(neck, apply = True, t = 1, r = 1, s = 1)

def CreateBreathing(spineCount):

    breathing = base.curve(p = [(0,0,0),(0.1, 0.1, 0), (0, 0.2,0), (-0.1, 0.1,0), (0,0,0)], degree = 1, name = "CTRL_BREATHING")
    base.move(0, 0.1, 0, breathing+".scalePivot", breathing+".rotatePivot")
    base.scale(0.3, 0.3, 0.3, breathing)
    breathingPos = base.xform(base.ls("RIG_BREATHING_END"), q = True, t = True, ws = True)
    breathingStart = base.xform(base.ls("RIG_BREATHING_START"), q = True, t = True, ws = True)
    base.move(breathingPos[0], breathingPos[1] - 0.1, breathingPos[2] + 0.1, breathing)
    base.move(breathingStart[0], breathingStart[1], breathingStart[2], breathing+".scalePivot", breathing+".rotatePivot")
    base.parent(breathing, "CTRL_SPINE_"+str(spineCount - 1))
    base.makeIdentity(breathing, apply = True, t = 1, r = 1, s = 1)   
 
def CreateHead():    
    head = base.curve(p = [(0.5,0,0), (0.25,-0.25,-0.5), (0.25,-0.5, -0.5), (0,-0.6,-0.5),(-0.25,-0.5,-0.5), (-0.25, -0.25, -0.5), (-0.5,0,0), (-0.25, -0.25, 0.5), (-0.25, -0.5, 0.5), (0,-0.6, 0.5) ,(0.25, -0.5, 0.5),(0.25, -0.25, 0.5), (0.5,0,0)], degree = 1, name = "CTRL_HEAD")
    base.scale(0.3, 0.3, 0.3, head)
    headPos = base.xform(base.ls("RIG_Head"), q= True, t = True, ws = True)
    neckPos = base.xform(base.ls("RIG_Neck_End"), q = True, t = True, ws = True)
    base.move(headPos[0], headPos[1], headPos[2], head)
    base.move(neckPos[0], neckPos[1], neckPos[2], head+".scalePivot", head+".rotatePivot")    
    base.parent(head, "CTRL_NECK")
    base.makeIdentity(head, apply = True, t = 1, r = 1, s = 1)    
    
    #jaw
    jaw = base.curve(p = [(0,0,0),(0.1, 0.1, 0), (0, 0.2,0), (-0.1, 0.1,0), (0,0,0)], degree = 1, name = "CTRL_JAW")
    base.move(0, 0.1, 0, jaw+".scalePivot", jaw+".rotatePivot")
    base.scale(0.3, 0.3, 0.3, jaw)
    jawPos = base.xform(base.ls("RIG_Jaw_End"), q = True, t = True, ws = True)
    jawStart = base.xform(base.ls("RIG_Jaw_Start"), q = True, t = True, ws = True)
    base.move(jawPos[0], jawPos[1] - 0.1, jawPos[2] + 0.1, jaw)
    base.move(jawStart[0], jawStart[1], jawStart[2], jaw+".scalePivot", jaw+".rotatePivot")
    base.parent(jaw, "CTRL_HEAD")
    base.makeIdentity(jaw, apply = True, t = 1, r = 1, s = 1)    
    
        
def CreateFeet():
    l_arrow = base.curve(p = [(1,0,0),(1,0,2), (2,0,2),(0,0,6), (-2,0,2), (-1,0,2), (-1,0,0), (1,0,0)], degree = 1, name = "CTRL_L_Foot")
    base.addAttr(shortName = "KF", longName = "Knee_Twist", attributeType = 'double', defaultValue = 0, minValue = -100, maxValue = 100, keyable = True)            
    base.addAttr(shortName = "KR", longName = "Knee_Fix", attributeType = 'double', defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)            
    base.addAttr(shortName = "FR", longName = "Foot_Roll", attributeType = 'double', defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)            
    base.addAttr(shortName = "BR", longName = "Ball_Roll", attributeType = 'double', defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)            


    r_arrow = base.curve(p = [(1,0,0),(1,0,2), (2,0,2),(0,0,6), (-2,0,2), (-1,0,2), (-1,0,0), (1,0,0)], degree = 1, name = "CTRL_R_Foot")
    base.addAttr(shortName = "KF", longName = "Knee_Twist", attributeType = 'double', defaultValue = 0, minValue = -100, maxValue = 100, keyable = True)            
    base.addAttr(shortName = "KR", longName = "Knee_Fix", attributeType = 'double', defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)            
    base.addAttr(shortName = "FR", longName = "Foot_Roll", attributeType = 'double', defaultValue = 0, minValue = 0, maxValue = 100, keyable = True) 
    base.addAttr(shortName = "BR", longName = "Ball_Roll", attributeType = 'double', defaultValue = 0, minValue = 0, maxValue = 100, keyable = True)                           
  
    
    base.scale(0.08, 0.08, 0.08, l_arrow)
    base.scale(0.08, 0.08, 0.08, r_arrow)
        
    l_footPos = base.xform(base.ls("RIG_L_Foot"), q = True, t = True, ws = True)
    r_footPos = base.xform(base.ls("RIG_R_Foot"), q = True, t = True, ws = True)  
        
    base.move(l_footPos[0], 0, l_footPos[2], l_arrow)
    base.move(r_footPos[0], 0, r_footPos[2], r_arrow)    
    
    base.makeIdentity(l_arrow, apply = True, t = 1, r = 1, s = 1)        
    base.makeIdentity(r_arrow, apply = True, t = 1, r = 1, s = 1) 
        
    base.parent(l_arrow, "MASTER_CONTROLLER")
    base.parent(r_arrow, "MASTER_CONTROLLER")    
 
def CreateFingers(fingerCount):
    sides = ['L', 'R']
    
    for side in sides:
        for i in range(0, fingerCount):
            
            #base.move(fingerPosition[0], fingerPosition[1], fingerPosition[2], fingerGrp)
            #base.makeIdentity(fingerGrp, apply = True, t = 1, r = 1, s = 1) 
            #print fingerRotation
            for j in range(0,3):
                #fingerRotation = base.xform(base.ls("RIG_"+side+"_Finger_"+str(i)+"_"+str(j)), q = True, ws = True, ro = True)
                fingerRotation = base.xform(base.ls("Loc_"+side+"_Finger_"+str(i)+"_"+str(j)), q = True, ws = True, ro = True)
                fingerPosition = base.xform(base.ls("Loc_"+side+"_Finger_"+str(i)+"_"+str(j)), q = True, ws = True, t = True)
            
                allFingers =  base.ls("RIG_"+side+"_Finger_"+str(i)+"_"+str(j))   
        
                finger = base.curve(p =[(0,0,0), (0,0,0.5), (0.2, 0, 0.7),(0,0,0.9), (-0.2, 0, 0.7), (0,0,0.5)], degree = 1, name = "CTRL_"+side+"_Finger_"+str(i)+"_"+str(j))
                base.rotate(-90,0,0, finger)
                           
                #base.parent(finger, fingerGrp)
                for k, fi in enumerate(allFingers):
                    fingerPos = base.xform(fi, q = True, t = True, ws = True)
                    fingerRot = base.joint(fi, q = True, o = True)
                    base.scale(0.1, 0.1, 0.1, finger)    
                    base.move(fingerPos[0], fingerPos[1], fingerPos[2], finger)
                fingerGrp = base.group(em = True, n = "CTRL_GRP_"+side+"_Finger_"+str(i)+"_"+str(j))
                base.move(fingerPosition[0], fingerPosition[1], fingerPosition[2], fingerGrp)
                base.rotate(0, fingerRotation[1], 0, fingerGrp)     
                base.makeIdentity(finger, apply = True, t = 1, r = 1, s = 1)      
                base.makeIdentity(fingerGrp, apply = True, t = 1, r = 1, s = 1)      
                base.parent(finger, fingerGrp)
                base.rotate(0, fingerRotation[1], 0, fingerGrp, r = True)   

                if j > 0:
                    base.parent(fingerGrp, "CTRL_"+side+"_Finger_"+str(i)+"_"+str(j-1))
                else:
                    base.parent(fingerGrp, "CTRL_"+side+"_Wrist")
                        
            
                                    
            

  
def setColors():
    base.setAttr('MASTER_CONTROLLER.overrideEnabled', 1)
    base.setAttr('MASTER_CONTROLLER.overrideRGBColors', 1)
    base.setAttr('MASTER_CONTROLLER.overrideColorRGB', 1,1,1)        
     
      