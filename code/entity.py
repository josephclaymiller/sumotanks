#entity - an ode physics controlled object in the game world

import sys

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

Infinity = 1e10000
NaN = Infinity/Infinity

class entity( NodePath):
    def __init__( self ):
        NodePath.__init__( self, 'entity' )
        self.setAntialias(AntialiasAttrib.MMultisample)

    def step( self ):
        pos = self.odeBody.getPosition()
        quat = Quat(self.odeBody.getQuaternion())
        if pos.length() == Infinity or pos.length() == NaN:
            #Object got out of control; problem with collision or bug
            self.stop()
            pos = Vec3(0,0,0)
            quat = Quat(0,0,0,0)
        self.setPos( render, pos )
        self.setQuat( render, quat )

    def stop ( self ):
        #Stop an entity's motion and rotation
        self.odeBody.setLinearVel( Vec3(0,0,0) )
        self.odeBody.setForce( Vec3(0,0,0) )
        self.odeBody.setAngularVel( Vec3(0,0,0) )
        self.odeBody.setTorque( Vec3(0,0,0) )

    def setPos( self, *args):
        NodePath.setPos( self, *args )
        self.updateOde()

    def setHpr( self, *args ):
        NodePath.setHpr( self, *args )
        self.updateOde()

    def updateOde( self ):
        self.odeBody.setPosition( self.getPos( render ) )
        self.odeBody.setQuaternion( self.getQuat( render ) )

class testSmiley( entity ):
    #a simple ode sphere smiley; for testing purposes
    def __init__( self, _odeSpace, _odeWorld ):
        entity.__init__( self )
        self.model = loader.loadModel( '../art/tank/newtank.egg' )

        self.odeMass = OdeMass()
        self.odeMass.setBox(1, Vec3(1,1,1))

        self.odeBody = OdeBody( _odeWorld )
        self.odeBody.setMass (self.odeMass )

        self.odeGeom = OdeBoxGeom( _odeSpace, Vec3(1,1,1))
        self.odeGeom.setBody( self.odeBody )

        self.model.reparentTo(self)

class testTerrain( entity ):
    #an ode object that does not move (like a terrain)
    def __init__( self, _odeSpace, _odeWorld ):
        entity.__init__( self )
        self.model = loader.loadModel( 'models/environment')
        self.model.setScale(0.25)
        self.model.setPos(-8,42,0)

        self.model.flattenStrong()

        trimeshData = OdeTriMeshData( self.model, True )
        self.odeGeom = OdeTriMeshGeom( _odeSpace, trimeshData )

        self.model.reparentTo( self )
   
    def updateOde( self ):
        self.odeGeom.setPosition( self.getPos( render ) )
        self.odeGeom.setQuaternion( self.getQuat( render ) )

class testTank( entity ):
    def __init__( self, _odeSpace, _odeWorld ):
        entity.__init__( self )
        self.model = loader.loadModel( '../art/tank/newtank.egg' )
        self.model.setScale( 0.01 )
   
        self.odeMass = OdeMass()
        self.odeMass.setBox( 1, Vec3(1,1,1) )
   
        self.odeBody = OdeBody( _odeWorld )
        self.odeBody.setMass( self.odeMass )
   
        self.model.flattenStrong()
        trimeshData = OdeTriMeshData( self.model, True )
        self.odeGeom = OdeTriMeshGeom( _odeSpace, trimeshData )
   
        if False: # checking the data
            print "self.odeGeom.getNumTriangles()", self.odeGeom.getNumTriangles()
            for i in xrange(self.odeGeom.getNumTriangles()):
                x = Point3(0)
                y = Point3(0)
                z = Point3(0)
                self.odeGeom.getTriangle( i, x, y, z )
                print x,y,z
        self.odeGeom.setBody( self.odeBody )
