from antlr4 import *
from antlr_out.MiniPythonListener import MiniPythonListener


llvm_header = '''
; ModuleID = '{}'
source_filename = "{}"
target datalayout = "e-m:o-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.12.0"
'''

llvm_attributes = '''
attributes #0 = {
    nounwind ssp uwtable
    "disable-tail-calls"="false"
    "less-precise-fpmad"="false"
    "no-frame-pointer-elim"="true"
    "no-frame-pointer-elim-non-leaf"
    "no-infs-fp-math"="false"
    "no-nans-fp-math"="false"
    "stack-protector-buffer-size"="8"
    "target-cpu"="penryn"
    "target-features"="+cx16,+fxsr,+mmx,+sse,+sse2,+sse3,+sse4.1,+ssse3"
    "unsafe-fp-math"="false"
    "use-soft-float"="false"
}'''

llvm_footer = '''
!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"PIC Level", i32 2}
!1 = !{!"Apple LLVM version 8.0.0 (clang-800.0.42.1)"}
'''


class Runtime(MiniPythonListener):
    def visitTerminal(self, node):
        print('Visit terminal %s' % node.getText())


def generate_llvm(tree, file_name):
    result = ''

    walker = ParseTreeWalker()
    runtime = Runtime()
    walker.walk(runtime, tree)

    llvm_code = llvm_header.format(file_name) + result + llvm_attributes + llvm_footer
    with open(file_name + '.ll', 'w') as dest_file:
        dest_file.write(llvm_code)
