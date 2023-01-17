
from PIL import Image

import numpy as np

from OpenGL.GL import *

import matplotlib.pyplot as plt

class TextureManager:
    built_arrays = {}

    @staticmethod
    def needs_build (path):
        return not (path in TextureManager.built_arrays)
    @staticmethod
    def get_build(path):
        return TextureManager.built_arrays[path]
    @staticmethod
    def store_build(path, _gl_text):
        TextureManager.built_arrays[path] = _gl_text

class Texture:
    def __init__(self, path=""):
        self.path = path
    def get_image(self):
        return Image.open(self.path).convert('RGBA')
    def createImage(self):
        if hasattr(self, "_Texture__img"): return self.__img
        self.__img = self.get_image()
        return self.__img
    def initGL(self):
        if not TextureManager.needs_build(self.path):
            self._gl_text = TextureManager.get_build(self.path)
            return

        img = self.createImage()

        img_data = np.array(list(img.getdata()), np.int8)
        self._gl_text = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._gl_text)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        TextureManager.store_build(self.path, self._gl_text)
    def size(self):
        return self.get_image().size

class AtlasTexture(Texture):
    def __init__(self, project, atlas):
        super().__init__("")
        self.atlas = []
        self.make_atlas(project, atlas)
    
    def make_atlas(self, project, path):
        with open(path, 'r') as file:
            lines = file.read().split("\n")
            self.path = project.build_path( lines[0] )

            for line in lines[1:]:
                self.make_atlas_line(line)
    def make_atlas_line(self, line):
        if line.strip() == "": return
        w, h, x, y, cx, cy = tuple(map(int, line.split(" ")))
        for dx in range(cx):
            for dy in range(cy):
                self.atlas.append( [ x + dx * w, y + dy * h, w, h ] )
    def coordinates(self, index):
        img = self.createImage()

        x, y, w, h = self.atlas[index]
        # Prevent strange effects on pixel border
        x += 0.01
        y += 0.01
        w -= 0.02
        h -= 0.02

        x0, y0 = x, y
        x1, y1 = x + w, y + h

        return [
            [x0 / img.size[0], y1 / img.size[1]],
            [x1 / img.size[0], y1 / img.size[1]],
            [x1 / img.size[0], y0 / img.size[1]],
            [x0 / img.size[0], y0 / img.size[1]],
        ]
