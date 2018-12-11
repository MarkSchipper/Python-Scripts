import maya.cmds as base

def CreateConstraints(fingerCount):
    
    #left
    l_wristCtrl = base.ls("CTRL_L_Wrist", type = 'transform')
    l_wristIK = base.ls("IK_L_Arm")
    l_wristJoint = base.ls("RIG_L_Wrist")
        

    #right
    r_wristCtrl = base.ls("CTRL_R_Wrist", type = 'transform')
    r_wristIK = base.ls("IK_R_Arm")
    r_wristJoint = base.ls("RIG_R_Wrist")
    
    base.pointConstraint(l_wristCtrl, l_wristIK, mo = True)
    base.orientConstraint(l_wristCtrl, l_wristJoint, mo = True)
    base.connectAttr("CTRL_L_Wrist.Elbow_PV", "IK_L_Arm.twist")
    
    base.pointConstraint(r_wristCtrl, r_wristIK, mo = True)
    base.orientConstraint(r_wristCtrl, r_wristJoint, mo = True)    
    base.connectAttr("CTRL_R_Wrist.Elbow_PV", "IK_R_Arm.twist") 
    
    base.orientConstraint("CTRL_L_Clavicle", "RIG_L_Clavicle")
    base.orientConstraint("CTRL_R_Clavicle", "RIG_R_Clavicle")
    
    
    base.orientConstraint("CTRL_NECK", "RIG_Neck_Start")
    
    if base.objExists("RIG_L_ArmTwist_0"):
        l_twistJoints = base.ls("RIG_L_ArmTwist_*")
        r_twistJoints = base.ls("RIG_L_ArmTwist_*")
        for i, x in enumerate(l_twistJoints):   
            l_wristMultiply = base.shadingNode("multiplyDivide", asUtility = True, n = "L_ArmTwist_Node_"+str(i))
            base.setAttr(l_wristMultiply+".operation", 1)
            base.setAttr(l_wristMultiply+".input2Y", 1 - (1 / len(l_twistJoints) * (i + 1)))
            #input
            base.connectAttr("CTRL_L_Wrist.rotateY", "L_ArmTwist_Node_"+str(i)+".input1Y")
            #output
            base.connectAttr("L_ArmTwist_Node_"+str(i)+".outputY", "RIG_L_ArmTwist_"+str(i)+".rotateX")
            
            r_wristMultiply = base.shadingNode("multiplyDivide", asUtility = True, n = "R_ArmTwist_Node_"+str(i))
            base.setAttr(r_wristMultiply+".operation", 1)
            base.setAttr(r_wristMultiply+".input2Y", 1 - (1 / len(r_twistJoints) * (i + 1)))
            #input
            base.connectAttr("CTRL_R_Wrist.rotateY", "R_ArmTwist_Node_"+str(i)+".input1Y")
            #output
            base.connectAttr("R_ArmTwist_Node_"+str(i)+".outputY", "RIG_R_ArmTwist_"+str(i)+".rotateX")
            
    
    clusters = base.ls("Cluster_*", type = 'transform')
    spineCtrl = base.ls("CTRL_SPINE_*", type = 'transform')      
    
    for j, cl in enumerate(clusters):
        if j > 0:
            base.parent(cl, spineCtrl[j - 1])
        else:
            base.parent(cl, "CTRL_PELVIS")     
            
                
    for k in range(0, fingerCount):
        l_allFingers = base.ls("RIG_L_Finger_"+str(k)+"_*")
        r_allFingers = base.ls("RIG_R_Finger_"+str(k)+"_*")        
        
        base.connectAttr("CTRL_L_Finger_"+str(k)+".rotateY", l_allFingers[0]+".rotateY")
        base.connectAttr("CTRL_R_Finger_"+str(k)+".rotateY", r_allFingers[0]+".rotateY")
        
        for l, l_finger in enumerate(l_allFingers):
            base.connectAttr("CTRL_L_Finger_"+str(k)+".rotateZ", l_finger+".rotateZ")
        
        for m, r_finger in enumerate(r_allFingers):
            base.connectAttr("CTRL_R_Finger_"+str(k)+".rotateZ", r_finger+".rotateZ")        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                
            
            