import maya.cmds as base
import Locators
import Joints
import SecondaryLocators

Locators = reload(Locators)
Joints = reload(Joints)
SecondaryLocators = reload(SecondaryLocators)
global selected
base.window("Auto Rigger")

base.rowColumnLayout(nc = 1)

Locators.createFields()
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

base.showWindow()
