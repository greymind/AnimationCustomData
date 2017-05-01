'''
Custom Data Exporter for Maya

(c) 2009 - 2011
    Balakrishnan Ranganathan (balki_live_com)
    All Rights Reserved.
'''

from Common import *

global xmlDocument
global exportPath
global exportFbx
global outputFilePathTextField

def Traverse(node, parentXmlNode):
    '''
    Traverse the maya full-path node and attach it to the parentXmlNode
    '''
    global xmlDocument
    children = Cmds.listRelatives([node], children=True)

    '''
    print "\nNode: " + str(node)
    print "Children: " + str(children)
    print "Node type: " + Cmds.nodeType(node)
    print "Attributes: " + str(Cmds.listAttr(node))
    '''

    print node
    nodeName = node.split("|")[-1]
    nodeType = Cmds.nodeType(node)
    
    xmlNode = xmlDocument.createElement("CustomData")
    xmlNode.setAttribute("Name", nodeName)
        
    if nodeType in ["node", "transform"]:
        #CreateTransformNodes(node, xmlNode)
		Nop
    elif nodeType in ["joint"]:
        CreateTransformNodes(nodeName, xmlNode)
    elif nodeType in ["pointConstraint"]:
        targetList = Cmds.pointConstraint(nodeName, q=True, tl=True)
        weightAliasList = Cmds.pointConstraint(nodeName, q=True, wal=True)
        if targetList != None:
            xmlTargetListNode = xmlDocument.createElement("TargetList")
            xmlNode.appendChild(xmlTargetListNode)
            for i in range(0, len(targetList)):
                target = targetList[i]
                weightAlias = weightAliasList[i]
                xmlTargetNode = xmlDocument.createElement("Target")
                xmlTargetListNode.appendChild(xmlTargetNode)
                xmlTargetNode.setAttribute("Name", target)
                xmlTargetNode.setAttribute("Weight", str(Cmds.getAttr(nodeName + "." + weightAlias)))
    elif nodeType in ["orientConstraint"]:
        targetList = Cmds.orientConstraint(nodeName, q=True, tl=True)
        weightAliasList = Cmds.orientConstraint(nodeName, q=True, wal=True)
        if targetList != None:
            xmlTargetListNode = xmlDocument.createElement("TargetList")
            xmlNode.appendChild(xmlTargetListNode)
            for i in range(0, len(targetList)):
                target = targetList[i]
                weightAlias = weightAliasList[i]
                xmlTargetNode = xmlDocument.createElement("Target")
                xmlTargetListNode.appendChild(xmlTargetNode)
                xmlTargetNode.setAttribute("Name", target)
                xmlTargetNode.setAttribute("Weight", str(Cmds.getAttr(nodeName + "." + weightAlias)))

    xmlNode.setAttribute("MayaType", nodeType)
    parentXmlNode.appendChild(xmlNode)

    if children != None:
        xmlChildrenNode = xmlDocument.createElement("CustomDataCollection")
        xmlNode.appendChild(xmlChildrenNode)
        for child in children:
            Traverse(node + "|" + child, xmlChildrenNode)

def ExportCustomDataNode(xmlParentNode, name, value):
    xmlCustomDataNode = xmlDocument.createElement("CustomData")
    xmlParentNode.appendChild(xmlCustomDataNode)
    xmlCustomDataNode.setAttribute("Name", name)
    xmlCustomDataNode.setAttribute("Value", str(value))

def ExportAttributeAsCustomData(xmlParentNode, name, attributeName):
    customData = ""
    if Cmds.objExists(attributeName):
        customData = Cmds.getAttr(attributeName)
    
    if IsNoneOrEmpty(str(customData)):
        Cmds.confirmDialog(title="Custom Data Exporter for Maya", message="Warning: %s is None or Empty!" % attributeName, button=["Doh!"])
        sys.exit()
    
    ExportCustomDataNode(xmlParentNode, name, customData)

def CreateCustomAttributes():
    Cmds.select(cl=True)
    #Cmds.group(em=True, name="CustomData")
    if not Cmds.objExists("CustomData.Scale"):
        Cmds.addAttr("CustomData", longName="Scale", at="double", keyable=True)
        Cmds.setAttr("CustomData.Scale", 1)
    if not Cmds.objExists("CustomData.IdleAnimation"):
        Cmds.addAttr("CustomData", longName="IdleAnimation", dt="string", keyable=True)
    if not Cmds.objExists("CustomData.ChestJoint"):
        Cmds.addAttr("CustomData", longName="ChestJoint", dt="string", keyable=True)
    if not Cmds.objExists("CustomData.NeckJoint"):
        Cmds.addAttr("CustomData", longName="NeckJoint", dt="string", keyable=True)
    if not Cmds.objExists("CustomData.LeftToeJoint"):
        Cmds.addAttr("CustomData", longName="LeftToeJoint", dt="string", keyable=True)
    if not Cmds.objExists("CustomData.RightToeJoint"):
        Cmds.addAttr("CustomData", longName="RightToeJoint", dt="string", keyable=True)
        
def ExportCustomAttributes(parentXmlNode):
    ExportAttributeAsCustomData(parentXmlNode, "IdleAnimation", "CustomData.IdleAnimation")
    ExportAttributeAsCustomData(parentXmlNode, "Scale", "CustomData.Scale")
    ExportAttributeAsCustomData(parentXmlNode, "ChestJoint", "CustomData.ChestJoint")
    ExportAttributeAsCustomData(parentXmlNode, "NeckJoint", "CustomData.NeckJoint")
    ExportAttributeAsCustomData(parentXmlNode, "LeftToeJoint", "CustomData.LeftToeJoint")
    ExportAttributeAsCustomData(parentXmlNode, "RightToeJoint", "CustomData.RightToeJoint")
    
def ExportMoves(parentXmlNode):
    xmlMovesNode = xmlDocument.createElement("CustomData")
    parentXmlNode.appendChild(xmlMovesNode)
    xmlMovesNode.setAttribute("Name", "MoveLister")
    
    xmlMoveNode = xmlDocument.createElement("CustomDataCollection")
    xmlMovesNode.appendChild(xmlMoveNode)
    
    totalMovesNode = "MoveLister.totalMoves"
    totalMoves = Cmds.getAttr(totalMovesNode)
    ExportCustomDataNode(xmlMoveNode, totalMovesNode, str(totalMoves))
    
    minFrame = 100000
    maxFrame = -1
    for i in range(0, totalMoves):
        nodePrefix = "MoveLister.move" + str(i)

        moveNameNode = nodePrefix + "Name"
        moveName = Cmds.getAttr(moveNameNode)
        ExportCustomDataNode(xmlMoveNode, moveNameNode, str(moveName))
        
        moveMinNode = nodePrefix + "Min"
        moveMin = Cmds.getAttr(moveMinNode)
        ExportCustomDataNode(xmlMoveNode, moveMinNode, str(moveMin))
        
        minFrame = min(minFrame, moveMin)
        
        moveMaxNode = nodePrefix + "Max"
        moveMax = Cmds.getAttr(moveMaxNode)
        ExportCustomDataNode(xmlMoveNode, moveMaxNode, str(moveMax))
        
        maxFrame = max(maxFrame, moveMax)
        
    return [minFrame, maxFrame]

def FbxExport():
    fbxExport = 'FBXExportInAscii -v true'
    Mel.eval(fbxExport)

    fbxExport = 'FBXExportLights -v false'
    Mel.eval(fbxExport)

    fbxExport = 'FBXExportCameras -v false'
    Mel.eval(fbxExport)
    
    meshFilePath = os.path.splitext(os.path.basename(Cmds.file(q=True, sn=True)))[0] + ".fbx"
    fbxExport = 'FBXExport -f "' + meshFilePath + '" -s'
    Mel.eval(fbxExport)
        
def Main(filePath):
    global xmlDocument
    global exportPath
    global exportFbx

    xmlDocument = Dom.Document()
    rootXmlElement = xmlDocument.createElement("CustomData")
    rootXmlElement.setAttribute("version", "0.3")
    xmlDocument.appendChild(rootXmlElement)

    xmlNodesElement = xmlDocument.createElement("CustomDataCollection")
    rootXmlElement.appendChild(xmlNodesElement)

    rootNode = u"|CustomData"
    if not Cmds.objExists(rootNode):
        print "\n\nError: Please provide a root node (group) in maya named 'CustomData' so the exporter can know what objects to process."
        Cmds.confirmDialog(title="Custom Data Exporter for Maya", message="Please provide a root node (group) in maya named 'CustomData' so the exporter can know what objects to export.", button=["Ooh!"])
    else:
        Traverse(rootNode, xmlNodesElement)
        frames = ExportMoves(xmlNodesElement)
        ExportCustomAttributes(xmlNodesElement)
        
        directoryName = os.path.dirname(Cmds.file(q=True, sn=True))
        filePath = "%s/%s" % (directoryName, filePath)
        rootXmlElement.writexml(open(filePath, "w"), "", "\t", "\n")
        if exportFbx == True:
            Bake(frames[0], frames[1])
            FbxExport()
            Cmds.undo()
            Cmds.undo()
        print "\n\n\nExport complete."
        Cmds.confirmDialog(title="Custom Data Exporter for Maya", message="Export complete!", button=["Yay!"])

def ExportCustomData(*args):
    '''
    Pass the desired output path to Main
    '''
    global outputFilePathTextField
    
    Main(Cmds.textField(outputFilePathTextField, query=True, text=True))
    
def CreateCustomData(*args):
    Cmds.select(cl=True)
    
    baseNode = u'|CustomData'
    
    if not Cmds.objExists(baseNode):
        Cmds.group(em=True, name=baseNode)

    if not Cmds.objExists("%s|Sequencer" % baseNode):
        Cmds.group(em=True, name="Sequencer", parent=baseNode)
    
    if not Cmds.objExists("%s|FirstPersonCamera_Head" % baseNode) and not Cmds.objExists("%s|FirstPersonCamera_Tail" % baseNode):
        Cmds.select(baseNode, r=True)
        Cmds.joint(n="FirstPersonCamera_Head")
        Cmds.joint(n="FirstPersonCamera_Tail", p=(0, 0, 0))
        Cmds.select(cl=True)

    if not Cmds.objExists("%s|CharacterForward_Head" % baseNode) and not Cmds.objExists("%s|CharacterForward_Tail" % baseNode):
        Cmds.select(baseNode, r=True)
        Cmds.joint(n="CharacterForward_Head")
        Cmds.joint(n="CharacterForward_Tail", p=(0, 0, 0))
        Cmds.select(cl=True)
        
    if not Cmds.objExists("%s|Grenade_Head" % baseNode) and not Cmds.objExists("%s|Grenade_Tail" % baseNode):
        Cmds.select(baseNode, r=True)
        Cmds.joint(n="Grenade_Head")
        Cmds.joint(n="Grenade_Tail", p=(0, 0, 0))
        Cmds.select(cl=True)
    
    CreateCustomAttributes()
    
def Run(eFbx = True):
    '''
    Create UI Window
    '''
    global exportFbx
    global outputFilePathTextField
    exportFbx = eFbx
    
    window = Cmds.window(title="Custom Data Exporter for Maya", widthHeight=(500, 100))
    Cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, "left", 1), columnWidth=[(1, 125), (2, 350)] )
    Cmds.text(label="Output file path")
    outputFilePathTextField = Cmds.textField()
    Cmds.textField(outputFilePathTextField, edit=True, text="CustomData.xml")
    Cmds.button(label="Export custom data file", command=ExportCustomData)
    Cmds.button(label="Create custom data nodes", command=CreateCustomData)
    Cmds.text(label="Warning: Remember that a freeze for scale and rotation takes place.")
    Cmds.showWindow(window)
