import maya.cmds as base

##############################################
##            Locators class                ##
## Creates all the Locators					##
##############################################

# create the input fields for the amount of spines and fingers
def createFields():    
    global spineCount
    global fingerCount
    base.text("Spine Count", l = "Spine Count")
    spineCount = base.intField(minValue = 1, maxValue = 10, value = 4)

    base.text("Fingers Amount", l = "Fingers Amount")
    fingerCount = base.intField(minValue = 1, maxValue = 10, value = 5)
    
# return the value from the spineCount int field
def ReturnFingerAmount():
    return base.intField(fingerCount, query = True, value = True)

# return the value from the fingerCount int field    
def ReturnSpineAmount():
   return base.intField(spineCount, query = True, value = True)    

# Create the Locators
def CreateLocators():
    
    # Check if the object 'Loc_Master' exists, if it does do nothing
    # else create an empty ( em = True ) group and name it          
    if base.objExists('Loc_Master'):
        print 'Loc_Master already exists'
    else:
        base.group(em = True, name = "Loc_Master")
    
    # Create a new spaceLocator and store it in the var root
    # Scale it down and move it, parent it to the group    
    root = base.spaceLocator(n = "Loc_ROOT")    
    base.scale(0.1,0.1,0.1, root)
    base.move(0,1,0, root)
    base.parent(root, "Loc_Master")

    createSpine()

# create the spine function    
def createSpine():
    
    # simple for loop, check how many spines we need to create
    for i in range(0, base.intField(spineCount, query = True, value = True)):
        spine = base.spaceLocator(n = 'Loc_SPINE_' + str(i))
        base.scale(0.1, 0.1, 0.1, spine)
        if i == 0:
            base.parent(spine, 'Loc_ROOT')
        else:
            base.parent(spine, 'Loc_SPINE_' + str(i - 1))
        base.move(0, 1.25 + (0.25 * i), 0, spine)

    createHead()
    createArms(1)        
    createArms(-1)
    createLegs(1)
    createLegs(-1)
    
    # set colors of the objects
    setColors()
    
def createHead():
    neck = base.spaceLocator(n = 'Loc_Neck')
    base.parent(neck, 'Loc_SPINE_' + str(ReturnSpineAmount() - 1))
    base.scale(1,1, 1, neck)
    base.move(0,1.25 + (0.25 * ReturnSpineAmount()), 0, neck)  
    
    head = base.spaceLocator(n = 'Loc_Head')
    base.parent(head, 'Loc_Neck')
    base.scale(1,1,1, head)
    base.move(0, 1.50 + (0.25 * base.intField(spineCount, query = True, value = True)),0, head)  
    
    ## jaw
    jawEnd = base.spaceLocator(n = 'Loc_Jaw_End')
    jawStart = base.spaceLocator(n = 'Loc_Jaw_Start')
    base.parent(jawStart, 'Loc_Head')
    base.parent(jawEnd, jawStart)
    base.scale(1,1,1, jawEnd)
    base.scale(0.5,0.5,0.5, jawStart)
    base.move(0, 1.40 + (0.25 * base.intField(spineCount, query = True, value = True)),0.02, jawStart)
    base.move(0, 1.40 + (0.25 * base.intField(spineCount, query = True, value = True)),0.15, jawEnd)

def createLegs(side):
    if side == 1:
        if base.objExists('L_Leg_GRP'):
            print 'nuttn'
        else:
            upperLegGRP = base.group(em = True, name = 'L_Leg_GRP')
            base.parent(upperLegGRP, 'Loc_ROOT')
            base.move(0.1, 1, 0, upperLegGRP)

        upperLeg = base.spaceLocator(n = 'Loc_L_UpperLeg')
        base.scale(0.1,0.1,0.1, upperLeg)
        base.move(0.15, 1, 0, upperLeg)
        base.parent(upperLeg, 'L_Leg_GRP')
        
        
        ## lower leg
        lowerLeg = base.spaceLocator(n = 'Loc_L_LowerLeg')
        base.scale(0.1,0.1,0.1, lowerLeg)
        base.move(0.15,0.2, 0, lowerLeg)
        base.parent(lowerLeg, 'Loc_L_UpperLeg')
        
        ## foot
        foot = base.spaceLocator(n = 'Loc_L_Foot')
        base.scale(0.1, 0.1, 0.1, foot)
        base.move(0.15, -0.4, 0, foot)
        base.parent(foot, 'Loc_L_LowerLeg')
        
        ## football
        
        football = base.spaceLocator(n = 'Loc_L_FootBall')
        base.scale(0.1,0.1,0.1, football)
        base.move(0.15, -0.5, 0.15, football)
        base.parent(football, 'Loc_L_Foot')
        
        ## toes
        
        toes = base.spaceLocator(n = 'Loc_L_Toes')
        base.scale(0.1,0.1,0.1, toes)
        base.move(0.15, -0.5, 0.3, toes)
        base.parent(toes, 'Loc_L_FootBall')
            
    else:    
        if base.objExists('R_Leg_GRP'):
            print 'nuttn'
        else:
            upperLegGRP = base.group(em = True, name = 'R_Leg_GRP')
            base.parent(upperLegGRP,'Loc_ROOT')
            base.move(-0.1, 1, 0, upperLegGRP)
            
        upperLeg = base.spaceLocator(n = 'Loc_R_UpperLeg')
        base.scale(0.1,0.1,0.1, upperLeg)
        base.move(-0.15, 1, 0, upperLeg)
        base.parent(upperLeg, 'R_Leg_GRP')
        
        # lower leg
        
        lowerLeg = base.spaceLocator(n = 'Loc_R_LowerLeg')
        base.scale(0.1,0.1,0.1, lowerLeg)
        base.move(-0.15, 0.2, 0, lowerLeg)
        base.parent(lowerLeg, 'Loc_R_UpperLeg')
        
        # foot
        
        foot = base.spaceLocator(n = 'Loc_R_Foot')
        base.scale(0.1, 0.1, 0.1, foot)
        base.move(-0.15, -0.4, 0, foot)
        base.parent(foot, 'Loc_R_LowerLeg')
        
        ## football
        
        football = base.spaceLocator(n = 'Loc_R_FootBall')
        base.scale(0.1,0.1,0.1, football)
        base.move(-0.15, -0.5, 0.15, football)
        base.parent(football, 'Loc_R_Foot')
        
        ## toes
        
        toes = base.spaceLocator(n = 'Loc_R_Toes')
        base.scale(0.1,0.1,0.1, toes)
        base.move(-0.15, -0.5, 0.3, toes)
        base.parent(toes, 'Loc_R_Foot')
        
def createArms(side):
    global editMode
    if side == 1: # left
        if base.objExists('L_Arm_GRP'):
            print 'im not doing anything'
        else:
            #L_arm = base.group(em = True, name = 'L_Arm_GRP')
            #base.parent(L_arm, 'Loc_SPINE_'+ str(base.intField(spineCount, query = True, value = True) - 1))
            
            #clavicle start
            clavicle = base.spaceLocator(n = 'Loc_L_Clavicle')
            base.scale(0.1,0.1,0.1, clavicle)
            base.parent(clavicle, 'Loc_SPINE_'+ str(base.intField(spineCount, query = True, value = True) - 1))
            base.move(0.1 * side, 1 + (0.25 * base.intField(spineCount, query = True, value = True)), 0.1, clavicle)
            
            #upperarm          
            upperArm = base.spaceLocator(n = 'Loc_L_UpperArm') # arm
            base.scale(0.1,0.1, 0.1, upperArm)
            base.parent(upperArm, 'Loc_L_Clavicle')
            base.move(0.35 * side, 1 + (0.25 * base.intField(spineCount, query = True, value = True)), 0, upperArm)
            
            #elbow
            elbow = base.spaceLocator(n = 'Loc_L_Elbow')
            base.scale(0.1,0.1,0.1, elbow)
            base.parent(elbow, upperArm)
            
            #wrist
            
            wrist = base.spaceLocator(n = 'Loc_L_Wrist')
            base.scale(0.1,0.1,0.1, wrist)
            base.parent(wrist, elbow)
            base.move(0.35 * side, 1 + (0.25 * base.intField(spineCount, query = True, value = True)), 0, upperArm)
            
            #move elbow
            base.move(0.6 * side, 1.4, -0.2, elbow)
            
            #move wrist
            base.move(0.8 * side, 1, 0, wrist)
            createHands(1, wrist)
            
    else: # right
        if base.objExists('R_Arm_GRP'):
            print 'im still not doing anything'
        else:
            R_arm = base.group(em = True, name = 'R_Arm_GRP')
            base.parent(R_arm, 'Loc_SPINE_' + str(base.intField(spineCount, query = True, value = True) - 1)) 
            
            #clavicle start
            clavicle = base.spaceLocator(n = 'Loc_R_Clavicle')
            base.scale(0.1,0.1,0.1, clavicle)
            base.parent(clavicle, 'Loc_SPINE_'+ str(base.intField(spineCount, query = True, value = True) - 1))
            base.move(0.1 * side, 1 + (0.25 * base.intField(spineCount, query = True, value = True)), 0.1, clavicle)
            
            ## upperarm
            upperArm = base.spaceLocator(n = 'Loc_R_UpperArm')
            base.scale(0.1,0.1,0.1, upperArm)
            base.parent(upperArm, 'Loc_R_Clavicle')
            base.move(0.35 * side, 1 + (0.25 * base.intField(spineCount, query = True, value = True)), 0, upperArm)  
            
             #elbow
            elbow = base.spaceLocator(n = 'Loc_R_Elbow')
            base.scale(0.1,0.1,0.1, elbow)
            base.parent(elbow, upperArm)
            
            #wrist
            
            wrist = base.spaceLocator(n = 'Loc_R_Wrist')
            base.scale(0.1,0.1,0.1, wrist)
            base.parent(wrist, elbow)
            
            base.move(0.35 * side, 1 + (0.25 * base.intField(spineCount, query = True, value = True)), 0, R_arm)           
            
            #move elbow
            base.move(0.6 * side, 1.4, -0.2, elbow)
            
            #move wrist
            base.move(0.8 * side, 1, 0, wrist)

   
            createHands(-1, wrist)


def createHands(side, wrist):
    if side == 1:
        if base.objExists('L_Hand_GRP'):
            print 'nuttin'
        else:
            hand = base.group(em = True, name = 'L_Hand_GRP')
            pos = base.xform(wrist, q=True, t = True, ws = True)
            base.move(pos[0], pos[1], pos[2], hand)
            base.parent(hand, 'Loc_L_Wrist')
            
            for i in range(0, base.intField(fingerCount, query = True, value = True)):
                createFingers(1, pos, i)
            
    else:
        if base.objExists('R_Hand_GRP'):
            print 'do'
        else:

            hand = base.group(em = True, name = 'R_Hand_GRP')
            pos = base.xform(wrist, q=True, t = True, ws = True)
            base.move(pos[0], pos[1], pos[2], hand)        
            base.parent(hand, 'Loc_R_Wrist')
            
            for i in range(0, base.intField(fingerCount, query = True, value = True)):
                createFingers(-1, pos, i)

def createFingers(side, handPos, count):
    for x in range(0,3):
        if side == 1:
            finger = base.spaceLocator(n = 'Loc_L_Finger_' + str(count) + '_' + str(x))
            base.scale(0.05, 0.05, 0.05, finger)
            if x == 0:
                base.parent(finger, 'Loc_L_Wrist')
            else:
                base.parent(finger, 'Loc_L_Finger_' + str(count) + '_' + str(x - 1))
            base.move(handPos[0] + (0.1 + (0.1 * x)) * side, handPos[1] - (0.1 + (0.1 *x)), handPos[2] + -(0.05 * count), finger)
        else:        
            finger = base.spaceLocator(n = 'Loc_R_Finger_' + str(count) + '_' + str(x))
            base.scale(0.05, 0.05, 0.05, finger)
            if x == 0:
                base.parent(finger, 'Loc_R_Wrist')
            else:
                base.parent(finger, 'Loc_R_Finger_' + str(count) + '_' + str(x - 1))
            base.move(handPos[0] + (0.1 + (0.1 * x)) * side, handPos[1] - (0.1 + (0.1 *x)), handPos[2] + -(0.05 * count), finger)
    
def setColors():
    base.setAttr('Loc_Master.overrideEnabled', 1)
    base.setAttr('Loc_Master.overrideRGBColors', 1)

 
def mirrorLocators():
    allLeftLocators = base.ls("Loc_L_*")
    leftLocators = base.listRelatives(*allLeftLocators, p = True, f = True)

    allRightLocators = base.ls("Loc_R_*")
    rightLocators = base.listRelatives(*allRightLocators, p = True, f = True)
    
    for i,l in enumerate(leftLocators):
        pos = base.xform(l, q = True, t=True, ws = True)
        base.move(-pos[0], pos[1], pos[2], rightLocators[i])
            
def deleteLocators():
    nodes = base.ls("Loc_*")
    base.delete(nodes)   
  