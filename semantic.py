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

        def add(self, node):
            self.body.append(node)

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
        self.current_node.add(node)
        self.current_node = node

    def exitSuite(self, ctx):
        self.current_node = self.current_node.scope

    class Function(Global):
        def __init__(self, name, scope):
            super().__init__(scope)
            self.name = name

        def __str__(self):
            return "<function: '{}'>".format(self.name)

    def enterFunc_def(self, ctx):
        func_name = ctx.children[1].getText()
        node = SemanticParser.Function(func_name, self.current_node)
        self.current_node.add(node)
        self.current_node = node

    class FunctionInput(Global):
        def __init__(self, name, scope):
            super().__init__(scope)
            self.name = name
            self.has_default = False
            self.all_positional = False
            self.all_keywords = False

        def __str__(self):
            tag_name = 'input'
            if self.has_default:
                tag_name = 'default'
            elif self.all_positional:
                tag_name = 'array'
            elif self.all_keywords:
                tag_name = 'dict'
            return "<{}: '{}'>".format(tag_name, self.name)

    def enterVfpdef(self, ctx):
        if isinstance(self.current_node, SemanticParser.FunctionInput):
            self.current_node = self.current_node.scope

        param_name = ctx.children[0].getText()
        node = SemanticParser.FunctionInput(param_name, self.current_node)
        self.current_node.add(node)
        self.current_node = node

    def exitVfpdef(self, ctx):
        my_index = 0
        for index, child in enumerate(ctx.parentCtx.children):
            if isinstance(child, MiniPythonParser.VfpdefContext):
                if ctx.invokingState == child.invokingState:
                    my_index = index
                    break

        if my_index > 0:
            before = ctx.parentCtx.children[my_index - 1]
            if isinstance(before, TerminalNode):
                if before.getText() == '*':
                    self.current_node.all_positional = True
                elif before.getText() == '**':
                    self.current_node.all_keywords = True

        if my_index < len(ctx.parentCtx.children) - 1:
            after = ctx.parentCtx.children[my_index + 1]
            if isinstance(after, TerminalNode) and after.getText() == '=':
                self.current_node.has_default = True

    def exitVar_arg_list(self, ctx):
        if isinstance(self.current_node, SemanticParser.FunctionInput):
            self.current_node = self.current_node.scope

    def exitFunc_def(self, ctx):
        self.current_node = self.current_node.scope

    class Condition(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return '<if>'

    def enterIf_stmt(self, ctx):
        node = SemanticParser.Condition(self.current_node)
        self.current_node.add(node)
        self.current_node = node

    def exitIf_stmt(self, ctx):
        self.current_node = self.current_node.scope

    class CycleByCond(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return '<while>'

    def enterWhile_stmt(self, ctx):
        node = SemanticParser.CycleByCond(self.current_node)
        self.current_node.add(node)
        self.current_node = node

    def exitWhile_stmt(self, ctx):
        self.current_node = self.current_node.scope

    class CycleByCollection(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return '<for>'

    def enterFor_stmt(self, ctx):
        node = SemanticParser.CycleByCollection(self.current_node)
        self.current_node.add(node)
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
        action = ctx.children[0].getText()
        node = SemanticParser.ControlFlow(action, self.current_node)
        self.current_node.add(node)
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
        name = ctx.children[1].getText()
        node = SemanticParser.Abstraction(name, self.current_node)
        self.current_node.add(node)
        self.current_node = node

    def exitClass_def(self, ctx):
        self.current_node = self.current_node.scope

    class Decorative(Global):
        def __init__(self, parts, scope):
            super().__init__(scope)
            self.parts = parts

        def __str__(self):
            return "<decorator: '{}'>".format('.'.join(self.parts))

    def enterDecorator(self, ctx):
        dotted_name = ctx.children[1]
        joined_name = ''.join(map(lambda x: x.getText(), dotted_name.children))
        node = SemanticParser.Decorative(joined_name.split('.'), self.current_node)
        self.current_node.add(node)
        self.current_node = node

    def exitDecorator(self, ctx):
        self.current_node = self.current_node.scope

    def enterTest(self, ctx):
        if len(ctx.children) == 1:
            pass

    class Disjunction(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return "<or>"

    def enterOr_test(self, ctx):
        if len(ctx.children) > 1:
            node = SemanticParser.Disjunction(self.current_node)
            self.current_node.add(node)
            self.current_node = node

    def exitOr_test(self, ctx):
        if isinstance(self.current_node, SemanticParser.Disjunction):
            if len(ctx.children) > 1:
                self.current_node = self.current_node.scope

    class Conjunction(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return "<and>"

    def enterAnd_test(self, ctx):
        if len(ctx.children) > 1:
            node = SemanticParser.Conjunction(self.current_node)
            self.current_node.add(node)
            self.current_node = node

    def exitAnd_test(self, ctx):
        if isinstance(self.current_node, SemanticParser.Conjunction):
            if len(ctx.children) > 1:
                self.current_node = self.current_node.scope

    class Negative(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return "<not>"

    def enterNot_test(self, ctx):
        if len(ctx.children) > 1:
            node = SemanticParser.Negative(self.current_node)
            self.current_node.add(node)
            self.current_node = node

    def exitNot_test(self, ctx):
        if isinstance(self.current_node, SemanticParser.Negative):
            if len(ctx.children) > 1:
                self.current_node = self.current_node.scope

    class Comparison(Global):
        def __init__(self, operator, scope):
            super().__init__(scope)
            self.operator = operator

        def __str__(self):
            return "<comp: '{}'>".format(self.operator)

    def enterComp_op(self, ctx):
        operator = ctx.children[0].getText()
        node = SemanticParser.Comparison(operator, self.current_node)

        left = self.current_node.body[-1]
        self.current_node.body.remove(left)
        node.add(left)

        self.current_node.add(node)
        self.current_node = node

    def exitComparison(self, ctx):
        while isinstance(self.current_node, SemanticParser.Comparison):
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
                operator = ctx.children[1].getText()
                node = SemanticParser.Assign(operator, self.current_node)

            elif isinstance(ctx.children[1], MiniPythonParser.Aug_assignContext):
                operator = ctx.children[1].children[0].getText()
                node = SemanticParser.AugAssign(operator, self.current_node)

            if node:
                self.current_node.add(node)
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
                operator = ctx.children[1].getText()
                node = SemanticParser.Addity(operator, self.current_node)
                self.current_node.add(node)
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
                operator = ctx.children[1].getText()
                node = SemanticParser.Multiply(operator, self.current_node)
                self.current_node.add(node)
                self.current_node = node

    def exitTerm(self, ctx):
        if isinstance(self.current_node, SemanticParser.Multiply):
            if len(ctx.children) > 1:
                self.current_node = self.current_node.scope

    def enterFactor(self, ctx):
        #TODO: support for unary operations
        if len(ctx.children) == 1:
            pass

    def exitFactor(self, ctx):
        if isinstance(self.current_node, (SemanticParser.Variable, SemanticParser.Constant)):
            self.current_node = self.current_node.scope

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

    class GenList(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return "<list>"

    class GenDict(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return "<dict>"

    def enterAtom(self, ctx):
        child = ctx.children[0]

        if isinstance(child, TerminalNode):
            text = child.getText()
            if text in ['True', 'False', 'None']:
                node = SemanticParser.Constant(text, self.current_node)
                self.current_node.add(node)

            elif text == '[':
                node = SemanticParser.GenList(self.current_node)
                self.current_node.add(node)
                self.current_node = node

            elif text == '{':
                node = SemanticParser.GenDict(self.current_node)
                self.current_node.add(node)
                self.current_node = node

            else:
                node = SemanticParser.Variable(text, self.current_node)
                self.current_node.add(node)
                self.current_node = node

        elif isinstance(child, (MiniPythonParser.NumberContext, MiniPythonParser.StringContext)):
            value = child.children[0].getText()
            node = SemanticParser.Constant(value, self.current_node)
            self.current_node.add(node)

    def exitAtom(self, ctx):
        if isinstance(self.current_node, (SemanticParser.GenList, SemanticParser.GenDict)) and len(ctx.children) > 1:
            self.current_node = self.current_node.scope

    class Call(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return "<call>".format()

    class Index(Global):
        def __init__(self, scope):
            super().__init__(scope)

        def __str__(self):
            return "<index>".format()

    class Resolve(Global):
        def __init__(self, name, scope):
            super().__init__(scope)
            self.name = name

        def __str__(self):
            return "<resolve: '{}'>".format(self.name)

    def enterTrailer(self, ctx):
        operator = ctx.children[0].getText()
        if operator == '.':
            text = ctx.children[1].getText()
            node = SemanticParser.Resolve(text, self.current_node)
            self.current_node.add(node)
            self.current_node = node

        elif operator == '(':
            node = SemanticParser.Call(self.current_node)
            self.current_node.add(node)
            self.current_node = node

        elif operator == '[':
            node = SemanticParser.Index(self.current_node)
            self.current_node.add(node)
            self.current_node = node

    def exitTrailer(self, ctx):
        if isinstance(self.current_node, (SemanticParser.Call, SemanticParser.Index, SemanticParser.Resolve)):
            self.current_node = self.current_node.scope

    def enterComp_for(self, ctx):
        node = SemanticParser.CycleByCollection(self.current_node)
        self.current_node.add(node)
        self.current_node = node

    def exitComp_for(self, ctx):
        self.current_node = self.current_node.scope

    def enterComp_if(self, ctx):
        node = SemanticParser.Condition(self.current_node)
        self.current_node.add(node)
        self.current_node = node

    def exitComp_if(self, ctx):
        self.current_node = self.current_node.scope

    def enterArgument(self, ctx):
        #TODO: parse different arguments
        pass

    def enterSubscript_list(self, ctx):
        # TODO: parse subscripts
        pass

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
