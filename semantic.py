from antlr4 import ParseTreeWalker
from antlr4 import TerminalNode

from antlr_out.MiniPythonParser import MiniPythonParser
from antlr_out.MiniPythonListener import MiniPythonListener


class SemanticParser(MiniPythonListener):
    current_node = None

    class Global:
        def __init__(self, scope):
            self.scope = scope
            self.body = []

        def __str__(self):
            return '<global>'

        def get_children(self):
            return self.body

    def __init__(self):
        self.root = SemanticParser.Global(None)
        self.current_node = self.root

    class Block(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return '<block>'

    def enterSuite(self, ctx):
        node = SemanticParser.Block(self.current_node)
        self.current_node.body.append(node)
        self.current_node = node

    def exitSuite(self, ctx):
        self.current_node = self.current_node.scope

    class Function(Global):
        def __init__(self, name, scope):
            super().__init__(scope)
            self.name = name
            self.input = []

        def __str__(self):
            return "<function: '{}'>".format(self.name)

        def get_children(self):
            return self.input + super().get_children()

    def enterFunc_def(self, ctx):
        func_name = ctx.children[1].symbol.text
        node = SemanticParser.Function(func_name, self.current_node)
        self.current_node.body.append(node)
        self.current_node = node

    class FunctionInput(Global):
        def __init__(self, name, scope):
            super().__init__(scope)
            self.name = name

        def __str__(self):
            return "<input: '{}'>".format(self.name)

    def enterVfpdef(self, ctx):
        param_name = ctx.children[0].symbol.text
        func = self.current_node
        if isinstance(func, SemanticParser.Function):
            node = SemanticParser.FunctionInput(param_name, self.current_node)
            func.input.append(node)

    def exitFunc_def(self, ctx):
        self.current_node = self.current_node.scope

    class Condition(Global):
        def __init__(self, scope):
            super().__init__(scope)
            self.predicate = []

        def get_children(self):
            return self.predicate + super().get_children()

        def __str__(self):
            return '<if>'

    def enterIf_stmt(self, ctx):
        node = SemanticParser.Condition(self.current_node)
        self.current_node.body.append(node)
        self.current_node = node

    def exitIf_stmt(self, ctx):
        self.current_node = self.current_node.scope

    class CycleByCond(Global):
        def __init__(self, scope):
            super().__init__(scope)
            self.predicate = []

        def get_children(self):
            return self.predicate + super().get_children()

        def __str__(self):
            return '<while>'

    def enterWhile_stmt(self, ctx):
        node = SemanticParser.CycleByCond(self.current_node)
        self.current_node.body.append(node)
        self.current_node = node

    def exitWhile_stmt(self, ctx):
        self.current_node = self.current_node.scope

    class CycleByCollection(Global):
        def __init__(self, scope):
            super().__init__(scope)
            self.cursor = []
            self.collection = []

        def get_children(self):
            return self.cursor + self.collection + super().get_children()

        def __str__(self):
            return '<for>'

    def enterFor_stmt(self, ctx):
        node = SemanticParser.CycleByCollection(self.current_node)
        self.current_node.body.append(node)
        self.current_node = node

    def exitFor_stmt(self, ctx):
        self.current_node = self.current_node.scope

    class ControlFlow(Global):
        def __init__(self, action, scope):
            super().__init__(scope)
            self.action = action

        def __str__(self):
            return "<flow: '{}'>".format(self.action)

    def enterFlow_stmt(self, ctx):
        action = ctx.children[0].symbol.text
        node = SemanticParser.ControlFlow(action, self.current_node)
        self.current_node.body.append(node)
        self.current_node = node

    def exitFlow_stmt(self, ctx):
        self.current_node = self.current_node.scope

    class Abstraction(Global):
        def __init__(self, name, scope):
            super().__init__(scope)
            self.name = name

        def __str__(self):
            return "<class: '{}'>".format(self.name)

    def enterClass_def(self, ctx):
        name = ctx.children[1].symbol.text
        node = SemanticParser.Abstraction(name, self.current_node)
        self.current_node.body.append(node)
        self.current_node = node

    def exitClass_def(self, ctx):
        self.current_node = self.current_node.scope

    def enterTest(self, ctx):
        if len(ctx.children) == 1:
            pass

    def enterOr_test(self, ctx):
        if len(ctx.children) == 1:
            pass

    def enterAnd_test(self, ctx):
        if len(ctx.children) == 1:
            pass

    def enterNot_test(self, ctx):
        if len(ctx.children) == 1:
            pass

    class Comparison(Global):
        def __init__(self, operator, scope):
            super().__init__(scope)
            self.operator = operator

        def __str__(self):
            return "<comp: '{}'>".format(self.operator)

    def enterComparison(self, ctx):
        if len(ctx.children) > 1:
            #TODO: make loop for many comp_ops
            child = ctx.children[1]
            if isinstance(child, MiniPythonParser.Comp_opContext):
                operator = child.children[0].symbol.text

                if isinstance(self.current_node, (SemanticParser.Condition, SemanticParser.CycleByCond)):
                    node = SemanticParser.Comparison(operator, self.current_node)
                    self.current_node.predicate.append(node)
                    self.current_node = node

    def exitComparison(self, ctx):
        if isinstance(self.current_node, SemanticParser.Comparison):
            self.current_node = self.current_node.scope

    class Assign(Global):
        def __init__(self, operator, scope):
            super().__init__(scope)
            self.operator = operator

        def __str__(self):
            return "<assign: '{}'>".format(self.operator)

    class AugAssign(Global):
        def __init__(self, operator, scope):
            super().__init__(scope)
            self.operator = operator

        def __str__(self):
            return "<aug assign: '{}'>".format(self.operator)

    def enterExpr_stmt(self, ctx):
        if len(ctx.children) > 1:
            node = None
            if isinstance(ctx.children[1], TerminalNode):
                operator = ctx.children[1].symbol.text
                node = SemanticParser.Assign(operator, self.current_node)

            elif isinstance(ctx.children[1], MiniPythonParser.Aug_assignContext):
                operator = ctx.children[1].children[0].symbol.text
                node = SemanticParser.AugAssign(operator, self.current_node)

            if node:
                self.current_node.body.append(node)
                self.current_node = node

    def exitExpr_stmt(self, ctx):
        if isinstance(self.current_node, (SemanticParser.Assign, SemanticParser.AugAssign)):
            self.current_node = self.current_node.scope

    def enterStar_expr(self, ctx):
        if len(ctx.children) == 1:
            pass

    class Addity(Global):
        def __init__(self, operator, scope):
            super().__init__(scope)
            self.operator = operator

        def __str__(self):
            return "<additive: '{}'>".format(self.operator)

    def enterExpr(self, ctx):
        if len(ctx.children) > 1:
            if isinstance(ctx.children[1], TerminalNode):
                operator = ctx.children[1].symbol.text
                node = SemanticParser.Addity(operator, self.current_node)
                self.current_node.body.append(node)
                self.current_node = node

    def exitExpr(self, ctx):
        if isinstance(self.current_node, SemanticParser.Addity):
            self.current_node = self.current_node.scope

    class Multiply(Global):
        def __init__(self, operator, scope):
            super().__init__(scope)
            self.operator = operator

        def __str__(self):
            return "<multiply: '{}'>".format(self.operator)

    def enterTerm(self, ctx):
        if len(ctx.children) > 1:
            if isinstance(ctx.children[1], TerminalNode):
                operator = ctx.children[1].symbol.text
                node = SemanticParser.Multiply(operator, self.current_node)
                self.current_node.body.append(node)
                self.current_node = node
        if len(ctx.children) == 1:
            pass

    def exitTerm(self, ctx):
        if isinstance(self.current_node, SemanticParser.Multiply):
            self.current_node = self.current_node.scope

    def enterFactor(self, ctx):
        if len(ctx.children) == 1:
            pass

    class Variable(Global):
        def __init__(self, name, scope):
            super().__init__(scope)
            self.name = name

        def __str__(self):
            return "<var: '{}'>".format(self.name)

    class Constant(Global):
        def __init__(self, value, scope):
            super().__init__(scope)
            self.value = value

        def __str__(self):
            return "<const: '{}'>".format(self.value)

    class Call(Global):
        def __init__(self, callable, scope):
            super().__init__(scope)
            self.callable = callable

        def __str__(self):
            return "<call: '{}'>".format(self.callable)

    def enterAtom(self, ctx):
        if len(ctx.children) == 1:
            child = ctx.children[0]

            if isinstance(child, TerminalNode):
                name = child.symbol.text
                if len(ctx.parentCtx.children) == 1:
                    node = SemanticParser.Variable(name, self.current_node)
                    self.current_node.body.append(node)

                elif ctx.parentCtx.children[1].children[0].symbol.text == '(':
                    node = SemanticParser.Call(name, self.current_node)
                    self.current_node.body.append(node)
                    self.current_node = node

            elif isinstance(child, (MiniPythonParser.NumberContext, MiniPythonParser.StringContext)):
                value = child.children[0].symbol.text
                node = SemanticParser.Constant(value, self.current_node)
                self.current_node.body.append(node)

    def exitTrailer(self, ctx):
        if isinstance(self.current_node, SemanticParser.Call):
            self.current_node = self.current_node.scope

    def to_file(self, dest_file):
        def write_rec(node, depth):
            dest_file.write(' ' * 2 * depth + str(node) + '\n')
            for child in node.get_children():
                write_rec(child, depth + 1)
        write_rec(self.root, 0)


def get_semantic(tree, file_name):
    walker = ParseTreeWalker()
    parser = SemanticParser()
    walker.walk(parser, tree)

    with open(file_name + '.sem', 'w') as dest_file:
        parser.to_file(dest_file)
    return parser
