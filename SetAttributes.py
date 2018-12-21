import maya.cmds as base

def LockAttributes():
    axis = ['X', 'Y', 'Z']
    
    allSpines = base.ls('CTRL_SPINE_*', type = 'transform')
    l_allFingers = base.ls('CTRL_L_Finger_*', type = 'transform')
    r_allFingers = base.ls('CTRL_R_Finger_*', type = 'transform')
    
    for axe in axis:
       
        base.setAttr('CTRL_PELVIS.scale'+axe, lock = True, k = False)
        base.setAttr('CTRL_L_Wrist.scale'+axe, lock = True, k = False)
        base.setAttr('CTRL_R_Wrist.scale'+axe, lock = True, k = False)
        base.setAttr('CTRL_L_Foot.scale'+axe, lock = True, k = False)
        base.setAttr('CTRL_R_Foot.scale'+axe, lock = True, k = False)
        
        base.setAttr('CTRL_L_Clavicle.scale'+axe, lock = True, k = False)        
        base.setAttr('CTRL_L_Clavicle.translate'+axe, lock = True, k = False)        
        base.setAttr('CTRL_R_Clavicle.scale'+axe, lock = True, k = False)        
        base.setAttr('CTRL_R_Clavicle.translate'+axe, lock = True, k = False)          
        
        for i in range(0, len(allSpines)):
            base.setAttr('CTRL_SPINE_'+str(i)+'.translate'+axe, lock = True, k = False)
            base.setAttr('CTRL_SPINE_'+str(i)+'.scale'+axe, lock = True, k = False)
            
        base.setAttr('CTRL_NECK.scale'+axe, lock = True, k = False)    
        base.setAttr('CTRL_NECK.translate'+axe, lock = True, k = False)
        
        base.setAttr('CTRL_HEAD.scale'+axe, lock = True, k = False)    
        base.setAttr('CTRL_HEAD.translate'+axe, lock = True, k = False)
        
        base.setAttr('CTRL_BREATHING.scale'+axe, lock = True, k = False)        
        base.setAttr('CTRL_BREATHING.translate'+axe, lock = True, k = False)        
        base.setAttr('CTRL_BREATHING.rotateY', lock = True, k = False)
        base.setAttr('CTRL_BREATHING.rotateZ', lock = True, k = False)
        
        base.setAttr('CTRL_JAW.scale'+axe, lock = True, k = False)        
        base.setAttr('CTRL_JAW.translate'+axe, lock = True, k = False)        
        base.setAttr('CTRL_JAW.rotateY', lock = True, k = False)
        base.setAttr('CTRL_JAW.rotateZ', lock = True, k = False) 
        
        for j in range(0, len(l_allFingers)):
            base.setAttr('CTRL_L_Finger_'+str(j)+'.scale'+axe, lock = True, k = False)
            base.setAttr('CTRL_R_Finger_'+str(j)+'.scale'+axe, lock = True, k = False)
            
            base.setAttr('CTRL_L_Finger_'+str(j)+'.translate'+axe, lock = True, k = False)            
            base.setAttr('CTRL_R_Finger_'+str(j)+'.translate'+axe, lock = True, k = False)
            
            #base.setAttr('CTRL_L_Finger_'+str(j)+'.rotateX', lock = True, k = False)            
            #base.setAttr('CTRL_L_Finger_'+str(j)+'.rotateY', lock = True, k = False)            
                        
            #base.setAttr('CTRL_R_Finger_'+str(j)+'.rotateX', lock = True, k = False)            
            #base.setAttr('CTRL_R_Finger_'+str(j)+'.rotateY', lock = True, k = False)            
            
            
            
               