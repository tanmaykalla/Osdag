"""
Initialized on 23-04-2019
Commenced on 24-04-2019
@author: Anand Swaroop
"""""

import numpy


class ExtendedBothWays(object):

    def __init__(self, beamLeft, beamRight, plateRight, nut_bolt_array, bbWeldAbvFlang_21, bbWeldAbvFlang_22,
                 bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23, bbWeldBelwFlang_24, bbWeldSideWeb_21, bbWeldSideWeb_22):

        # Initializing the arguments
        self.beamLeft = beamLeft                            # beamLeft frepresents the column
        self.beamRight = beamRight
        self.plateRight = plateRight
        self.nut_bolt_array = nut_bolt_array
        self.beamRight.length = 1000.0


        # Weld above flange for left and right beam
        self.bbWeldAbvFlang_21 = bbWeldAbvFlang_21      # Right beam upper side
        self.bbWeldAbvFlang_22 = bbWeldAbvFlang_22      # Right beam lower side

        self.bbWeldBelwFlang_21 = bbWeldBelwFlang_21    # behind bbWeldBelwFlang_11
        self.bbWeldBelwFlang_22 = bbWeldBelwFlang_22    # behind bbWeldBelwFlang_12
        self.bbWeldBelwFlang_23 = bbWeldBelwFlang_23    # behind bbWeldBelwFlang_13
        self.bbWeldBelwFlang_24 = bbWeldBelwFlang_24    # behind bbWeldBelwFlang_14


        self.bbWeldSideWeb_21 = bbWeldSideWeb_21        # Behind bbWeldSideWeb_11
        self.bbWeldSideWeb_22 = bbWeldSideWeb_22        # Behind bbWeldSideWeb_12
        #



    def create_3DModel(self):
        """
        :return: CAD model of each entity such as Left beam, right beam, both end plates and so on
        """
        self.createBeamLGeometry()
        self.createBeamRGeometry()
        self.createPlateRGeometry()
        self.create_nut_bolt_array()

        self.create_bbWeldAbvFlang_21()          #left beam above flange weld
        self.create_bbWeldAbvFlang_22()          #left beam above 2nd (lower) flange

        self.create_bbWeldBelwFlang_21()            #right beam weld similar to left beam
        self.create_bbWeldBelwFlang_22()
        self.create_bbWeldBelwFlang_23()
        self.create_bbWeldBelwFlang_24()

        self.create_bbWeldSideWeb_21()              #right beam weld behind left beam
        self.create_bbWeldSideWeb_22()            #right beam weld behind left beam


        # call for create_model of filletweld from Components directory
        self.beamLModel = self.beamLeft.create_model()
        self.beamRModel = self.beamRight.create_model()
        self.plateRModel = self.plateRight.create_model()
        self.nutBoltArrayModels = self.nut_bolt_array.create_model()

        self.bbWeldAbvFlang_21Model = self.bbWeldAbvFlang_21.create_model()
        self.bbWeldAbvFlang_22Model = self.bbWeldAbvFlang_22.create_model()

        self.bbWeldBelwFlang_21Model = self.bbWeldBelwFlang_21.create_model()
        self.bbWeldBelwFlang_22Model = self.bbWeldBelwFlang_22.create_model()
        self.bbWeldBelwFlang_23Model = self.bbWeldBelwFlang_23.create_model()
        self.bbWeldBelwFlang_24Model = self.bbWeldBelwFlang_24.create_model()

        self.bbWeldSideWeb_21Model = self.bbWeldSideWeb_21.create_model()
        self.bbWeldSideWeb_22Model = self.bbWeldSideWeb_22.create_model()

#############################################################################################################
#   Following functions takes inputs as origin, u direction and w direction of concerned component to place #
#   same component at appropriate place                                                                     #
#############################################################################################################

    def createBeamLGeometry(self):
        beamOriginL = numpy.array([0.0,0.0,0.0 ])
        beamL_uDir = numpy.array([1.0, 0.0, 0.0])
        beamL_wDir = numpy.array([0.0, 0.0, 1.0])
        self.beamLeft.place(beamOriginL, beamL_uDir, beamL_wDir)

    def createBeamRGeometry(self):
        gap = self.beamRight.D /2  +  self.plateRight.T
        beamOriginR = numpy.array([0.0, gap, self.beamLeft.length /2 ])
        beamR_uDir = numpy.array([1.0, 0.0, 0.0])
        beamR_wDir = numpy.array([0.0, 1.0, 0.0])
        self.beamRight.place(beamOriginR, beamR_uDir, beamR_wDir)

    def createPlateRGeometry(self):
        gap = 0.5 * self.plateRight.T + self.beamRight.D/2
        plateOriginR = numpy.array([-self.plateRight.W/2, gap, self.beamLeft.length /2 ])
        plateR_uDir = numpy.array([0.0, 1.0, 0.0])
        plateR_wDir = numpy.array([1.0, 0.0, 0.0])
        self.plateRight.place(plateOriginR, plateR_uDir, plateR_wDir)

    def create_nut_bolt_array(self):
        nutboltArrayOrigin = self.plateRight.sec_origin + numpy.array([0.0,  self.beamRight.T/2, self.plateRight.L/2])
        gaugeDir = numpy.array([1.0, 0, 0])
        pitchDir = numpy.array([0, 0, -1.0])
        boltDir = numpy.array([0, -1.0, 0])
        self.nut_bolt_array.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)

    def create_bbWeldAbvFlang_21(self):
        weldAbvFlangOrigin_21 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.D/2 +  self.plateRight.T, self.beamLeft.length / 2 +self.beamRight.D/2])
        uDirAbv_21 = numpy.array([0, 1.0, 0])
        wDirAbv_21 = numpy.array([1.0, 0, 0])
        self.bbWeldAbvFlang_21.place(weldAbvFlangOrigin_21, uDirAbv_21, wDirAbv_21)

    def create_bbWeldAbvFlang_22(self):
        weldAbvFlangOrigin_22 = numpy.array([self.beamLeft.B / 2, self.beamLeft.D/2 +  self.plateRight.T, self.beamLeft.length / 2 -self.beamRight.D/2 ])
        uDirAbv_22 = numpy.array([0, 1.0, 0])
        wDirAbv_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldAbvFlang_22.place(weldAbvFlangOrigin_22, uDirAbv_22, wDirAbv_22)


    def create_bbWeldBelwFlang_21(self):
        weldBelwFlangOrigin_21 = numpy.array([-self.beamLeft.t / 2, self.beamLeft.D/2 +  self.plateRight.T,  self.beamLeft.length / 2 +(self.beamLeft.D / 2) -
                                              self.beamLeft.T])
        uDirBelw_21 = numpy.array([0, 1.0, 0])
        wDirBelw_21 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_21.place(weldBelwFlangOrigin_21, uDirBelw_21, wDirBelw_21)

    def create_bbWeldBelwFlang_22(self):
        weldBelwFlangOrigin_22 = numpy.array([self.beamLeft.B / 2, self.beamLeft.D/2 +  self.plateRight.T,  self.beamLeft.length / 2+(self.beamLeft.D / 2) -
                                              self.beamLeft.T])
        uDirBelw_22 = numpy.array([0, 1.0, 0])
        wDirBelw_22 = numpy.array([-1.0, 0, 0])
        self.bbWeldBelwFlang_22.place(weldBelwFlangOrigin_22, uDirBelw_22, wDirBelw_22)

    def create_bbWeldBelwFlang_23(self):
        weldBelwFlangOrigin_23 = numpy.array([-self.beamLeft.B / 2, self.beamLeft.D/2 +  self.plateRight.T,  self.beamLeft.length / 2 -(self.beamLeft.D / 2) +
                                              self.beamLeft.T])
        uDirBelw_23 = numpy.array([0, 1.0, 0])
        wDirBelw_23 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_23.place(weldBelwFlangOrigin_23, uDirBelw_23, wDirBelw_23)

    def create_bbWeldBelwFlang_24(self):
        weldBelwFlangOrigin_24 = numpy.array([self.beamLeft.t / 2,self.beamLeft.D/2 +  self.plateRight.T,  self.beamLeft.length / 2-(self.beamLeft.D / 2) +
                                              self.beamLeft.T])
        uDirBelw_24 = numpy.array([0, 1.0, 0])
        wDirBelw_24 = numpy.array([1.0, 0, 0])
        self.bbWeldBelwFlang_24.place(weldBelwFlangOrigin_24, uDirBelw_24, wDirBelw_24)

    def create_bbWeldSideWeb_21(self):
        weldSideWebOrigin_21 = numpy.array([-self.beamLeft.t / 2, self.beamLeft.D/2 +  self.plateRight.T, self.beamLeft.length / 2 - self.bbWeldSideWeb_21.L/2])
        uDirWeb_21 = numpy.array([0, 1.0, 0])
        wDirWeb_21 = numpy.array([0, 0, 1.0])
        self.bbWeldSideWeb_21.place(weldSideWebOrigin_21, uDirWeb_21, wDirWeb_21)

    def create_bbWeldSideWeb_22(self):
        weldSideWebOrigin_22 = numpy.array([self.beamLeft.t / 2, self.beamLeft.D/2 +  self.plateRight.T, self.beamLeft.length / 2 + self.bbWeldSideWeb_21.L/2])
        uDirWeb_22 = numpy.array([0, 1.0, 0])
        wDirWeb_22 = numpy.array([0, 0, -1.0])
        self.bbWeldSideWeb_22.place(weldSideWebOrigin_22, uDirWeb_22, wDirWeb_22)


#############################################################################################################
#   Following functions returns the CAD model to the function display_3DModel of main file                  #
#############################################################################################################
    def get_beamLModel(self):
        return self.beamLModel

    def get_beamRModel(self):
        return self.beamRModel

    def get_plateRModel(self):
        return self.plateRModel

    def get_nutboltmodels(self):
        return self.nut_bolt_array.get_models()

    def get_bbWeldAbvFlang_21Model(self):
        return self.bbWeldAbvFlang_21Model

    def get_bbWeldAbvFlang_22Model(self):
        return self.bbWeldAbvFlang_22Model

    def get_bbWeldBelwFlang_21Model(self):
        return self.bbWeldBelwFlang_21Model

    def get_bbWeldBelwFlang_22Model(self):
        return self.bbWeldBelwFlang_22Model

    def get_bbWeldBelwFlang_23Model(self):
        return self.bbWeldBelwFlang_23Model

    def get_bbWeldBelwFlang_24Model(self):
        return self.bbWeldBelwFlang_24Model

    def get_bbWeldSideWeb_21Model(self):
        return self.bbWeldSideWeb_21Model

    def get_bbWeldSideWeb_22Model(self):
        return self.bbWeldSideWeb_22Model