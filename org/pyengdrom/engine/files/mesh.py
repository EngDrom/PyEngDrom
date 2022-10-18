
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np

import enum


FRAG_TEXT = '''
#version 330 core
out vec4 _fragColor;
void main()
{
    _fragColor = vec4(1);
}
'''
VERT_TEXT = '''
#version 330 core
layout (location = 0) in vec3 aPos;
void main()
{
    gl_Position = vec4(aPos, 1.0);
}
'''

class Mesh:
    LAST_VERSION = 0

    def __init__(self, path, *args):
        self.path = path

        self.vao  = []
        self.vbos = []

        self.indices = []
        self.args    = args

        self._texture = None
    def initGL(self, widget):
        self.widget = widget

        self._gl_vbos = []
        data_arr_size = []
        
        for idx in range(len(self.vbos)):
            # Create data array and generate buffer
            data_arr = np.reshape( np.array(
                self.vbos[idx], dtype=np.float32
            ), (
                len(self.vbos[idx]) // self.vao[idx], # Point count 
                self.vao[idx]                         # Vector size
            ))
            vvbo = glGenBuffers(1)
            self._gl_vbos.append(vvbo)

            # Bind buffer and set data
            glBindBuffer(GL_ARRAY_BUFFER, vvbo)
            glBufferData(
                GL_ARRAY_BUFFER, data_arr.nbytes, data_arr, GL_DYNAMIC_DRAW
            )
            data_arr_size.append(data_arr.dtype.itemsize * self.vao[idx])

        self._gl_vao = mvao = glGenVertexArrays(1)
        glBindVertexArray(mvao)

        for idx, vvbo in enumerate(self._gl_vbos):
            glEnableVertexAttribArray(idx)
            glBindBuffer(GL_ARRAY_BUFFER, self._gl_vbos[idx])
            glVertexAttribPointer(
                idx, self.vao[idx], GL_FLOAT, GL_FALSE, data_arr_size[idx], None
            )
            
            glDisableVertexAttribArray(idx)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        indice_data_array = np.array( self.indices, dtype=np.uint32 )

        self.element_buffer = glGenBuffers(1)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indice_data_array.dtype.itemsize * len(self.indices), indice_data_array, GL_STATIC_DRAW)

    def setMatrix(self, matrix, location):
        location = glGetUniformLocation(self.main_shader, location)

        glUniformMatrix4fv(location, 1, GL_FALSE, matrix)
    def setVec3(self, vec3, location):
        location = glGetUniformLocation(self.main_shader, location)

        glUniform3f(location, vec3[0], vec3[1], vec3[2])
    def paintGL(self, shader, mModel):
        # Init shader and uniform matrices
        self.main_shader = shader.main_shader

        self.setMatrix(glGetDoublev(GL_PROJECTION_MATRIX), "mProj")
        self.setMatrix(self.widget.camera.get_matrix(),    "mView")
        self.setMatrix(mModel,                             "mModel")

        if self._texture is not None:
            glBindTexture(GL_TEXTURE_2D, self._texture._gl_text)

        # Init VAO and VBOs
        glBindVertexArray(self._gl_vao)
        for i in range(len(self._gl_vbos)): glEnableVertexAttribArray(i)
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        glDrawElements(
            GL_TRIANGLES,
            len(self.indices),
            GL_UNSIGNED_INT,
            None
        )

        # Clean up VBOs, VAO, shader
        for i in range(len(self._gl_vbos)): glDisableVertexAttribArray(i)
        glBindVertexArray(0)
        glUseProgram(0)


    def __str__(self):
        return f"<Mesh {self.path} vao={self.vao} {self.args}>"

    @staticmethod
    def from_args(path, project, *args):
        mesh = Mesh.read(path, project)
        mesh.args = args

        return mesh
    @staticmethod
    def read(path, project) -> "Mesh":
        text = ""
        with open(path, "r") as file: text = file.read()

        version, file = text.split("\n", 1)
        version_code = version[9:] if "version: " in version else Mesh.LAST_VERSION

        return getattr(Mesh, f"read_version_{version_code}")(file, path, project)
    @staticmethod
    def read_version_0(string, path, project):
        class ReadMode(enum.Enum):
            VAO  = 0
            VBO  = 1
            INDX = 2
            UNKN = 3
        
        mode = ReadMode.UNKN
        mesh = Mesh(path)

        lines = string.split("\n")
        for line in lines:
            line = line.strip()
            if line[-1] == ":":
                nmode = line[:-1]
                if nmode == "vao"    : mode = ReadMode.VAO
                if nmode == "vbo"    : mode = ReadMode.VBO
                if nmode == "indices": mode = ReadMode.INDX
            else:
                tpe = float if mode == ReadMode.VBO else int
                arr = list(map(tpe, line.split(" ")))
                if mode == ReadMode.INDX:
                    mesh.indices = arr
                elif mode == ReadMode.VAO:
                    mesh.vao = arr
                else:
                    mesh.vbos.append(arr)
        
        return mesh
