import maya.cmds as base

import SetAttributes

SetAttributes = reload(SetAttributes)

def CreateConstraints(fingerCount, spineAmount):
    
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
    
    base.orientConstraint("CTRL_L_Clavicle", "RIG_L_Clavicle", mo = True)
    base.orientConstraint("CTRL_R_Clavicle", "RIG_R_Clavicle", mo = True)
    base.orientConstraint("CTRL_NECK", "RIG_Neck_Start", mo = True)
    base.orientConstraint("CTRL_HEAD", "RIG_Neck_End", mo = True)
    base.orientConstraint("CTRL_JAW", "RIG_Jaw_Start", mo = True)
    if(base.objExists("CTRL_BREATHING")):
        base.orientConstraint("CTRL_BREATHING", "RIG_BREATHING_START", mo = True)
    
    base.connectAttr("CTRL_SPINE_"+str(spineAmount - 1)+".rotateY", "IK_Spine.twist")
    
    if base.objExists("RIG_L_ArmTwist_0"):
        l_twistJoints = base.ls("RIG_L_ArmTwist_*")
        r_twistJoints = base.ls("RIG_L_ArmTwist_*")
        for i, x in enumerate(l_twistJoints):   
            l_wristMultiply = base.shadingNode("multiplyDivide", asUtility = True, n = "L_ArmTwist_Node_"+str(i))
            base.setAttr(l_wristMultiply+".operation", 1)
            base.setAttr(l_wristMultiply+".input2Y", (1.0 - (1.0 / len(l_twistJoints) * (i + 1))) * -1)
            
            
            #check connections
            print base.listConnections("L_ArmTwist_Node_"+str(i), plugs = True)
            
            #input
            base.connectAttr("CTRL_L_Wrist.rotateY", "L_ArmTwist_Node_"+str(i)+".input1Y")
            #output
            base.connectAttr("L_ArmTwist_Node_"+str(i)+".outputY", "RIG_L_ArmTwist_"+str(i)+".rotateX")
            
            r_wristMultiply = base.shadingNode("multiplyDivide", asUtility = True, n = "R_ArmTwist_Node_"+str(i))
            base.setAttr(r_wristMultiply+".operation", 1)
            base.setAttr(r_wristMultiply+".input2Y", (1.0 - (1.0 / len(r_twistJoints) * (i + 1))) * -1)
            #input
            base.connectAttr("CTRL_R_Wrist.rotateY", "R_ArmTwist_Node_"+str(i)+".input1Y")
            #output
            base.connectAttr("R_ArmTwist_Node_"+str(i)+".outputY", "RIG_R_ArmTwist_"+str(i)+".rotateX")
            
    
    clusters = base.ls("Spine_Cluster_*", type = 'transform')
    spineCtrl = base.ls("CTRL_SPINE_*", type = 'transform')      
    
    for j, cl in enumerate(clusters):
        if j > 0:
            print j
            base.parent(cl, spineCtrl[j - 1])
            print spineCtrl[j - 1]
        else:
            base.parent(cl, "CTRL_PELVIS")     
            
                
    for k in range(0, fingerCount):
        l_allFingers = base.ls("RIG_L_Finger_"+str(k)+"_*")
        r_allFingers = base.ls("RIG_R_Finger_"+str(k)+"_*")        
        
        if(k > 0):
            base.connectAttr("CTRL_L_Finger_"+str(k)+".rotateZ", l_allFingers[0]+".rotateY")
            base.connectAttr("CTRL_R_Finger_"+str(k)+".rotateZ", r_allFingers[0]+".rotateY")
        
            for l, l_finger in enumerate(l_allFingers):
                base.connectAttr("CTRL_L_Finger_"+str(k)+".rotateY", l_finger+".rotateZ")
            
            for m, r_finger in enumerate(r_allFingers):
                base.connectAttr("CTRL_R_Finger_"+str(k)+".rotateY", r_finger+".rotateZ")
        else:
            base.connectAttr("CTRL_L_Finger_"+str(k)+".rotateZ", l_allFingers[0]+".rotateY")
            base.connectAttr("CTRL_R_Finger_"+str(k)+".rotateZ", r_allFingers[0]+".rotateY")
        
            for l, l_finger in enumerate(l_allFingers):
                base.connectAttr("CTRL_L_Finger_"+str(k)+".rotateX", l_finger+".rotateZ")
            
            for m, r_finger in enumerate(r_allFingers):
                base.connectAttr("CTRL_R_Finger_"+str(k)+".rotateX", r_finger+".rotateZ")            
        
    if base.objExists("RIG_L_INV_Heel"):
        base.pointConstraint("RIG_L_INV_Toes", "IK_L_Toes", mo = True)
        base.pointConstraint("RIG_L_INV_Ball", "IK_L_FootBall", mo = True)
        base.pointConstraint("RIG_L_INV_Ankle", "IK_L_Leg", mo = True)
        
        base.pointConstraint("RIG_R_INV_Toes", "IK_R_Toes", mo = True)
        base.pointConstraint("RIG_R_INV_Ball", "IK_R_FootBall", mo = True)
        base.pointConstraint("RIG_R_INV_Ankle", "IK_R_Leg", mo = True)
        
        base.pointConstraint("CTRL_L_Foot", "RIG_L_INV_Heel", mo = True)
        base.orientConstraint("CTRL_L_Foot", "RIG_L_INV_Heel", mo = True)
        
        base.pointConstraint("CTRL_R_Foot", "RIG_R_INV_Heel", mo = True)
        base.orientConstraint("CTRL_R_Foot", "RIG_R_INV_Heel", mo = True)
        
        base.connectAttr("CTRL_L_Foot.Foot_Roll", "RIG_L_INV_Ball.rotateX")
        base.connectAttr("CTRL_L_Foot.Ball_Roll", "RIG_L_INV_Toes.rotateX")
        
        base.connectAttr("CTRL_R_Foot.Foot_Roll", "RIG_R_INV_Ball.rotateX")
        base.connectAttr("CTRL_R_Foot.Ball_Roll", "RIG_R_INV_Toes.rotateX")
        
       
        
    else:
        base.parent("IK_L_Toes", "IK_L_FootBall")
        base.parent("IK_L_FootBall", "IK_L_Leg")              
        
        base.parent("IK_R_Toes", "IK_R_FootBall")
        base.parent("IK_R_FootBall", "IK_R_Leg")        
        
        base.pointConstraint("CTRL_R_Foot", "IK_R_Leg", mo = True)
        base.orientConstraint("CTRL_R_Foot", "IK_R_Leg", mo = True)
        
        base.pointConstraint("CTRL_L_Foot", "IK_L_Leg", mo = True)
        base.orientConstraint("CTRL_L_Foot", "IK_L_Leg", mo = True)
        
    
    #feet constraints    
    
    #lleft
    base.setAttr("IK_L_Leg.poleVectorX", 1)
    base.setAttr("IK_L_Leg.poleVectorZ", 0)
    l_footAverage = base.shadingNode("plusMinusAverage", asUtility = True, n = "L_Foot_Node") 
    base.setAttr(l_footAverage+".operation", 2)   
    base.connectAttr("CTRL_L_Foot.Knee_Fix", l_footAverage+".input1D[0]")
    base.connectAttr("CTRL_L_Foot.Knee_Twist", l_footAverage+".input1D[1]")  
    base.connectAttr(l_footAverage+".output1D", "IK_L_Leg.twist")  
    base.setAttr("CTRL_L_Foot.Knee_Fix", 90)
    
    #right
    base.setAttr("IK_R_Leg.poleVectorX", 1)
    base.setAttr("IK_R_Leg.poleVectorZ", 0)
    r_footAverage = base.shadingNode("plusMinusAverage", asUtility = True, n = "R_Foot_Node") 
    base.setAttr(r_footAverage+".operation", 2)   
    base.connectAttr("CTRL_R_Foot.Knee_Fix", r_footAverage+".input1D[0]")
    base.connectAttr("CTRL_R_Foot.Knee_Twist", r_footAverage+".input1D[1]")  
    base.connectAttr(r_footAverage+".output1D", "IK_R_Leg.twist")  
    base.setAttr("CTRL_R_Foot.Knee_Fix", 90)
    
    SetAttributes.LockAttributes()    

def BindSkin():
    sel = base.ls(sl = True)
    if (len(sel) == 0):
        base.confirmDialog(title = "Empty Selection", message = "You have to select a mesh", button = ['Ok'])
    else:
        for i in range(0, len(sel)):
            base.skinCluster(sel[i], "RIG_ROOT", bm = 3, sm = 1, dr = 0.1, name = "Mesh"+str(i))
            base.geomBind('Mesh'+str(i), bm = 3, gvp = [256, 1])   
    
     

    if (base.objExists("RIG_LAYER")):
        _rig = base.select("RIG") 
        base.editDisplayLayerMembers("RIG_LAYER", "RIG")
    else:   
        _rig = base.select("RIG") 
        base.createDisplayLayer(nr = True, name = "RIG_LAYER")        
    
    _ik = base.ls("IK_*")
    base.editDisplayLayerMembers("RIG_LAYER", _ik)
    

    if (base.objExists("CONTROLLERS")):
        base.editDisplayLayerMembers("CONTROLLERS", "MASTER_CONTROLLER")
    else:
        _ctrl = base.select("MASTER_CONTROLLER")    
        base.createDisplayLayer(nr = True, name = "CONTROLLERS")
        
        
        
                
            
            