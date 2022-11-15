from org.pyengdrom.editor.base import EditorMode
from org.pyengdrom.editor.idle import IdleEditorMode
from org.pyengdrom.engine.files.material import Material
from org.pyengdrom.engine.files.mesh import Mesh

FRAG_TEXT = '''
#version 330 core
out vec4 _fragColor;
in vec2 pTC;
void main()
{
    float opacity = 0;
    
    int ux = int( pTC.x * 1000 );
    int uy = int( pTC.y * 1000 );
    int rx = ux % 50;
    int ry = uy % 50;

    if (rx == 0 || ry == 0) {
        opacity = 1;
    }

    _fragColor = vec4(0, 0, 0, opacity);
}
'''
VERT_TEXT = '''
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 tC;

uniform mat4 mView;

out vec2 pTC;
void main()
{
    pTC = tC;
    gl_Position = vec4(aPos, 1.0);
}
'''

class EditorGridMode(IdleEditorMode):
    def __init__(self, grid):
        super().__init__()

        self.grid = grid

        self.mesh = Mesh("!")
        self.mesh.vao = [ 3, 2 ]
        self.mesh.vbos = [
            [
                -1, -1, 0,
                -1,  1, 0,
                 1, -1, 0,
                 1,  1, 0
            ],
            [
                -1, -1,
                -1, 1,
                1, -1,
                1, 1,
            ]
        ]

        self.mesh.indices = [ 0, 1, 2, 1, 2, 3 ]

        self.material = Material("!")

        self.material.frag = FRAG_TEXT
        self.material.vert = VERT_TEXT
    
    ##################
    # OpenGL related #
    ##################

    def restartGL(self, engine):
        self.mesh.initGL(None, None)
        self.material.initGL()
        super().restartGL(engine)
    def endPaintGL(self, engine):
        self.material.useGL()
        #self.mesh.widget = engine
        self.mesh.paintGL(self.material, None, use_proj=False)