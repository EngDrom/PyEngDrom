

from org.pyengdrom.engine.utils.template import ProjectTemplate
import os

def create_project(template: ProjectTemplate, name: str, path: str):
    assert os.path.exists(path)

    with open(os.path.join(path, ".project"), 'w') as file:
        file.write(f"[project]\nname={name}\n")
