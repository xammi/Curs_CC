import sys
from antlr4 import *
from antlr4.tree.Trees import Trees

from antlr_out.MiniPythonLexer import MiniPythonLexer
from antlr_out.MiniPythonParser import MiniPythonParser
from llvm import generate_llvm

GRAMMAR = 'MiniPython'
ANTLR_CALL = 'antlr4 -Dlanguage=Python3 {}.g4 -o ../antlr_out'.format(GRAMMAR)


def get_antlr_parser(input_stream):
    lexer = MiniPythonLexer(input_stream)
    # tokens = lexer.getAllTokens()
    stream = CommonTokenStream(lexer)
    parser = MiniPythonParser(stream)
    return parser


def parse_single_input():
    input_seq = input('>>> ')
    parser = get_antlr_parser(InputStream(input_seq))
    tree = parser.single_input()
    print_tree(tree, sys.stdin)
    return tree


def parse_file_input(file_name):
    parser = get_antlr_parser(FileStream(file_name, encoding='utf-8'))
    tree = parser.file_input()

    with open(file_name + '.ast', 'w') as dest_file:
        print_tree(tree, dest_file)
    return tree


def print_tree(tree, place):
    def print_rec(sub_tree, depth):
        if isinstance(sub_tree, TerminalNode):
            token_type = sub_tree.symbol.type
            if token_type == MiniPythonParser.INDENT:
                text = '<indent>'
            elif token_type == MiniPythonParser.DEDENT:
                text = '<dedent>'
            elif token_type == MiniPythonParser.NEWLINE:
                text = '<newline>'
            else:
                text = sub_tree.getText()
                text = '\'' + text + '\''
        else:
            text = Trees.getNodeText(sub_tree, MiniPythonParser.ruleNames, None)
            text = '<' + text + '>'

        print(' ' * 2 * depth, text, file=place)

        if hasattr(sub_tree, 'children') and sub_tree.children:
            for child in sub_tree.children:
                print_rec(child, depth + 1)

    print_rec(tree, 0)


def main():
    examples = [
        'fact.ex',
        'web_view.ex',
        'logger.ex',
        'simple.ex',
    ]
    for index, example in enumerate(examples, start=1):
        print('{}. {}'.format(index, example))

    action = input('>>> ') or None
    if action:
        action = int(action)
        file_name = 'examples/' + examples[action - 1]
        tree = parse_file_input(file_name)
        generate_llvm(tree, file_name)
        print('Success!')
    else:
        print('Goodbye!')


if __name__ == '__main__':
    main()
