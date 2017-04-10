# Generated from MiniPython.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MiniPythonParser import MiniPythonParser
else:
    from MiniPythonParser import MiniPythonParser

# This class defines a complete listener for a parse tree produced by MiniPythonParser.
class MiniPythonListener(ParseTreeListener):

    # Enter a parse tree produced by MiniPythonParser#single_input.
    def enterSingle_input(self, ctx:MiniPythonParser.Single_inputContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#single_input.
    def exitSingle_input(self, ctx:MiniPythonParser.Single_inputContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#file_input.
    def enterFile_input(self, ctx:MiniPythonParser.File_inputContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#file_input.
    def exitFile_input(self, ctx:MiniPythonParser.File_inputContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#decorator.
    def enterDecorator(self, ctx:MiniPythonParser.DecoratorContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#decorator.
    def exitDecorator(self, ctx:MiniPythonParser.DecoratorContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#decorators.
    def enterDecorators(self, ctx:MiniPythonParser.DecoratorsContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#decorators.
    def exitDecorators(self, ctx:MiniPythonParser.DecoratorsContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#decorated.
    def enterDecorated(self, ctx:MiniPythonParser.DecoratedContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#decorated.
    def exitDecorated(self, ctx:MiniPythonParser.DecoratedContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#func_def.
    def enterFunc_def(self, ctx:MiniPythonParser.Func_defContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#func_def.
    def exitFunc_def(self, ctx:MiniPythonParser.Func_defContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#var_arg_list.
    def enterVar_arg_list(self, ctx:MiniPythonParser.Var_arg_listContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#var_arg_list.
    def exitVar_arg_list(self, ctx:MiniPythonParser.Var_arg_listContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#vfpdef.
    def enterVfpdef(self, ctx:MiniPythonParser.VfpdefContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#vfpdef.
    def exitVfpdef(self, ctx:MiniPythonParser.VfpdefContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#stmt.
    def enterStmt(self, ctx:MiniPythonParser.StmtContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#stmt.
    def exitStmt(self, ctx:MiniPythonParser.StmtContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#simple_stmt.
    def enterSimple_stmt(self, ctx:MiniPythonParser.Simple_stmtContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#simple_stmt.
    def exitSimple_stmt(self, ctx:MiniPythonParser.Simple_stmtContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#expr_stmt.
    def enterExpr_stmt(self, ctx:MiniPythonParser.Expr_stmtContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#expr_stmt.
    def exitExpr_stmt(self, ctx:MiniPythonParser.Expr_stmtContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#testlist_star_expr.
    def enterTestlist_star_expr(self, ctx:MiniPythonParser.Testlist_star_exprContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#testlist_star_expr.
    def exitTestlist_star_expr(self, ctx:MiniPythonParser.Testlist_star_exprContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#aug_assign.
    def enterAug_assign(self, ctx:MiniPythonParser.Aug_assignContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#aug_assign.
    def exitAug_assign(self, ctx:MiniPythonParser.Aug_assignContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#flow_stmt.
    def enterFlow_stmt(self, ctx:MiniPythonParser.Flow_stmtContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#flow_stmt.
    def exitFlow_stmt(self, ctx:MiniPythonParser.Flow_stmtContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#compound_stmt.
    def enterCompound_stmt(self, ctx:MiniPythonParser.Compound_stmtContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#compound_stmt.
    def exitCompound_stmt(self, ctx:MiniPythonParser.Compound_stmtContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#if_stmt.
    def enterIf_stmt(self, ctx:MiniPythonParser.If_stmtContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#if_stmt.
    def exitIf_stmt(self, ctx:MiniPythonParser.If_stmtContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#while_stmt.
    def enterWhile_stmt(self, ctx:MiniPythonParser.While_stmtContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#while_stmt.
    def exitWhile_stmt(self, ctx:MiniPythonParser.While_stmtContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#for_stmt.
    def enterFor_stmt(self, ctx:MiniPythonParser.For_stmtContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#for_stmt.
    def exitFor_stmt(self, ctx:MiniPythonParser.For_stmtContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#suite.
    def enterSuite(self, ctx:MiniPythonParser.SuiteContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#suite.
    def exitSuite(self, ctx:MiniPythonParser.SuiteContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#test.
    def enterTest(self, ctx:MiniPythonParser.TestContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#test.
    def exitTest(self, ctx:MiniPythonParser.TestContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#or_test.
    def enterOr_test(self, ctx:MiniPythonParser.Or_testContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#or_test.
    def exitOr_test(self, ctx:MiniPythonParser.Or_testContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#and_test.
    def enterAnd_test(self, ctx:MiniPythonParser.And_testContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#and_test.
    def exitAnd_test(self, ctx:MiniPythonParser.And_testContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#not_test.
    def enterNot_test(self, ctx:MiniPythonParser.Not_testContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#not_test.
    def exitNot_test(self, ctx:MiniPythonParser.Not_testContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#comparison.
    def enterComparison(self, ctx:MiniPythonParser.ComparisonContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#comparison.
    def exitComparison(self, ctx:MiniPythonParser.ComparisonContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#comp_op.
    def enterComp_op(self, ctx:MiniPythonParser.Comp_opContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#comp_op.
    def exitComp_op(self, ctx:MiniPythonParser.Comp_opContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#star_expr.
    def enterStar_expr(self, ctx:MiniPythonParser.Star_exprContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#star_expr.
    def exitStar_expr(self, ctx:MiniPythonParser.Star_exprContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#expr.
    def enterExpr(self, ctx:MiniPythonParser.ExprContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#expr.
    def exitExpr(self, ctx:MiniPythonParser.ExprContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#term.
    def enterTerm(self, ctx:MiniPythonParser.TermContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#term.
    def exitTerm(self, ctx:MiniPythonParser.TermContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#factor.
    def enterFactor(self, ctx:MiniPythonParser.FactorContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#factor.
    def exitFactor(self, ctx:MiniPythonParser.FactorContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#trailer.
    def enterTrailer(self, ctx:MiniPythonParser.TrailerContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#trailer.
    def exitTrailer(self, ctx:MiniPythonParser.TrailerContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#subscript_list.
    def enterSubscript_list(self, ctx:MiniPythonParser.Subscript_listContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#subscript_list.
    def exitSubscript_list(self, ctx:MiniPythonParser.Subscript_listContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#atom.
    def enterAtom(self, ctx:MiniPythonParser.AtomContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#atom.
    def exitAtom(self, ctx:MiniPythonParser.AtomContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#list_compr.
    def enterList_compr(self, ctx:MiniPythonParser.List_comprContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#list_compr.
    def exitList_compr(self, ctx:MiniPythonParser.List_comprContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#dict_compr.
    def enterDict_compr(self, ctx:MiniPythonParser.Dict_comprContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#dict_compr.
    def exitDict_compr(self, ctx:MiniPythonParser.Dict_comprContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#expr_list.
    def enterExpr_list(self, ctx:MiniPythonParser.Expr_listContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#expr_list.
    def exitExpr_list(self, ctx:MiniPythonParser.Expr_listContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#test_list.
    def enterTest_list(self, ctx:MiniPythonParser.Test_listContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#test_list.
    def exitTest_list(self, ctx:MiniPythonParser.Test_listContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#class_def.
    def enterClass_def(self, ctx:MiniPythonParser.Class_defContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#class_def.
    def exitClass_def(self, ctx:MiniPythonParser.Class_defContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#arg_list.
    def enterArg_list(self, ctx:MiniPythonParser.Arg_listContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#arg_list.
    def exitArg_list(self, ctx:MiniPythonParser.Arg_listContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#argument.
    def enterArgument(self, ctx:MiniPythonParser.ArgumentContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#argument.
    def exitArgument(self, ctx:MiniPythonParser.ArgumentContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#comp_iter.
    def enterComp_iter(self, ctx:MiniPythonParser.Comp_iterContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#comp_iter.
    def exitComp_iter(self, ctx:MiniPythonParser.Comp_iterContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#comp_for.
    def enterComp_for(self, ctx:MiniPythonParser.Comp_forContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#comp_for.
    def exitComp_for(self, ctx:MiniPythonParser.Comp_forContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#comp_if.
    def enterComp_if(self, ctx:MiniPythonParser.Comp_ifContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#comp_if.
    def exitComp_if(self, ctx:MiniPythonParser.Comp_ifContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#dotted_name.
    def enterDotted_name(self, ctx:MiniPythonParser.Dotted_nameContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#dotted_name.
    def exitDotted_name(self, ctx:MiniPythonParser.Dotted_nameContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#string.
    def enterString(self, ctx:MiniPythonParser.StringContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#string.
    def exitString(self, ctx:MiniPythonParser.StringContext):
        pass


    # Enter a parse tree produced by MiniPythonParser#number.
    def enterNumber(self, ctx:MiniPythonParser.NumberContext):
        pass

    # Exit a parse tree produced by MiniPythonParser#number.
    def exitNumber(self, ctx:MiniPythonParser.NumberContext):
        pass


