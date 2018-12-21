import maya.cmds as base
import Locators


Locators = reload(Locators)


def CreateJointsWindow():
    global setPrefix
    setPrefix = "test"

    base.window("Joint Creation")
    base.rowColumnLayout(nc = 1)
    base.button(l = "Create Joints", w = 200, c = "Joints.createJoints()")
    base.button(l = "Delete Joints", w = 200, c = "Joints.deleteJoints()")
    base.showWindow()

    
  
def createJoints():
    #displayLayer = base.ls('RIG', type = 'displayLayer')
    base.select(deselect = True)
   
    spineAmount = base.ls("Loc_SPINE_*", type = 'transform')
    amount = base.ls("Loc_L_Finger_*_0", type = 'transform')
    if base.objExists('RIG'):
        print 'RIG already exists'
    else:
        jointGRP = base.group(em = True, name = "RIG")

    ## create spine
    root = base.ls("Loc_ROOT")
    
    
    allSpines = base.ls("Loc_SPINE_*", type='locator')
    spine = base.listRelatives(*allSpines, p = True, f = True)
       
    rootPos = base.xform(root, q = True, t = True, ws = True)
    rootJoint = base.joint(radius = 1, p = rootPos, name = "RIG_ROOT")
        
    for i, s in enumerate(spine):
        pos = base.xform(s, q = True, t = True, ws = True)
        j = base.joint(radius = 0.8, p = pos, name = "RIG_SPINE_" + str(i))
    
    createHead(len(spineAmount))
    createArmJoints(len(spineAmount))
    createFingerJoints(len(amount))
    if(base.objExists("Loc_Volume_0")):
        CreateVolumeJoints()
    
    if (base.objExists('Loc_L_INV_Heel*')):
        createInverseFootRoll()
    else:
        print ''    
    createLegs()
    setJointOrientation()

def CreateVolumeJoints():    
    allSpines = base.ls("RIG_SPINE_*", type = 'joint')
    volumeLoc = base.ls("Loc_Volume_*", type = 'transform')
    l_chestVolume = base.ls("Loc_L_ChestVolume_*", type = 'transform')
    r_chestVolume = base.ls("Loc_R_ChestVolume_*", type = 'transform')    
    print allSpines
    print volumeLoc
    for i, s in enumerate(allSpines):
        if(i == len(allSpines) - 1):
            base.select(s)
            startPos = base.xform(s, q = True, t = True, ws = True)
            pos = base.xform(base.ls("Loc_Breathing", type = 'transform'), q = True, t = True, ws = True)
            breathingJointStart = base.joint(radius = 0.8, p = (startPos[0], startPos[1], startPos[2] + 0.05), name = "RIG_BREATHING_START")            
            breathingJointEnd = base.joint(radius = 0.8, p = pos, name = "RIG_BREATHING_END")
        else:    
            base.select(s)
            
            pos = base.xform(volumeLoc[i], q = True, t = True, ws = True)
            l_chestPos = base.xform(l_chestVolume[i], q = True, t = True, ws = True)
            r_chestPos = base.xform(r_chestVolume[i], q = True, t = True, ws = True)            
            
            volumeJoint = base.joint(radius = 0.8, p = pos, name = "RIG_VOLUME_"+str(i))
            base.select(s)
            l_chestVolumeJoint = base.joint(radius = 0.8, p = l_chestPos, name = "RIG_L_CHEST_VOLUME_"+str(i))
            base.select(s)
            r_chestVolumeJoint = base.joint(radius = 0.8, p = r_chestPos, name = "RIG_R_CHEST_VOLUME_"+str(i))
        
    
def createHead(amount):
    base.select(deselect = True)
    base.select("RIG_SPINE_"+str(amount - 1))   
    
    neckJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_Neck_Start'), q = True, t = True, ws = True), name = "RIG_Neck_Start")
    base.joint(radius = 1, p = base.xform(base.ls('Loc_Neck_End'), q = True, t = True, ws = True), name = "RIG_Neck_End")
    base.joint(radius = 1, p = base.xform(base.ls('Loc_Head'), q = True, t = True, ws = True), name = "RIG_Head")
    
    base.select(deselect = True)
    base.select("RIG_Neck_End")
    
    jawJointStart = base.joint(radius= 1, p = base.xform(base.ls('Loc_Jaw_Start'), q = True, t = True, ws = True), name = 'RIG_Jaw_Start')
    jawJointEnd = base.joint(radius = 1, p = base.xform(base.ls('Loc_Jaw_End'), q = True, t = True, ws = True), name = 'RIG_Jaw_End')
    
def createArmJoints(amount):
    base.select(deselect = True)
    base.select("RIG_SPINE_"+str(amount - 1))
    L_Clavicle = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_Clavicle'), q = True, t = True, ws = True), name = "RIG_L_Clavicle")
    L_UpperArmJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_UpperArm'), q = True, t = True, ws = True), name = "RIG_L_UpperArm")
    
    if(base.objExists('Loc_L_Elbow_2')):
        L_ElbowJoint = base.joint(radius = 1, p = base.xform(base.ls("Loc_L_Elbow_1"), q = True, t = True, ws = True), name = "RIG_L_Elbow_1")   
        L_ElbowJoint = base.joint(radius = 1, p = base.xform(base.ls("Loc_L_Elbow_2"), q = True, t = True, ws = True), name = "RIG_L_Elbow_2")   
    else:    
        L_ElbowJoint = base.joint(radius = 1, p = base.xform(base.ls("Loc_L_Elbow"), q = True, t = True, ws = True), name = "RIG_L_Elbow")
    
    if (base.objExists('Loc_L_ArmTwist_*')):
        L_armTwists = base.ls('Loc_L_ArmTwist_*', type = 'transform')
        print L_armTwists
        for i, a in enumerate(L_armTwists):
            L_twistJoint = base.joint(radius = 1, p = base.xform(a, q = True, t = True, ws = True), name = "RIG_L_ArmTwist_"+str(i))
    else:
        print ''
    L_WristJoint = base.joint(radius = 1, p = base.xform(base.ls("Loc_L_Wrist"), q = True, t = True, ws = True), name = "RIG_L_Wrist")
    
    base.select(deselect = True)
    base.select("RIG_SPINE_"+str(amount - 1))
    
    R_Clavicle = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_Clavicle'), q = True, t = True, ws = True), name = "RIG_R_Clavicle")
    R_UpperArmJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_UpperArm'), q = True, t = True, ws = True), name = "RIG_R_UpperArm")

    if(base.objExists('Loc_R_Elbow_2')):
        R_ElbowJoint = base.joint(radius = 1, p = base.xform(base.ls("Loc_R_Elbow_1"), q = True, t = True, ws = True), name = "RIG_R_Elbow_1")   
        R_ElbowJoint = base.joint(radius = 1, p = base.xform(base.ls("Loc_R_Elbow_2"), q = True, t = True, ws = True), name = "RIG_R_Elbow_2")   
    else:    
        R_ElbowJoint = base.joint(radius = 1, p = base.xform(base.ls("Loc_R_Elbow"), q = True, t = True, ws = True), name = "RIG_R_Elbow")

    
    if (base.objExists('Loc_R_ArmTwist_*')):
        R_armTwists = base.ls('Loc_R_ArmTwist_*', type = 'transform')
        for j, at in enumerate(R_armTwists):
            R_twistJoint = base.joint(radius = 1, p = base.xform(at, q = True, t = True, ws = True), name = "RIG_R_ArmTwist_"+str(j))
    else:
        print ''
    R_WristJoint = base.joint(radius = 1, p = base.xform(base.ls("Loc_R_Wrist"), q = True, t = True, ws = True), name = "RIG_R_Wrist")
    

    
def createFingerJoints(amount):
    for x in range(0, amount):
        createFinger(x)
       
   
def createFinger(i):

    base.select(deselect = True)
    base.select("RIG_L_Wrist")
    allFingers = base.ls( "Loc_L_Finger_" + str(i) + "_*", type='transform')
    fingers = base.listRelatives(allFingers, p = True, s = False)
   
    for x, f in enumerate(allFingers):
        
        pos = base.xform(f, q = True, t = True, ws = True)
        j = base.joint(radius = 1, p = pos, name = "RIG_L_Finger_"+str(i)+"_"+str(x))
        
        
    base.select(deselect = True)
    base.select("RIG_R_Wrist")
    r_allFingers = base.ls( "Loc_R_Finger_" + str(i) + "_*", type='transform')
    r_fingers = base.listRelatives(r_allFingers, p = True, s = False)

    for y, g in enumerate(r_allFingers):
        
        r_pos = base.xform(g, q = True, t = True, ws = True)
        r_j = base.joint(radius = 1, p = r_pos, name = "RIG_R_Finger_"+str(i)+"_"+str(y))    
        
        
        
def createLegs():
    base.select(deselect = True)
    base.select('RIG_ROOT')
    
    L_upperLegJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_UpperLeg', type = 'transform'), q = True, t = True, ws = True), name = "RIG_L_UpperLeg")
    L_KneeJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_LowerLeg'), q = True, t = True, ws = True), name = 'RIG_L_LowerLeg')   
    L_FootJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_Foot') , q = True, t = True, ws = True), name = 'RIG_L_Foot')     
    L_FootBallJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_FootBall') , q = True, t = True, ws = True), name = 'RIG_L_FootBall') 
    L_ToeJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_Toes'), q = True, t = True, ws = True), name = 'RIG_L_Toes')
    
    ## 
    base.select(deselect = True)
    base.select('RIG_ROOT')

    R_upperLegJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_UpperLeg', type = 'transform'), q = True, t = True, ws = True), name = "RIG_R_UpperLeg")
    R_KneeJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_LowerLeg'), q = True, t = True, ws = True), name = 'RIG_R_LowerLeg')  
    L_FootJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_Foot') , q = True, t = True, ws = True), name = 'RIG_R_Foot')     
    R_FootBallJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_FootBall'), q = True, t = True, ws = True)  , name = 'RIG_R_FootBall') 
    R_ToeJoint = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_Toes'), q = True, t = True, ws = True), name = 'RIG_R_Toes')

def createInverseFootRoll():
    base.select(deselect = True)

    L_heel = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_INV_Heel', type = 'transform'), q = True, t = True, ws = True), name = 'RIG_L_INV_Heel')
    L_toel = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_INV_Toes', type = 'transform'), q = True, t = True, ws = True), name = 'RIG_L_INV_Toes')
    L_ball = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_INV_Ball', type = 'transform'), q = True, t = True, ws = True), name = 'RIG_L_INV_Ball')
    L_ankle = base.joint(radius = 1, p = base.xform(base.ls('Loc_L_INV_Ankle', type = 'transform'), q = True, t = True, ws = True), name = 'RIG_L_INV_Ankle')
    base.parent(L_heel, 'RIG')

    base.select(deselect = True)


    R_heel = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_INV_Heel', type = 'transform'), q = True, t = True, ws = True), name = 'RIG_R_INV_Heel')
    R_toel = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_INV_Toes', type = 'transform'), q = True, t = True, ws = True), name = 'RIG_R_INV_Toes')
    R_ball = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_INV_Ball', type = 'transform'), q = True, t = True, ws = True), name = 'RIG_R_INV_Ball')
    R_ankle = base.joint(radius = 1, p = base.xform(base.ls('Loc_R_INV_Ankle', type = 'transform'), q = True, t = True, ws = True), name = 'RIG_R_INV_Ankle')
    base.parent(R_heel, 'RIG')

def setJointOrientation():

    base.select('RIG_ROOT')
    base.joint(e = True, ch = True, oj = 'xyz', secondaryAxisOrient = 'xup')    
      
def deleteJoints():
    base.select(deselect = True)
    base.delete(base.ls('RIG'))       
        
        
        
        