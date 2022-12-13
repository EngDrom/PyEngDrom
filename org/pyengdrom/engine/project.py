
import os

from org.pyengdrom.config.reader import ProjectConfig
from org.pyengdrom.engine.files.grid import Grid
from org.pyengdrom.engine.files.level import Level
from org.pyengdrom.engine.files.material import Material
from org.pyengdrom.engine.files.mesh import Mesh
from org.pyengdrom.pydromadaire import PyDromLangage

class EngineProject:
    def __init__(self, folder):
        self.level  = None
        self.folder = folder

        if not os.path.exists(folder): raise Exception("Project folder could not be found")
        self._conf_path = os.path.join(folder, ".project")

        if not os.path.exists(self._conf_path):
            raise Exception("Project config could not be found")
        self._config = ProjectConfig.read(self._conf_path)
        self._config.save(self._conf_path)
        self.load_level(self._config.project__default_level)
    def build_path(self, path):
        return os.path.join(self.folder, path)
    def unbuild_path (self, path):
        dirname = os.path.dirname(path)
        name = os.path.basename(path)
        return os.path.join(os.path.relpath(self.folder, dirname), name)
    def load_level(self, path):
        level_path = os.path.join(self.folder, path)

        self.level = Level.read(level_path, self)
    def load_mesh(self, mesh, *args):
        mesh_path = os.path.join(self.folder, mesh)
        if mesh_path.endswith(".grid"):
            grid = Grid.from_path(mesh_path, self, *args)
            grid._Mesh__path = mesh_path
            return grid

        mesh = Mesh.from_args(mesh_path, self, *args)
        mesh._Mesh__path = mesh_path
        return mesh
    def load_mat(self, mat, *args):
        mat_path = os.path.join(self.folder, mat)

        mat = Material.from_args(mat_path, self, *args)
        return mat
    def load_script (self, path, *args):
        file_path = os.path.join(self.folder, path)

        module = ".".join(".".join(path.split("/")).split("\\"))
        with open(file_path, 'r') as file:
            node = PyDromLangage.compile( file.read(), module )
            stack = PyDromLangage.run_module(node, { '$engdrom.project': self })
            return stack