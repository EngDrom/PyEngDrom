

from org.pyengdrom.pydromadaire.evaluate.nodes.grammar.function_node import StackBasedFunction, use_stack


AWAIT_LEVEL_LOADED = '$engdrom.await.level_load'

class EngDromAPI:
    CONTROLLERS = set()
    @staticmethod
    @use_stack
    def registerController(stack, controller):
        EngDromAPI.CONTROLLERS.add(controller)
    @staticmethod
    @use_stack
    def getControllers(stack):
        return list(EngDromAPI.CONTROLLERS)
    @staticmethod
    @use_stack
    def awaitLevelLoaded(stack, function):
        if not AWAIT_LEVEL_LOADED in stack.__global__.dict:
            stack.__global__.dict[AWAIT_LEVEL_LOADED] = []
        stack.__global__.dict[AWAIT_LEVEL_LOADED].append(
            (stack, function if not isinstance(function, StackBasedFunction) else lambda *args: function(stack, *args))
        )
