

import enum

from OpenGL.GL import shaders
from OpenGL    import GL

BACKBUFFER_VERTEX = '''
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 tCoord;

uniform mat4 mProj;
uniform mat4 mView;
uniform mat4 mModel;

uniform vec3 mColor;

out vec3 _mColor;
void main()
{
    gl_Position = mProj * mView * mModel * vec4(aPos, 1.0);
    _mColor = mColor;
}
'''
BACKBUFFER_FRAGMENT = '''
#version 330 core
out vec4 _fragColor;
in vec3 _mColor;
void main()
{
    _fragColor = vec4(_mColor, 1);
}
'''


class Material:
    BACKBUFFER_MATERIAL = None
    @staticmethod
    def get_backbuffer_material() -> "Material":
        if Material.BACKBUFFER_MATERIAL is not None: return Material.BACKBUFFER_MATERIAL

        Material.BACKBUFFER_MATERIAL = Material("")
        Material.BACKBUFFER_MATERIAL.vert = BACKBUFFER_VERTEX
        Material.BACKBUFFER_MATERIAL.frag = BACKBUFFER_FRAGMENT
        Material.BACKBUFFER_MATERIAL.initGL()

        return Material.BACKBUFFER_MATERIAL
    
    LAST_VERSION = 0

    def __init__(self, path):
        self.path = path
        self.frag = []
        self.vert = []
        self.args = []
    def initGL(self):
        self.vert_shader = shaders.compileShader(self.vert, GL.GL_VERTEX_SHADER)
        self.frag_shader = shaders.compileShader(self.frag, GL.GL_FRAGMENT_SHADER)

        self.main_shader = shaders.compileProgram(self.vert_shader, self.frag_shader)
    def cleanGL(self):
        shaders.glDetachShader(self.main_shader, self.vert_shader)
        shaders.glDetachShader(self.main_shader, self.frag_shader)
        shaders.glDeleteShader(self.vert_shader)
        shaders.glDeleteShader(self.frag_shader)

        GL.glDeleteProgram(self.main_shader)
    def reloadGL(self):
        self.cleanGL()
        self.initGL()
    def useGL(self):
        GL.glUseProgram(self.main_shader)
    def unUseGL(self):
        GL.glUseProgram(0)

    @staticmethod
    def from_args(path, project, *args):
        mat = Material.read(path, project)
        mat.args = args

        return mat
    @staticmethod
    def read(path, project) -> "Material":
        text = ""
        with open(path, "r") as file: text = file.read()

        version, file = text.split("\n", 1)
        version_code = version[9:] if "version: " in version else Material.LAST_VERSION

        return getattr(Material, f"read_version_{version_code}")(file, path, project)
    @staticmethod
    def read_version_0(string, path, project):
        frag, vert = [], []
        material   = Material(path)

        class ReadMode(enum.Enum): FRAG = 0; VERT = 1; UNKW = 2
        mode = ReadMode.UNKW

        lines = string.split("\n")
        for line in lines:
            l0 = line.strip()
            
            if l0 == "fragment:" or l0 == "vertex:":
                mode = ReadMode.FRAG if l0[0] == "f" else ReadMode.VERT
            elif mode == ReadMode.FRAG:
                frag.append(line)
            elif mode == ReadMode.VERT:
                vert.append(line)
        
        material.frag = "\n".join(frag)
        material.vert = "\n".join(vert)

        return material
