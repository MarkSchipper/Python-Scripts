import maya.cmds as base
import Locators

Locators = reload(Locators)

def IKHandles():
    
    print Locators.ReturnSpineAmount()
    base.ikHandle(name = "IK_L_Arm", sj = base.ls("RIG_L_UpperArm")[0], ee = base.ls("RIG_L_Wrist")[0], sol = 'ikRPsolver')
    base.ikHandle(name = "IK_R_Arm", sj = base.ls("RIG_R_UpperArm")[0], ee = base.ls("RIG_R_Wrist")[0], sol = 'ikRPsolver')
    base.ikHandle(name = "IK_L_Leg", sj = base.ls("RIG_L_UpperLeg")[0], ee = base.ls("RIG_L_Foot")[0], sol = 'ikRPsolver')
    base.ikHandle(name = "IK_R_Leg", sj = base.ls("RIG_R_UpperLeg")[0], ee = base.ls("RIG_R_Foot")[0], sol = 'ikRPsolver')            
    
    
    ##########################################
    rootPos = base.xform(base.ls("RIG_ROOT", type = 'joint'), q = True, t = True, ws = True)
    spines = base.ls("RIG_SPINE_*", type = 'joint')
    
    spinePos = []
    
    for i, sp in enumerate(spines):
        spinePos.append(base.xform(spines[i], q = True, t = True, ws = True))
        
        
    base.curve( p = [(rootPos[0], rootPos[1], rootPos[2])], n = "SpineCurve", degree = 1)    

    for j, sp in enumerate(spinePos):
        base.curve('SpineCurve', a = True, p = [(spinePos[j][0], spinePos[j][1], spinePos[j][2])])
        
    
    curveCV = base.ls('SpineCurve.cv[0:]', fl = True)
    
    for k, cv in enumerate(curveCV):
        c = base.cluster(cv, cv, n = "Cluster_"+str(k)+"_")
        
        if k > 0:
            base.parent(c, "Cluster_"+str(k - 1)+"_Handle")
    
    
    base.ikHandle(n = "IK_Spine", sj = "RIG_ROOT", ee = "RIG_SPINE_" + str(Locators.ReturnSpineAmount() - 1), sol = 'ikSplineSolver', c = 'SpineCurve')    
        
