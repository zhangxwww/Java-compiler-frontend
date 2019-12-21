from syntax import ASTNode
import re


class Error(Exception):
    pass


class StackOverflowError(Error):
    def __init__(self):
        pass

    def text(self):
        print('Stack Overflow!')


class StackUnderflowError(Error):
    def __init__(self):
        pass

    def text(self):
        print('Stack Underflow')


MAX_STACK_DEPTH = 15


class Stack:
    def __init__(self):
        self.arr = [None for i in range(MAX_STACK_DEPTH)]
        self.top = -1

    def push(self, x):
        if self.top < MAX_STACK_DEPTH - 1:
            self.top = self.top + 1
            self.arr[self.top] = x
        else:
            raise StackOverflowError

    def pop(self):
        if self.top >= 0:
            x = self.arr[self.top]
            self.top = self.top - 1
            return x
        else:
            raise StackUnderflowError


class CodeGenerator:
    def __init__(self, root):
        self.counter = 0
        self.root = root
        self.import_java_util_scanner = False

    def generateTAC(self, node):
        '''
        根据表达式节点产生三地址码
        :param node: 表达式的ASTNode
        :return: 产生的一系列语句和最终的变量名，最终为v[self.counter]命名产生的最后变量
        '''
        if node.type == 'TERM':
            numberOfChildren = len(node.children)
            if numberOfChildren == 1:
                if isinstance(node.children[0], ASTNode) and node.children[0].type == 'EXP':
                    return self.generateTAC(node.children[0])
                else:
                    self.counter = self.counter + 1
                    res = 'let v%d=%s;\n' % (self.counter, self.generateCode(node.children[0]))
                    return res, 'v%d' % self.counter
            elif numberOfChildren == 2:
                id = node.children[0]
                follow = node.children[1]
                if id == 'Float' and follow.type == "ID_FOLLOW_DOT":
                    self.counter += 1
                    res = 'let v%d=%s;\n' % (self.counter, self.generateCode(follow)[1:])
                    return res, 'v%d' % self.counter
                if follow.type == 'ID_FOLLOW_INDEX':
                    preamble, varname = self.generateTAC(follow.children[0])
                    self.counter = self.counter + 1
                    res = '%s let v%d=%s[%s];\n' % (preamble, self.counter, self.generateCode(id), varname)
                    return res, 'v%d' % self.counter
                if follow.type == 'ID_FOLLOW_DOT':
                    """
                    preamable, _ = self.generateTAC(follow.children[1])
                    self.counter = self.counter + 1
                    res = '%s let v%d=%s.%s;\n' % (preamable, self.counter, self.generateCode(id), self.generateCode(follow))
                    return res, self.counter
                    """
                    self.counter = self.counter + 1
                    res = 'let v%d=%s%s;\n' % (self.counter, self.generateCode(id), self.generateCode(follow))
                    return res, 'v%d' % self.counter
                if follow.type == 'ID_FOLLOW_CALL':
                    arglist = node.children[1].children
                    varlist = []
                    preambles = ''
                    for arg in arglist:
                        preamble, varname = self.generateTAC(arg)
                        preambles = preambles + preamble
                        varlist.append(varname)
                    lengthOfVarlist = len(varlist)
                    self.counter = self.counter + 1
                    res = '%s let v%d=%s(' % (preambles, self.counter, self.generateCode(id))
                    for (i, varname) in enumerate(varlist):
                        res = res + varname
                        if i != lengthOfVarlist - 1:
                            res = res + ','
                    res = res + ');\n'
                    return res, 'v%d' % self.counter
                if follow.type == 'ID_FOLLOW_EMPTY':
                    self.counter = self.counter + 1
                    res = 'let v%d=%s;\n' % (self.counter, self.generateCode(id))
                    return res, 'v%d' % self.counter
        if node.type == 'EXP':
            numberOfChildren = len(node.children)
            if numberOfChildren == 1:
                # 表达式为一个term
                return self.generateTAC(node.children[0])
            elif numberOfChildren == 2:
                preamble, varname = self.generateTAC(node.children[1])
                self.counter = self.counter + 1
                res = '%s let v%d=%s%s;\n' % (preamble, self.counter, self.generateCode(node.children[0]), varname)
                return res, 'v%d' % self.counter
            elif numberOfChildren == 3:
                preamble1, varname1 = self.generateTAC(node.children[0])
                preamble2, varname2 = self.generateTAC(node.children[2])
                self.counter = self.counter + 1
                res = '%s %s let v%d=%s%s%s;\n' % (
                    preamble1, preamble2,
                    self.counter,
                    varname1, self.generateCode(node.children[1]), varname2)
                return res, 'v%d' % self.counter

    def generateCode(self, node):
        res = ''
        if node is None:
            return ''

        if not isinstance(node, ASTNode):
            if str(node) == 'input':
                return 'prompt'
            elif str(node) == '==':
                return '==='
            elif str(node) == '!=':
                return '!=='
            elif str(node) == ';\n':
                return ';\n\n'
            else:
                return str(node)

        if node.type == 'PROGRAM':
            res = res + self.generateCode(node.children[0]) + self.generateCode(node.children[3])

        if node.type == 'IMPORT_STATE':
            special_import_cases = False
            if node.children[0] == 'java':
                if node.children[1].children[0] == 'util':
                    if node.children[2].children[0] == 'Scanner':
                        self.import_java_util_scanner = True
                        special_import_cases = True
                    if node.children[2].children[0] == 'Stack':
                        special_import_cases = True
                        res = res \
                              + \
'''
class Stack{
    constructor(){
        this.data = new Array();
        this.len = 0;
    }
    push(x){
        this.data.push(x);
        this.len += 1;
    }
    pop(){
        if(this.len>0){
            this.len -= 1;
        }
        return this.data.pop();
    }
    empty(){
        return this.len <= 0;
    }
}
'''
            if not special_import_cases:
                res = res + "import %s.%s.%s;\n" % (
                    node.children[0], node.children[1].children[0], node.children[2].children[0])

        if node.type == 'PERMISSION':
            pass

        if node.type == 'DEFINE_LIST':
            for child in node.children:
                res = res + self.generateCode(child) + ' '

        if node.type == 'VAR_DEFINE':
            hook, varname = self.generateTAC(node.children[2])
            res = res + '%svar %s=%s;\n' % (hook, node.children[1], varname)

        if node.type == 'FUNC_DEFINE':
            if node.children[3] == 'input' and self.import_java_util_scanner:
                res = res
            else:
                res = res + 'function %s(%s)%s' % (node.children[3], self.generateCode(node.children[4]), self.generateCode(node.children[5]))

        if node.type == 'TYPE':
            pass

        if node.type == 'EXP':
            res = res + '%s' % ''.join([self.generateCode(c) for c in node.children])

        if node.type == 'TERM':
            if isinstance(node.children[0], ASTNode) and node.children[0].type == 'EXP':
                res = res + '(%s)' % self.generateCode(node.children[0])
            else:
                res = res + ''.join([self.generateCode(c) for c in node.children])

        if node.type == 'BIN_OP' or node.type == 'UN_OP':
            res = res + self.generateCode(node.children[0])

        if node.type == 'ID_FOLLOW_CALL':
            leng = len(node.children)
            res = res + '(%s)' % ''.join(
                [self.generateCode(c) + (',' if i < leng - 1 else '') for (i, c) in enumerate(node.children)])

        if node.type == 'ID_FOLLOW_DOT':
            is_length_call = False
            try:
                if node.children[0] == 'length' and node.children[1].type == 'ID_FOLLOW_CALL':
                    res = res + '.length'
                    is_length_call = True
            except:
                pass
            if not is_length_call:
                res = res + '.%s%s' % (self.generateCode(node.children[0]), self.generateCode(node.children[1]))

        if node.type == 'ID_FOLLOW_INDEX':
            res = res + '[%s]' % self.generateCode(node.children[0])

        if node.type == 'ID_FOLLOW_EMPTY':
            pass

        if node.type == 'STATIC':
            pass

        if node.type == 'PARAMS':
            if node.children:
                leng = len(node.children)
                res = res + ''.join(
                    [self.generateCode(c) + (',' if i < leng - 1 else '') for (i, c) in enumerate(node.children)])

        if node.type == 'PARAM':
            res = res + self.generateCode(node.children[1])

        if node.type == 'BLOCK':
            res = res + '{\n%s}\n' % ''.join([self.generateCode(c) for c in node.children])

        if node.type == 'LOCAL_DEFINE_LIST':
            return ' '.join([self.generateCode(c) for c in node.children])

        if node.type == 'LOCAL_VAR_DEFINE':
            hook, varname = self.generateTAC(node.children[2])
            res = res + '%slet %s=%s;\n' % (hook, self.generateCode(node.children[1]), varname)

        if node.type == 'LOCAL_VAR_DEFINE_WITH_CONSTRUCTOR':
            res = res + 'let %s=new %s(%s);\n' % (
                self.generateCode(node.children[1]), self.generateCode(node.children[0].children[0]),
                self.generateCode(node.children[4]))

        if node.type == 'CODE_LIST':
            res = res + ''.join([self.generateCode(c) for c in node.children])

        if node.type == 'CODE':
            res = res + self.generateCode(node.children[0])

        if node.type == 'NORMAL_STATE_ASSIGN':
            hook, varname = self.generateTAC(node.children[2])
            res = res + '%s%s%s=%s;\n' % (hook, self.generateCode(node.children[0]), self.generateCode(node.children[1]), varname)

        if node.type == 'NORMAL_STATE_CALL':
            is_system_out_println = False
            try:
                if node.children[0] == 'System':
                    if node.children[1].type == 'ID_FOLLOW_DOT':
                        if node.children[1].children[0] == 'out':
                            if node.children[1].children[1].type == 'ID_FOLLOW_DOT':
                                if node.children[1].children[1].children[0] == 'println':
                                    res = res + 'console.log%s;\n' % (
                                        self.generateCode(node.children[1].children[1].children[1]))
                                    is_system_out_println = True
            except:
                pass
            if not is_system_out_println:
                res = res + '%s%s;\n' % (self.generateCode(node.children[0]), self.generateCode(node.children[1]))

        if node.type == 'NORMAL_STATE_CONTROL':
            res = res + self.generateCode(node.children[0])

        if node.type == 'SELECT_STATE':
            res = res + 'if(%s){%s}%s' % tuple([self.generateCode(c) for c in node.children])

        if node.type == 'SELECT_FOLLOW':
            if node.children[0] is not None and node.children[0].type != 'EMPTY':
                res = res + 'else{%s}' % self.generateCode(node.children[0])

        if node.type == 'LOOP_STATE':
            return self.generateCode(node.children[0])

        if node.type == 'FOR_LOOP':
            res = '%s for(;%s;){\n%s%s}\n' % (
                self.generateCode(node.children[0]),
                self.generateCode(node.children[1]),
                self.generateCode(node.children[3]),
                self.generateCode(node.children[2])
            )

        if node.type == 'WHILE_LOOP':
            res = 'while(%s){\n%s}\n' % (self.generateCode(node.children[0]), self.generateCode(node.children[1]))

        if node.type == 'RETURN_STATE':
            if len(node.children) == 0:
                res = res + 'return;\n'
            else:
                hook, varname = self.generateTAC(node.children[0])
                res = res + '%s return %s;\n' % (hook, varname)

        if node.type == 'ARRAY_DEFINE' or node.type == 'LOCAL_ARRAY_DEFINE':
            if node.children[0].children[0] != node.children[2].children[0]:
                print('Type Error!')
                return
            res = res + '%s=new Array(%s);\n' % (self.generateCode(node.children[1]), self.generateCode(node.children[3]))

        if node.type == 'EMPTY':
            pass
        return res

    def generateProgram(self):
        res = self.generateCode(self.root)
        res = res + 'main();'
        return res
