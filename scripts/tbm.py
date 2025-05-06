"""
Script for the showing Cone handling
"""
from typing import List
import openpyxl
from openpyxl import Workbook

import math
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
import NemAll_Python_AllplanSettings as AllpanSetttings
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Utility as AllplanUtility
import NemAll_Python_Reinforcement as AllplanReinf
import GeometryValidate as GeometryValidate

from BuildingElement import BuildingElement
from BuildingElementMigrationUtil import BuildingElementMigrationUtil
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from HandleParameterData import HandleParameterData
from HandleParameterType import HandleParameterType
from PythonPartUtil import PythonPartUtil


import os
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


def check_allplan_version(build_ele: BuildingElement,
                          version  : float):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True



def create_element(build_ele: BuildingElement,
                   doc      : AllplanElementAdapter.DocumentAdapter):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document
    """

    element = Tbm(doc)

    return element.create(build_ele)


def move_handle(build_ele  : BuildingElement,
                handle_prop: HandleProperties,
                input_pnt  : AllplanGeo.Point3D,
                doc        : AllplanElementAdapter.DocumentAdapter):
    """
    Modify the element geometry by handles

    Args:
        build_ele:  the building element.
        handle_prop handle properties
        input_pnt:  input point
        doc:        input document
    """

    build_ele.change_property(handle_prop, input_pnt)

    return create_element(build_ele, doc)


class Tbm():
    """
    Definition of class Cone
    """

    def __init__(self, doc):
        """
        Initialization of class Cone

        Args:
            doc: input document
        """

        self.model_ele_list = []
        self.reinf_ele_list = []
        self.handle_list    = []
        self.document       = doc


    def create(self,
               build_ele: BuildingElement):
        """
        Create the elements

        Args:
            build_ele:  the building element.

        Returns:
            tuple  with created elements and handles.
        """
        self.create_cylinder(build_ele)

        return (self.model_ele_list, self.handle_list)

    def create_cylinder(self,
                      build_ele: BuildingElement):
        """
        Create the 3D tbm ring

        Args:
            build_ele:  the building element.
        """
        coords = []
        tempCoord = []
        #----------------- Extract palette parameter values
        com_prop = AllpanSetttings.AllplanGlobalSettings.GetCurrentCommonProperties()

        #----------------- Get ring configuration parameters
        numberKey = build_ele.numberKey.value
        numberSegment = build_ele.numberSegment.value
        keyDowel = build_ele.keyDowel.value
        segmentDowel = build_ele.segmentDowel.value

        #----------------- Get ring geometric parameters
        radius     = build_ele.ringDia.value/2
        thickness = build_ele.ringThickness.value
        baseWidth = build_ele.ringWidth.value
        taper = build_ele.taper.value

        #----------------- Calculate number of positions
        posNumber = numberKey * keyDowel + numberSegment * segmentDowel

        #----------------- Get joint and erection angle
        jointAngle = build_ele.jointAngle.value
        jointAngle = AllplanGeo.Angle.DegToRad(-jointAngle)
        jointAngle = AllplanGeo.Angle(jointAngle)
        antijointAngle = build_ele.jointAngle.value
        antijointAngle = AllplanGeo.Angle.DegToRad(antijointAngle)
        antijointAngle = AllplanGeo.Angle(antijointAngle)

        erectionAngle = build_ele.keyAngle.value
        erectionAngle = AllplanGeo.Angle.DegToRad(erectionAngle)
        erectionAngle = AllplanGeo.Angle(erectionAngle)

        #----------------- Create axis placement
        axis_placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0, 0, -baseWidth/2 - taper/2))

        #----------------- Create cylinder
        outercylinder = AllplanGeo.BRep3D.CreateCylinder(axis_placement,radius, 2*baseWidth)
        innercylinder = AllplanGeo.BRep3D.CreateCylinder(axis_placement,radius - thickness, 2*baseWidth)
        err, cylinder = AllplanGeo.MakeSubtraction(outercylinder, innercylinder)
        #----------------- Taper
        topP1 = AllplanGeo.Point3D(0, radius, baseWidth/2 - taper/2)
        topP2= AllplanGeo.Point3D(0, -radius, baseWidth/2 + taper/2)
        topP3 = AllplanGeo.Point3D(2*radius, -radius, baseWidth/2 + taper/2)
        taperPlaneTop = AllplanGeo.Plane3D(topP1,topP2,topP3)
        is_cut, above, cylinder = AllplanGeo.CutBrepWithPlane(cylinder, taperPlaneTop)

        botP1 = AllplanGeo.Point3D(0, radius, -baseWidth/2 + taper/2)
        botP2= AllplanGeo.Point3D(0, -radius, -baseWidth/2 - taper/2)
        botP3 = AllplanGeo.Point3D(2*radius , -radius, -baseWidth/2 - taper/2)
        taperPlaneBot = AllplanGeo.Plane3D(botP1,botP2,botP3)
        is_cut, cylinder, below = AllplanGeo.CutBrepWithPlane(cylinder, taperPlaneBot)

        #----------------- Division
        divAngle = (360/posNumber)
        keyrotationAngle = (divAngle/2) * keyDowel
        keyrotationAngle = AllplanGeo.Angle.DegToRad(-keyrotationAngle)
        keyrotationAngle = AllplanGeo.Angle(keyrotationAngle)

        rotationAngle = divAngle * segmentDowel
        rotationAngle = AllplanGeo.Angle.DegToRad(-rotationAngle)
        rotationAngle = AllplanGeo.Angle(rotationAngle)

        # ---------------- Indicate BIBLOCK locations(conditional)
        if build_ele.biblock.value == True:
            biblockAngle = AllplanGeo.Angle.DegToRad(-divAngle)
            biblockAngle = AllplanGeo.Angle(biblockAngle)
            halfbiblockAngle = AllplanGeo.Angle.DegToRad(-divAngle/2)
            halfbiblockAngle = AllplanGeo.Angle(halfbiblockAngle)
            if keyDowel % 2 == 0:
                bp2 = AllplanGeo.Point3D(0,radius-thickness/2,0)
                bp2 = AllplanGeo.Rotate(bp2, halfbiblockAngle)
            else:
                bp2 = AllplanGeo.Point3D(0,radius-thickness/2,0)
            biblockAxis = AllplanGeo.AxisPlacement3D(bp2)
            biblock = AllplanGeo.BRep3D.CreateCylinder(biblockAxis, 50, 1.03*baseWidth)
            biblock = AllplanGeo.Move(biblock, AllplanGeo.Vector3D(0,0,-(1.03*baseWidth)/2))
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, biblock))
            for i in range(1, posNumber):
                bp2 = AllplanGeo.Rotate(bp2, biblockAngle)
                biblockAxis = AllplanGeo.AxisPlacement3D(bp2)
                biblock = AllplanGeo.BRep3D.CreateCylinder(biblockAxis, 50, 1.03*baseWidth)
                biblock = AllplanGeo.Move(biblock, AllplanGeo.Vector3D(0,0,-(1.03*baseWidth)/2))
                self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, biblock))

        #----------------- Arrange points and planes for segment cutting before loop
        p1 = AllplanGeo.Point3D(0,0,0)
        p2 = AllplanGeo.Point3D(0,2*(radius-thickness/2),0)
        p3 = AllplanGeo.Point3D(0,2*(radius-thickness/2),baseWidth)
        zVector = AllplanGeo.Vector3D(0,0,baseWidth)
        zAxis = AllplanGeo.Axis3D(p1, zVector)
        p2 = AllplanGeo.Rotate(p2, zAxis, keyrotationAngle)
        p3 = AllplanGeo.Rotate(p3, zAxis, keyrotationAngle)

        mirror1 = AllplanGeo.Point3D(0, -radius, 0)
        mirror2 = AllplanGeo.Point3D(0, radius, 0)
        mirror3 = AllplanGeo.Point3D(0, 0, radius)
        mirrorplane = AllplanGeo.Plane3D(mirror1, mirror2, mirror3)

        halfRingCut = AllplanGeo.CutBrepWithPlane(cylinder, mirrorplane)
        xPoint = AllplanGeo.Point3D(2*radius, 0, 0)
        yPoint = AllplanGeo.Point3D(0, 0, 0)
        zPoint = AllplanGeo.Point3D(0, 0, baseWidth)
        xPlane = AllplanGeo.Plane3D(xPoint, yPoint, zPoint)
        keyHalfRingCut = AllplanGeo.CutBrepWithPlane(cylinder, xPlane)

        if numberSegment % 2 == 0:
            loopcount = (numberSegment) / 2
        else:
            loopcount = ((numberSegment - 1) / 2) + 1

        for i in range(1,int(loopcount)+1):
            if i == 1:
                jointvector = AllplanGeo.Vector3D(p1, p2)
                jointaxis = AllplanGeo.Axis3D(p1, jointvector)
                pN2 = AllplanGeo.Point3D(0, radius-thickness/2, 0)
                pN2 = AllplanGeo.Rotate(pN2, zAxis, keyrotationAngle)
                pN3 = AllplanGeo.Point3D(0, radius-thickness/2, baseWidth)
                pN3 = AllplanGeo.Rotate(pN3, zAxis, keyrotationAngle)
                coord = AllplanGeo.Point3D.GetCoords(pN2)
                coordZ = AllplanGeo.Point3D(coord[0], coord[1], 1)
                keyzVector = AllplanGeo.Vector3D(pN2, coordZ)
                keyzAxis = AllplanGeo.Axis3D(pN2, keyzVector)
                pN1 = AllplanGeo.Rotate(p1, keyzAxis, erectionAngle)
                pN3 = AllplanGeo.Rotate(p3, keyzAxis, erectionAngle)
                pN1 = AllplanGeo.Rotate(pN1, jointaxis, jointAngle)
                pN3 = AllplanGeo.Rotate(pN3, jointaxis, jointAngle)
                mp1 = AllplanGeo.Mirror(pN1, mirrorplane)
                mp2 = AllplanGeo.Mirror(pN2, mirrorplane)
                mp3 = AllplanGeo.Mirror(pN3, mirrorplane)
                jointPlane = AllplanGeo.Plane3D(pN1, pN2, pN3)
                mrjointplane = AllplanGeo.Plane3D(mp1, mp2, mp3)
                pN1 = AllplanGeo.Rotate(pN1, jointaxis, antijointAngle)
                pN3 = AllplanGeo.Rotate(pN3, jointaxis, antijointAngle)
                result = AllplanGeo.CutBrepWithPlane(keyHalfRingCut[1], jointPlane)
                mrresult = AllplanGeo.CutBrepWithPlane(result[2], mrjointplane)

                #----------------- Get Intersection Coordinates
                coordSolid = AllplanGeo.CutBrepWithPlane(halfRingCut[1], jointPlane)
                err, coor = AllplanGeo.BRep3D.GetVertices(coordSolid[1])
                for j in range(len(coor)):
                    coordIndex = list(AllplanGeo.Point3D.GetCoords(coor[j])) + ['0 / 1',]
                    tempCoord.append(coordIndex)
                tempCoord = sorted(tempCoord, key=lambda x: x[2], reverse=True)
                coords.extend(tempCoord)
                tempCoord.clear()

                mrcoordSolid = AllplanGeo.CutBrepWithPlane(halfRingCut[2], mrjointplane)
                err, coor = AllplanGeo.BRep3D.GetVertices(mrcoordSolid[1])
                for j in range(len(coor)):
                    coordIndex = list(AllplanGeo.Point3D.GetCoords(coor[j])) + ['0 / -1',]
                    tempCoord.append(coordIndex)
                tempCoord = sorted(tempCoord, key=lambda x: x[2], reverse=True)
                coords.extend(tempCoord)
                tempCoord.clear()


                #----------------- Check Erection Tolerance (conditional)
                if build_ele.keyErection.value == True:
                    erectionVector = AllplanGeo.Vector3D(0,0,-build_ele.erectionDistance.value)
                    key = mrresult[1]
                    key = AllplanGeo.Move(mrresult[1], erectionVector)
                    self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, key))
                else:
                    key = mrresult[1]
                    self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, key))

                continue

            if i == 2:
                result1 = AllplanGeo.CutBrepWithPlane(halfRingCut[1], jointPlane)
                mrresult1 = AllplanGeo.CutBrepWithPlane(halfRingCut[2], mrjointplane)
            else:
                jointvector = AllplanGeo.Vector3D(p1, p2)
                jointaxis = AllplanGeo.Axis3D(p1, jointvector)
                p3 = AllplanGeo.Rotate(p3, jointaxis, jointAngle)
                mp2 = AllplanGeo.Mirror(p2, mirrorplane)
                mp3 = AllplanGeo.Mirror(p3, mirrorplane)
                jointPlane1 = AllplanGeo.Plane3D(p1, p2, p3)
                mrjointPlane1 = AllplanGeo.Plane3D(p1, mp2, mp3)
                p3 = AllplanGeo.Rotate(p3, jointaxis, antijointAngle)
                result1 = AllplanGeo.CutBrepWithPlane(halfRingCut[1], jointPlane1)
                mrresult1 = AllplanGeo.CutBrepWithPlane(halfRingCut[2], mrjointPlane1)

            p2 = AllplanGeo.Rotate(p2, zAxis, rotationAngle)
            p3 = AllplanGeo.Rotate(p3, zAxis, rotationAngle)
            jointvector = AllplanGeo.Vector3D(p1, p2)
            jointaxis = AllplanGeo.Axis3D(p1, jointvector)
            p3 = AllplanGeo.Rotate(p3, jointaxis, jointAngle)
            mp2 = AllplanGeo.Mirror(p2, mirrorplane)
            mp3 = AllplanGeo.Mirror(p3, mirrorplane)
            jointPlane2 = AllplanGeo.Plane3D(p1, p2, p3)
            mrjointPlane2 = AllplanGeo.Plane3D(p1, mp2, mp3)
            p3 = AllplanGeo.Rotate(p3, jointaxis, antijointAngle)

            result2 = AllplanGeo.CutBrepWithPlane(result1[1], jointPlane2)
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, result2[2]))
            mrresult2 = AllplanGeo.CutBrepWithPlane(mrresult1[2], mrjointPlane2)
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, mrresult2[1]))

            #----------------- Get Intersection Coordinates
            coordSolid = AllplanGeo.CutBrepWithPlane(halfRingCut[1], jointPlane2)
            err, coor = AllplanGeo.BRep3D.GetVertices(coordSolid[1])
            for j in range(len(coor)):
                coordIndex = list(AllplanGeo.Point3D.GetCoords(coor[j])) + [str(i-1)+' / '+str(i),]
                tempCoord.append(coordIndex)
            tempCoord = sorted(tempCoord, key=lambda x: x[2], reverse=True)
            coords.extend(tempCoord)
            tempCoord.clear()

            mrcoordSolid = AllplanGeo.CutBrepWithPlane(halfRingCut[2], mrjointPlane2)
            err, coor = AllplanGeo.BRep3D.GetVertices(mrcoordSolid[1])
            for j in range(len(coor)):
                coordIndex = list(AllplanGeo.Point3D.GetCoords(coor[j])) + [str(-i+1)+' / '+str(-i),]
                tempCoord.append(coordIndex)
            tempCoord = sorted(tempCoord, key=lambda x: x[2], reverse=True)
            coords.extend(tempCoord)
            tempCoord.clear()

            if i == loopcount:
                if numberSegment % 2 == 0:
                    jointvector = AllplanGeo.Vector3D(p1, p2)
                    jointaxis = AllplanGeo.Axis3D(p1, jointvector)
                    p3 = AllplanGeo.Rotate(p3, jointaxis, jointAngle)
                    mp2 = AllplanGeo.Mirror(p2, mirrorplane)
                    mp3 = AllplanGeo.Mirror(p3, mirrorplane)
                    jointPlane1 = AllplanGeo.Plane3D(p1, p2, p3)
                    mrjointPlane1 = AllplanGeo.Plane3D(p1, mp2, mp3)
                    p3 = AllplanGeo.Rotate(p3, jointaxis, antijointAngle)
                    result1 = AllplanGeo.CutBrepWithPlane(keyHalfRingCut[2], jointPlane1)
                    mrresult1 = AllplanGeo.CutBrepWithPlane(keyHalfRingCut[2], mrjointPlane1)

                    p2 = AllplanGeo.Rotate(p2, zAxis, rotationAngle)
                    p3 = AllplanGeo.Rotate(p3, zAxis, rotationAngle)
                    jointvector = AllplanGeo.Vector3D(p1, p2)
                    jointaxis = AllplanGeo.Axis3D(p1, jointvector)
                    p3 = AllplanGeo.Rotate(p3, jointaxis, antijointAngle)
                    jointPlane2 = AllplanGeo.Plane3D(p1, p2, p3)

                    result2 = AllplanGeo.CutBrepWithPlane(result1[1], jointPlane2)
                    self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, result2[2]))
                    mrresult2 = AllplanGeo.CutBrepWithPlane(mrresult1[2], jointPlane2)
                    self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, mrresult2[1]))

                    #----------------- Get Intersection Coordinates
                    coordSolid = AllplanGeo.CutBrepWithPlane(keyHalfRingCut[1], jointPlane2)
                    err, coor = AllplanGeo.BRep3D.GetVertices(coordSolid[1])
                    for j in range(len(coor)):
                        coordIndex = list(AllplanGeo.Point3D.GetCoords(coor[j])) + [str(i)+' / '+str(-i),]
                        tempCoord.append(coordIndex)
                    tempCoord = sorted(tempCoord, key=lambda x: x[2], reverse=True)
                    coords.extend(tempCoord)
                    tempCoord.clear()

                else:
                    counterkey = AllplanGeo.MakeUnion(mrresult2[2], result2[1])
                    self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, counterkey[1]))

        if build_ele.coordVertices.value == True:
            temp_list = [y for y in coords if abs(y[1]) > 0.000001]
            coords_list = [y for y in temp_list if abs(y[0]) > 0.000001]

            wb = openpyxl.Workbook()
            ws = wb.active
            file_name = "TBM Coordinates.xlsx"
            file_path = os.path.join(desktop_path, file_name)
            for row in coords_list:
                ws.append(row)
            wb.save(file_path)

        #startangle = AllplanGeo.Angle.DegToRad(0)
        #endangle = AllplanGeo.Angle.DegToRad(270)
        #axis_placement = AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0,0,0))
        #p1= AllplanGeo.Point3D(0,0,0)
        #p2= AllplanGeo.Point3D(1000,0,0)
        #line = AllplanGeo.Line3D(p1,p2)
        #arc = AllplanGeo.Arc3D(AllplanGeo.Point3D(0,0,0),AllplanGeo.Vector3D(1,0,0),AllplanGeo.Vector3D(0,0,1),1000,1000, startangle, endangle, True)
#
        #rresult= AllplanGeo.CutBrepWithPlane(arc, xPlane)
        #self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, rresult[1]))
        #pyp_util = PythonPartUtil()
#
        #pyp_util.add_pythonpart_view_2d3d(AllplanBasisElements.ModelElement3D(com_prop, cylinder))
#
        #self.model_ele_list = pyp_util.create_pythonpart(build_ele)
        #self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, cylinder))
        #self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, below))
