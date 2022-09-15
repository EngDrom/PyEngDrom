
from org.pyengdrom.config.config import EngDromConfig

class ProjectConfig:
    engine_config = EngDromConfig()

    to_save_data = {}

    def __setattr__(self, __name: str, __value) -> None:
        if "__" in __name:
            ctx, name = __name.split("__", 1)
            if not ctx in self.to_save_data: self.to_save_data[ctx] = set()

            self.to_save_data[ctx].add(name)
            
        super().__setattr__(__name, __value)

    def to_string(self):
        contexts = set()
        lines = []

        for ctx in self.to_save_data.keys():
            lines.append(f"[{ctx}]")
            for name in self.to_save_data[ctx]:
                lines.append(f"{name}={getattr(self, ctx + '__' + name)}")
            lines.append("")
        
        return "\n".join(lines)
    @staticmethod
    def from_string(string : str):
        lines   = string.split("\n")
        context = None
        elem    = ProjectConfig()

        for line in lines:
            line = line.strip()

            if line.startswith("[") and line.endswith("]"):
                context = line[1:-1]
            else:
                if context == None:
                    raise Exception("Improperly configured project config, expected context before first line")

                name, *value = line.split("=")
                setattr(elem, context + "__" + name.strip(), "=".join(value))
        
        return elem
    @staticmethod
    def read(path : str):
        with open(path, 'r') as file:
            return ProjectConfig.from_string(file.read())
