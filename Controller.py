import maya.cmds as base

def CreateController():
    #arrow = base.curve(p = [(1,0,0),(1,0,2), (2,0,2),(0,0,6), (-2,0,2), (-1,0,2), (-1,0,0), (1,0,0)], degree = 1)
    CreateMaster()
    CreatePelvis()
    CreateWrists()
    CreateClavicles()
    
def CreateMaster():
    ## master
    master_ctrl = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 16, name = "MASTER_CONTROLLER")
    selection = base.select("MASTER_CONTROLLER.cv[1]","MASTER_CONTROLLER.cv[3]","MASTER_CONTROLLER.cv[5]","MASTER_CONTROLLER.cv[7]","MASTER_CONTROLLER.cv[9]","MASTER_CONTROLLER.cv[11]","MASTER_CONTROLLER.cv[13]","MASTER_CONTROLLER.cv[15]")
    base.scale(0.7, 0.7, 0.7, selection)
    base.scale(2, 2, 2, master_ctrl)

    base.makeIdentity(master_ctrl, apply = True, t = 1, r = 1, s = 1)
    
def CreatePelvis():
    ## pelvis
    pelvis_ctrl = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 8, name = "CTRL_PELVIS")
    rootPos = base.xform(base.ls("RIG_ROOT", type = 'joint'), q = True, t = True, ws = True)
    base.move(rootPos[0],rootPos[1],rootPos[2], pelvis_ctrl) 
    base.scale(0.5, 0.5, 0.5, pelvis_ctrl)   
    base.makeIdentity(pelvis_ctrl, apply = True, t = 1, r = 1, s = 1)  
    base.parent(pelvis_ctrl, "MASTER_CONTROLLER")       
    
def CreateWrists():    

    #left
    L_wrist_ctrl = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 16, name = "CTRL_L_Wrist")
    l_selection = base.select("CTRL_L_Wrist.cv[1]","CTRL_L_Wrist.cv[3]","CTRL_L_Wrist.cv[5]","CTRL_L_Wrist.cv[7]","CTRL_L_Wrist.cv[9]","CTRL_L_Wrist.cv[11]","CTRL_L_Wrist.cv[13]","CTRL_L_Wrist.cv[15]")
    base.scale(0.7, 0.7, 0.7, l_selection)
    base.scale(0.15, 0.15, 0.15, L_wrist_ctrl)
    
    l_wristPos = base.xform(base.ls("RIG_L_Wrist"), q = True, t = True, ws = True)
    l_wristRot = base.joint(base.ls("RIG_L_Wrist"), q = True, o = True)
    
    base.move(l_wristPos[0], l_wristPos[1], l_wristPos[2], L_wrist_ctrl)
    base.rotate(0, 0, l_wristRot[0], L_wrist_ctrl)
    
    base.makeIdentity(L_wrist_ctrl, apply = True, t = 1, r = 1, s = 1)
    base.parent(L_wrist_ctrl, "MASTER_CONTROLLER")
    
    #right
    R_wrist_ctrl = base.circle(nr = (0,1,0), c = (0,0,0), radius = 1, degree = 1, s = 16, name = "CTRL_R_Wrist")
    r_selection = base.select("CTRL_R_Wrist.cv[1]","CTRL_R_Wrist.cv[3]","CTRL_R_Wrist.cv[5]","CTRL_R_Wrist.cv[7]","CTRL_R_Wrist.cv[9]","CTRL_R_Wrist.cv[11]","CTRL_R_Wrist.cv[13]","CTRL_L_Wrist.cv[15]")
    base.scale(0.7, 0.7, 0.7, r_selection)
    base.scale(0.15, 0.15, 0.15, R_wrist_ctrl)
    
    r_wristPos = base.xform(base.ls("RIG_R_Wrist"), q = True, t = True, ws = True)
    r_wristRot = base.joint(base.ls("RIG_R_Wrist"), q = True, o = True)
    
    base.move(r_wristPos[0], r_wristPos[1], r_wristPos[2], R_wrist_ctrl)
    base.rotate(0, 0, r_wristRot[0], R_wrist_ctrl)
    
    base.makeIdentity(R_wrist_ctrl, apply = True, t = 1, r = 1, s = 1)
    base.parent(R_wrist_ctrl, "MASTER_CONTROLLER")
    
    
def CreateClavicles():
    l_clavicle = base.curve(p = [(1,0,0),(1,1,1), (1,1.5,2), (1,1.7,3), (1,1.5,4), (1,1,5), (1,0,6), (-1, 0,6), (-1,1,5), (-1,1.5,4), (-1,1.7,3), (-1,1.5,2), (-1,1,1), (-1,0,0) ], degree = 1, name = "CTRL_L_Clavicle")
    r_clavicle = base.curve(p = [(1,0,0),(1,1,1), (1,1.5,2), (1,1.7,3), (1,1.5,4), (1,1,5), (1,0,6), (-1, 0,6), (-1,1,5), (-1,1.5,4), (-1,1.7,3), (-1,1.5,2), (-1,1,1), (-1,0,0) ], degree = 1, name = "CTRL_R_Clavicle")
    
    base.scale(0.05, 0.05, 0.05, l_clavicle)    
    base.scale(0.05, 0.05, 0.05, r_clavicle)  
    
    l_ArmPos = base.xform(base.ls("RIG_L_UpperArm"), q = True, t = True, ws = True)  
    r_ArmPos = base.xform(base.ls("RIG_R_UpperArm"), q = True, t = True, ws = True)
    
    
    base.move(l_ArmPos[0], l_ArmPos[1] + 0.125, l_ArmPos[2] - 0.1, l_clavicle)
    base.move(r_ArmPos[0], r_ArmPos[1] + 0.125, r_ArmPos[2] - 0.1, r_clavicle)    
    
    base.parent(l_clavicle, "CTRL_PELVIS")
    base.parent(r_clavicle, "CTRL_PELVIS")    
        
        
def CreateFeet():
    arrow = base.curve(p = [(1,0,0),(1,0,-2), (2,0,-2),(0,0,-6), (-2,0,-2), (-1,0,-2), (-1,0,0), (1,0,0)], degree = 1)            
        
    