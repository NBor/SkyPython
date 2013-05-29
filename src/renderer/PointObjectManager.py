'''
Created on 2013-05-25

@author: Neil
'''

from RendererObjectManager import RendererObjectManager
from rendererUtil.SkyRegionMap import SkyRegionMap

class PointObjectManager(RendererObjectManager):
    '''
    classdocs
    '''

    class RegionData(object):
        '''
        classdocs
        '''
    
        def __init__(self):
            '''
            constructor
            '''
            self.sources = []
            self.vertex_buffer = []
            self.color_buffer = []
            self.text_coord_buffer = []
            self.index_buffer = []
       
    class RegionDataFactory(object):
        '''
        classdocs
        '''
        def construct(self):
            return PointObjectManager.RegionData()
        
        def __init__(self):
            '''
            constructor
            '''
            
    NUM_STARS_IN_TEXTURE = 2
    MINIMUM_NUM_POINTS_FOR_REGIONS = 200
    COMPUTE_REGIONS = True
    sky_regions = SkyRegionMap()
    texture_ref = None
    
    def update_objects(self, points, update_type):
        only_update_points = True
        # We only care about updates to positions, ignore any other updates.
#     if (updateType.contains(UpdateType.Reset)) {
#       only_update_points = false;
#     } else if (updateType.contains(UpdateType.UpdatePositions)) {
#       // Sanity check: make sure the number of points is unchanged.
#       if (points.size() != num_points) {
#         Log.e("PointObjectManager",
#               "Updating PointObjectManager a different number of points: update had " +
#               points.size() + " vs " + num_points + " before");
#         return;
#       }
#     } else {
#       return;
#     }
# 
        num_points = len(points)
        
        self.sky_regions.clear()
        
        region = SkyRegionMap.CATCHALL_REGION_ID
        if self.COMPUTE_REGIONS: 
            # Find the region for each point, and put it in a separate list
            # for that region.
            for point in points:
                if len(points) < self.MINIMUM_NUM_POINTS_FOR_REGIONS:
                    region = SkyRegionMap.CATCHALL_REGION_ID
                else:
                    region = self.sky_regions.get_object_region(point.geocentric_coords)
                # self.sky_regions.get_region_data(region) is a RegionData instance
                data_for_region = self.sky_regions.get_region_data(region)
                data_for_region.sources.append(point)
            
            for region_key in self.sky_regions.region_data.keys():
                print region_key, len(self.sky_regions.get_region_data(region_key).sources)
            exit(0)
        else:
            self.sky_regions.get_region_data(region).sources = points
# 
#     // Generate the resources for all of the regions.
#     for (RegionData data : mSkyRegions.getDataForAllRegions()) {
#       int numVertices = 4 * data.sources.size();
#       int numIndices = 6 * data.sources.size();
# 
#       data.mVertexBuffer.reset(numVertices);
#       data.mColorBuffer.reset(numVertices);
#       data.mTexCoordBuffer.reset(numVertices);
#       data.mIndexBuffer.reset(numIndices);
# 
#       Vector3 up = new Vector3(0, 1, 0);
# 
#       // By inspecting the perspective projection matrix, you can show that,
#       // to have a quad at the center of the screen to be of size k by k
#       // pixels, the width and height are both:
#       // k * tan(fovy / 2) / screenHeight
#       // This is not difficult to derive.  Look at the transformation matrix
#       // in SkyRenderer if you're interested in seeing why this is true.
#       // I'm arbitrarily deciding that at a 60 degree field of view, and 480
#       // pixels high, a size of 1 means "1 pixel," so calculate sizeFactor
#       // based on this.  These numbers mostly come from the fact that that's
#       // what I think looks reasonable.
#       float fovyInRadians = 60 * MathUtil.PI / 180.0f;
#       float sizeFactor = MathUtil.tan(fovyInRadians * 0.5f) / 480;
# 
#       Vector3 bottomLeftPos = new Vector3(0, 0, 0);
#       Vector3 topLeftPos = new Vector3(0, 0, 0);
#       Vector3 bottomRightPos = new Vector3(0, 0, 0);
#       Vector3 topRightPos = new Vector3(0, 0, 0);
# 
#       Vector3 su = new Vector3(0, 0, 0);
#       Vector3 sv = new Vector3(0, 0, 0);
# 
#       short index = 0;
# 
#       float starWidthInTexels = 1.0f / NUM_STARS_IN_TEXTURE;
# 
#       for (PointSource p : data.sources) {
#         int color = 0xff000000 | p.getColor();  // Force alpha to 0xff
#         short bottomLeft = index++;
#         short topLeft = index++;
#         short bottomRight = index++;
#         short topRight = index++;
# 
#         // First triangle
#         data.mIndexBuffer.addIndex(bottomLeft);
#         data.mIndexBuffer.addIndex(topLeft);
#         data.mIndexBuffer.addIndex(bottomRight);
# 
#         // Second triangle
#         data.mIndexBuffer.addIndex(topRight);
#         data.mIndexBuffer.addIndex(bottomRight);
#         data.mIndexBuffer.addIndex(topLeft);
# 
#         int starIndex = p.getPointShape().getImageIndex();
# 
#         float texOffsetU = starWidthInTexels * starIndex;
# 
#         data.mTexCoordBuffer.addTexCoords(texOffsetU, 1);
#         data.mTexCoordBuffer.addTexCoords(texOffsetU, 0);
#         data.mTexCoordBuffer.addTexCoords(texOffsetU + starWidthInTexels, 1);
#         data.mTexCoordBuffer.addTexCoords(texOffsetU + starWidthInTexels, 0);
# 
#         Vector3 pos = p.getLocation();
#         Vector3 u = VectorUtil.normalized(VectorUtil.crossProduct(pos, up));
#         Vector3 v = VectorUtil.crossProduct(u, pos);
# 
#         float s = p.getSize() * sizeFactor;
# 
#         su.assign(s*u.x, s*u.y, s*u.z);
#         sv.assign(s*v.x, s*v.y, s*v.z);
# 
#         bottomLeftPos.assign(pos.x - su.x - sv.x, pos.y - su.y - sv.y, pos.z - su.z - sv.z);
#         topLeftPos.assign(pos.x - su.x + sv.x, pos.y - su.y + sv.y, pos.z - su.z + sv.z);
#         bottomRightPos.assign(pos.x + su.x - sv.x, pos.y + su.y - sv.y, pos.z + su.z - sv.z);
#         topRightPos.assign(pos.x + su.x + sv.x, pos.y + su.y + sv.y, pos.z + su.z + sv.z);
# 
#         // Add the vertices
#         data.mVertexBuffer.addPoint(bottomLeftPos);
#         data.mColorBuffer.addColor(color);
# 
#         data.mVertexBuffer.addPoint(topLeftPos);
#         data.mColorBuffer.addColor(color);
# 
#         data.mVertexBuffer.addPoint(bottomRightPos);
#         data.mColorBuffer.addColor(color);
# 
#         data.mVertexBuffer.addPoint(topRightPos);
#         data.mColorBuffer.addColor(color);
#       }
#       Log.i("PointObjectManager",
#             "Vertices: " + data.mVertexBuffer.size() + ", Indices: " + data.mIndexBuffer.size());
#       data.sources = null;
#     }
    
    def reload(self, gl, bool_full_reload):
        print "Not implemented"
        #raise NotImplementedError("need OpenGL support")
    
    def draw_internal(self, gl):
#     gl.glEnableClientState(GL10.GL_VERTEX_ARRAY);
#     gl.glEnableClientState(GL10.GL_COLOR_ARRAY);
#     gl.glEnableClientState(GL10.GL_TEXTURE_COORD_ARRAY);
# 
#     gl.glEnable(GL10.GL_CULL_FACE);
#     gl.glFrontFace(GL10.GL_CW);
#     gl.glCullFace(GL10.GL_BACK);
# 
#     gl.glEnable(GL10.GL_ALPHA_TEST);
#     gl.glAlphaFunc(GL10.GL_GREATER, 0.5f);
# 
#     gl.glEnable(GL10.GL_TEXTURE_2D);
# 
#     mTextureRef.bind(gl);
# 
#     gl.glTexEnvf(GL10.GL_TEXTURE_ENV, GL10.GL_TEXTURE_ENV_MODE, GL10.GL_MODULATE);
# 
        # Render all of the active sky regions.
        active_regions = self.render_state.active_sky_region_set
        active_region_data = self.sky_regions.get_data_for_active_regions(active_regions)
        print active_regions.active_standard_regions
        print active_region_data
        for data in active_region_data:
            print len(data.sources)
#       if (data.mVertexBuffer.size() == 0) {
#         continue;
#       }
# 
#       data.mVertexBuffer.set(gl);
#       data.mColorBuffer.set(gl, getRenderState().getNightVisionMode());
#       data.mTexCoordBuffer.set(gl);
#       data.mIndexBuffer.draw(gl, GL10.GL_TRIANGLES);
#     }
# 
#     gl.glDisableClientState(GL10.GL_TEXTURE_COORD_ARRAY);
#     gl.glDisable(GL10.GL_TEXTURE_2D);
#     gl.glDisable(GL10.GL_ALPHA_TEST);
#   }
        
        #raise NotImplementedError("need OpenGL support")

    def __init__(self, new_layer, new_texture_manager=None):
        '''
        change inputs to not be default
        '''
        RendererObjectManager.__init__(self, new_layer, new_texture_manager)
        self.sky_regions.region_data_factory = self.RegionDataFactory()
        