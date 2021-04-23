from opencmiss.zinc.context import Context
from opencmiss.zinc.element import Element
from opencmiss.zinc.field import Field
from opencmiss.zinc.fieldmodule import Fieldmodule
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.graphics import Graphics
from opencmiss.zinc.material import Material
import json

class PyZinc2ZincJS:
    '''
    This example demonstrates how to read and export a simple mesh
    '''
    
    def __init__(self):
        '''Initialise PyZinc Objects'''
        self._context = Context('animation_deforming_heart')
        self._context.getGlyphmodule().defineStandardGlyphs()
        self._default_region = self._context.getDefaultRegion()
        self._logger = self._context.getLogger()
        '''This set the prefix for the files to be exported'''
        self._prefix = 'MyExport'
        '''Read the file with the following function'''
        self.readMesh()
        '''Create surface graphics which will be viewed and exported'''
        self.createSurfaceGraphics()
        '''Create glyph graphics which will be viewed and exported'''
        self.createGlyphGraphics()
        '''Export To ZincJS format'''
        self.exportWebGLJson()
        '''Export graphics into JSON format'''
        numOfMessages = self._logger.getNumberOfMessages()
        for i in range(1, numOfMessages+1):
            print(self._logger.getMessageTextAtIndex(i))
                
    def readMesh(self):
        '''
        Create a stream information then call createStreamresourceFile 
        with the files you want to read into PyZinc
        '''
        prefix = "models/"
        sir = self._default_region.createStreaminformationRegion()
        nodeFilename = prefix + 'cube.exnode'
        fr = sir.createStreamresourceFile(nodeFilename)
        elemFileName = prefix + 'cube.exelem'
        fr2 = sir.createStreamresourceFile(elemFileName)
        self._default_region.read(sir)
        
    def exportWebGLJson(self):
        '''
        Export graphics into JSON format, one json export represents one
        surface graphics.
        '''
        scene = self._default_region.getScene()
        sceneSR = scene.createStreaminformationScene()
        sceneSR.setIOFormat(sceneSR.IO_FORMAT_THREEJS)
        number = sceneSR.getNumberOfResourcesRequired()
        resources = []
        '''Write out each graphics into a json file which can be rendered with ZincJS'''
        for i in range(number):
            resources.append(sceneSR.createStreamresourceMemory())
        scene.write(sceneSR)
        '''Write out each resource into their own file'''
        for i in range(number):
            f = None
            if i == 0:
                f = open(self._prefix + '_' + 'metadata.json', 'w+')
            else:
                f = open(self._prefix + '_' + str(i) + '.json', 'w+')
            buffer = resources[i].getBuffer()[1]
            print(buffer)
            if i == 0:
                for j in range(number-1):
                    '''
                    IMPORTANT: the replace name here is relative to your html page, so adjust it
                    accordingly.
                    '''		
                    replaceName = '' + self._prefix + '_' + str(j+1) + '.json'
                    old_name = 'memory_resource'+ '_' + str(j+2)
                    buffer = buffer.replace(old_name, replaceName)
            f.write(buffer)
            f.close()    
        
    def createSurfaceGraphics(self):
        '''
        Create the surface graphics using the finite element field 'coordinates'.
        The tessellations of the surface can be changed to increase/decrease details
        of the mesh.
        '''
        material_module = self._context.getMaterialmodule()
        scene = self._default_region.getScene()
        fieldmodule = self._default_region.getFieldmodule()
        tm = self._context.getTessellationmodule()
        tessellation = tm.createTessellation()
        tessellation.setMinimumDivisions([4,4,1])
        scene.beginChange()
        surface = scene.createGraphicsSurfaces()
        finite_element_field = fieldmodule.findFieldByName('coordinates')
        surface.setCoordinateField(finite_element_field)
        surface.setTessellation(tessellation)
        ''' Setting exterior only should reduce export size without compromising quality '''
        surface.setExterior(True)
        # Let the scene render the scene.
        scene.endChange()
        # createSurfaceGraphics end

    def createGlyphGraphics(self):
        '''
        Create the glyph graphics using the finite element field 'coordinates'.
        '''
        material_module = self._context.getMaterialmodule()
        scene = self._default_region.getScene()
        fieldmodule = self._default_region.getFieldmodule()
        scene.beginChange()
        glyph = scene.createGraphicsPoints()
        glyph.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
        finite_element_field = fieldmodule.findFieldByName('coordinates')
        glyph.setCoordinateField(finite_element_field)
        pointAttr = glyph.getGraphicspointattributes()
        label_field = fieldmodule.findFieldByName('cmiss_number')
        pointAttr.setLabelField(label_field)
        sphere = self._context.getGlyphmodule().findGlyphByGlyphShapeType(Glyph.SHAPE_TYPE_SPHERE)
        pointAttr.setGlyph(sphere)
        # Let the scene render the scene.
        scene.endChange()
        # createSurfaceGraphics end

PyZinc2ZincJS()

