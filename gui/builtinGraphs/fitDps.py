#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from gui.graph import Graph
import service
from gui import bitmapLoader
from eos.graph.fitDps import FitDpsGraph as FitDps
from eos.graph import Data
import gui.mainFrame
import service

class FitDpsGraph(Graph):
    propertyAttributeMap = {"angle": "maxVelocity",
                            "distance": "maxRange",
                            "signatureRadius": "signatureRadius"
                            }

    propertyLabelMap = {"angle": "Target Angle (degrees)",
                        "distance": "Distance to Target (km)",
                        "signatureRadius": "Target Signature Radius (m)"
                        }

    defaults = FitDps.defaults.copy()

    def __init__(self):
        Graph.__init__(self)
        self.defaults["distance"] = "0-20"
        self.defaults["signatureRadius"] = 195;
        self.name = "DPS"
        self.fitDps = None
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getFields(self):
        return self.defaults

    def getLabels(self):
        return self.propertyLabelMap

    def getIcons(self):
        icons = {}
        sFit = service.Attribute.getInstance()
        for key, attrName in self.propertyAttributeMap.iteritems():
            iconFile = sFit.getAttributeInfo(attrName).icon.iconFile
            bitmap = bitmapLoader.getBitmap(iconFile, "pack")
            if bitmap:
                icons[key] = bitmap

        return icons

    '''
    Will return a 2d matrix of dmg over distance and transversal.
    
    range is given in meters.
    '''
    def getDpsMatrix(self, fit, signature, rangeMax, rangeStep, transversalMax, transStep):
        fitDps = getattr(self, "fitDps", None)
        if fitDps is None or fitDps.fit != fit:
            fitDps = self.fitDps = FitDps(fit)
        
        from eos.graph import Graph, Data
        from eos.types import Hardpoint, State
        from math import log, sin, radians
               
        dpsMatrix = [];        
        for dist in xrange(1, rangeMax, rangeStep):
            transArray = []
            for trans in xrange(1, transversalMax, transStep):
                total = 0               
                for mod in fit.modules:
                    if mod.hardpoint == Hardpoint.TURRET:
                        if mod.state >= State.ACTIVE:
                            total += mod.dps * self._calcTurrentDmg(mod, dist, trans, signature)
        
                transArray.append(total);
            dpsMatrix.append(transArray);

        
        return dpsMatrix;
    
    '''
    This should be in EOS
    Calculates turrent dmg based on range and transversal, returns dps
    '''
    def _calcTurrentDmg(self, mod, range, trans, targetSig):
        tracking = mod.getModifiedItemAttr("trackingSpeed")
        turretOptimal = mod.maxRange
        turretFalloff = mod.falloff
        turretSigRes = mod.getModifiedItemAttr("optimalSigRadius")
        targetSigRad = targetSig;
        targetSigRad = turretSigRes if targetSigRad is None else targetSigRad
        transversal = trans; #sin(radians(data["angle"])) * data["velocity"]
         
        trackingEq = (((transversal / (range * tracking)) *
                       (turretSigRes / targetSigRad)) ** 2)
        rangeEq = ((max(0, range - turretOptimal)) / turretFalloff) ** 2
        
        chanceToHit = 0.5 ** (trackingEq + rangeEq);
        
        if chanceToHit > 0.01:
            #AvgDPS = Base Damage * [ ( ChanceToHit^2 + ChanceToHit + 0.0499 ) / 2 ]
            return (chanceToHit ** 2 + chanceToHit + 0.0499) / 2
        else:
            #All hits are wreckings
            return chanceToHit * 3
        
    
    def getPoints(self, fit, fields):
        fitDps = getattr(self, "fitDps", None)
        if fitDps is None or fitDps.fit != fit:
            fitDps = self.fitDps = FitDps(fit)

        fitDps.clearData()
        variable = None
        for fieldName, value in fields.iteritems():
            d = Data(fieldName, value)
            if not d.isConstant():
                if variable is None:
                    variable = fieldName
                else:
                    #We can't handle more then one variable atm, OOPS FUCK OUT
                    return False, "Can only handle 1 variable"

            fitDps.setData(d)

        if variable is None:
            return False, "No variable"

        x = []
        y = []
        for point, val in fitDps.getIterator():
            x.append(point[variable])
            y.append(val)

        return x, y

FitDpsGraph.register()
