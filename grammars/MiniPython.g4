grammar MiniPython;

tokens { INDENT, DEDENT }

@lexer::members {
    self.tokens = []
    self.indents = []
    self.opened = 0
    self.last_token = None
    self.INDENT, self.DEDENT = 59, 60

def get_indent_cnt(self, spaces):
    return len(spaces)

def emit(self):
    token = super().emit()
    self.tokens.append(token)
    return token

def emit_special(self, type, text=''):
    start = self._tokenStartCharIndex
    stop = start + len(text)
    self._tokenStartCharIndex = stop

    special = self._factory.create(self._tokenFactorySourcePair, type, text, Token.DEFAULT_CHANNEL,
        start, stop, self._tokenStartLine, self._tokenStartColumn)
    self.emitToken(special)
    self.tokens.append(special)
    return special

def nextToken(self):
    if self._input.LA(1) == Token.EOF and self.indents:
        self.emit_special(self.NEWLINE, '\n')
        while self.indents:
            self.emit_special(self.DEDENT)
            self.indents.pop()
        self.emitEOF()

    next = super().nextToken()
    if next.channel == Token.DEFAULT_CHANNEL:
        self.last_token = next
    return self.tokens.pop(0) if self.tokens else next
}

/*
 * start grammar rules
 */

single_input : NEWLINE | simple_stmt | compound_stmt NEWLINE ;
file_input : ( NEWLINE | stmt )* EOF ;

/*
 * syntax rules
 */

decorator : '@' dotted_name ( '(' arg_list ')' )? NEWLINE ;
decorators : decorator+ ;
decorated : decorators ( class_def | func_def ) ;

func_def : DEF NAME '(' var_arg_list? ')' ':' suite ;
var_arg_list
  : vfpdef ( ',' vfpdef )* ( ',' vfpdef '=' test )* (',' '*' vfpdef )? (',' '**' vfpdef )?
  | vfpdef '=' test ( ',' vfpdef '=' test )* (',' '*' vfpdef )? ( ',' '**' vfpdef )?
  | '*' vfpdef ( ',' '**' vfpdef )?
  | '**' vfpdef ;
vfpdef : NAME ;

stmt : simple_stmt | compound_stmt ;
simple_stmt : ( expr_stmt | flow_stmt ) NEWLINE ;

expr_stmt : testlist_star_expr ( '=' test | aug_assign | test_list ( '=' testlist_star_expr )* ) ;
testlist_star_expr : ( test | star_expr ) ( ',' ( test | star_expr ) )* ','? ;
aug_assign : ADD_ASSIGN | SUB_ASSIGN | MULT_ASSIGN | DIV_ASSIGN | MOD_ASSIGN ;
flow_stmt : PASS | BREAK | CONTINUE | RETURN test_list? ;

compound_stmt : if_stmt | while_stmt | for_stmt  | func_def | class_def | decorated ;
if_stmt : IF test ':' suite ( ELIF test ':' suite )* ( ELSE ':' suite )? ;
while_stmt : WHILE test ':' suite ;
for_stmt : FOR expr_list IN test_list ':' suite ;

suite : simple_stmt | NEWLINE INDENT stmt+ DEDENT ;

test : or_test ( IF or_test ELSE test )? ;
or_test : and_test ( OR and_test )* ;
and_test : not_test ( AND not_test )* ;
not_test : NOT not_test | comparison ;

comparison : star_expr ( comp_op star_expr )* ;
comp_op : LESS_THAN | GREATER_THAN | EQUALS | NOT_EQ | GT_EQ | LT_EQ | IN | NOT IN | IS | IS NOT ;
star_expr : '*'? expr ;

expr : term ( ( '+' | '-' ) term )* ;
term : factor ( ( '*' | '/' | '%' ) factor )* ;
factor : ( '+' | '-' ) factor | atom trailer* ;

trailer : '(' arg_list? ')' | '[' subscript_list ']' | '.' NAME ;
subscript_list : test | test? ':' test? ;
atom : NAME | string+ | number | NONE | TRUE | FALSE | '(' list_compr? ')' | '[' list_compr? ']' | '{' dict_compr? '}' ;
list_compr : test ( comp_for | (',' test)* ','? ) ;
dict_compr : test ':' test ( comp_for | ',' test ':' test )* ','? ;
expr_list : star_expr ( ',' star_expr )* ','? ;
test_list : test ( ',' test )* ','? ;

class_def : CLASS NAME ( '(' arg_list ')' )? ':' suite ;
arg_list : argument ( ',' argument )* ','? ;
argument : test comp_for? | test '=' test | '*' test | '**' test ;

comp_iter : comp_for | comp_if ;
comp_for : FOR expr_list IN or_test comp_iter ;
comp_if : IF or_test comp_iter? ;

dotted_name : NAME ( '.' NAME )* ;
string : STRING ;
number : INTEGER | FLOAT ;

/*
 * lexer rules
 */

NEWLINE : ( '\r'? '\n' | '\r' | '\f' ) SPACES?
{
import re
new_line = re.sub('[^\r\n\f]+', '', self.text)
spaces = re.sub('[\r\n\f]+', '', self.text)
next = self._input.LA(1)

if self.opened > 0 or next in [10, 13, 12, 35]:
    self.skip()
else:
    self.emit_special(self.NEWLINE, new_line)
    indent = self.get_indent_cnt(spaces)
    previous = self.indents[-1] if self.indents else 0

    if indent == previous:
        self.skip()
    elif indent > previous:
        self.indents.append(indent)
        self.emit_special(self.INDENT, spaces)
    else:
        while self.indents and self.indents[-1] > indent:
            self.emit_special(self.DEDENT)
            self.indents.pop()
};

DEF : 'def' ;
RETURN : 'return' ;
FROM : 'from' ;
IMPORT : 'import' ;
AS : 'as' ;
IF : 'if' ;
ELIF : 'elif' ;
ELSE : 'else' ;
WHILE : 'while' ;
FOR : 'for' ;
IN : 'in' ;
OR : 'or' ;
AND : 'and' ;
NOT : 'not' ;
IS : 'is' ;
NONE : 'None' ;
TRUE : 'True' ;
FALSE : 'False' ;
CLASS : 'class' ;
DEL : 'del' ;
PASS : 'pass' ;
CONTINUE : 'continue' ;
BREAK : 'break' ;

OPEN_PAREN : '(' {self.opened += 1} ;
CLOSE_PAREN : ')' {self.opened -= 1} ;
OPEN_BRACK : '[' {self.opened += 1} ;
CLOSE_BRACK : ']' {self.opened -= 1} ;
OPEN_BRACE : '{' {self.opened += 1} ;
CLOSE_BRACE : '}' {self.opened -= 1} ;

DOT : '.' ;
STAR : '*' ;
COMMA : ',' ;
COLON : ':' ;
ASSIGN : '=' ;
AT : '@' ;

LESS_THAN : '<' ;
GREATER_THAN : '>' ;
EQUALS : '==' ;
GT_EQ : '>=' ;
LT_EQ : '<=' ;
NOT_EQ : '!=' ;

ADD : '+' ;
MINUS : '-' ;
DIV : '/' ;
MOD : '%' ;

ADD_ASSIGN : '+=' ;
SUB_ASSIGN : '-=' ;
MULT_ASSIGN : '*=' ;
DIV_ASSIGN : '/=' ;
MOD_ASSIGN : '%=' ;

NAME : ID_START ID_CONTINUE* ;
STRING : SHORT_STRING | LONG_STRING ;
INTEGER : '0' | [1-9] [0-9]* ;
FLOAT : POINT_FLOAT | EXPONENT_FLOAT ;

SKIP_ : ( SPACES | COMMENT | LINE_JOINING ) -> skip ;

UNKNOWN_CHAR : . ;

fragment SHORT_STRING : '\'' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f'] )* '\'' | '"' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f"] )* '"' ;
fragment LONG_STRING : '\'\'\'' LONG_STRING_ITEM*? '\'\'\'' | '"""' LONG_STRING_ITEM*? '"""' ;
fragment LONG_STRING_ITEM : ~'\\' | STRING_ESCAPE_SEQ ;
fragment STRING_ESCAPE_SEQ : '\\' . ;

fragment POINT_FLOAT : INT_PART? FRACTION | INT_PART '.' ;
fragment EXPONENT_FLOAT : ( INT_PART | POINT_FLOAT ) EXPONENT ;

fragment INT_PART : [0-9]+ ;
fragment FRACTION : '.' INT_PART ;
fragment EXPONENT : [eE] [+-]? INT_PART ;

fragment ID_START : '_' | [A-Z] | [a-z] ;
fragment ID_CONTINUE : ID_START | [0-9] ;

fragment COMMENT : '#' ~[\r\n\f]* ;
fragment LINE_JOINING : '\\' SPACES? ( '\r'? '\n' | '\r' | '\f' ) ;
fragment SPACES : [ \t]+ ;
