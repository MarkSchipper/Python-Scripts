import maya.cmds as base
import Locators
import Joints
import SecondaryLocators

# we reload all classes when this file is executed, else we would need to restart Maya after every change
Locators = reload(Locators)
Joints = reload(Joints)
SecondaryLocators = reload(SecondaryLocators)
global selected

###########################################
#         Create the basic window        ##
###########################################

# Create a window with the name Auto Rigger

base.window("Auto Rigger")

# set the layout of the window
base.rowColumnLayout(nc = 1)

# Call the createFields function in the Locators file
Locators.createFields()
# separate the fields
base.separator(h = 5)
base.button(l = "Create Base Locators", w = 200, c = "Locators.CreateLocators()")
base.separator(h = 10)
base.button(l = "Create Secondary Locators", w = 200, c = "SecondaryLocators.CreateSecLocatorWindows()")
base.separator(h = 10)
base.button(l = "Delete All Locators", w = 200, c = "Locators.deleteLocators()")
base.separator(h = 10)
base.button(l = "Mirror L->R", w = 200, c = "Locators.mirrorLocators()")
base.separator(h = 15)
base.button(l = "Create Joints", w = 200, c = "Joints.CreateJointsWindow()")

base.separator(h = 20)
base.separator()

# show the actual window
base.showWindow()
