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


def GenerateCode(node):
    res = ''
    if node is None:
        return ''

    if not isinstance(node, ASTNode):
        if str(node) == 'input':
            return 'prompt'
        else:
            return str(node)

    if node.type == 'PROGRAM':
        res = res + GenerateCode(node.children[2])

    if node.type == 'PERMISSION':
        pass

    if node.type == 'DEFINE_LIST':
        for child in node.children:
            res = res + GenerateCode(child) + ' '

    if node.type == 'VAR_DEFINE':
        res = res + 'var %s=%s;' % (node.children[1], GenerateCode(node.children[2]))

    if node.type == 'FUNC_DEFINE':
        res = res + 'function %s(%s)%s' % (
        node.children[3], GenerateCode(node.children[4]), GenerateCode(node.children[5]))

    if node.type == 'TYPE':
        pass

    if node.type == 'EXP':
        res = res + '(%s)' % ''.join([GenerateCode(c) for c in node.children])

    if node.type == 'COMPUTE_EXP':
        res = res + '(%s)' % ''.join([GenerateCode(c) for c in node.children])

    if node.type == 'TERM_BEFORE':
        res = res + ''.join([GenerateCode(c) for c in node.children])

    if node.type == 'RELATION_OP':
        res = res + GenerateCode(node.children[0]) + GenerateCode(node.children[1])

    if node.type == 'TERM':
        if isinstance(node.children[0], ASTNode):
            if node.children[0].type == 'EXP':
                res = res + GenerateCode(node.children[1])
        else:
            if len(node.children) == 2:
                res = res + GenerateCode(node.children[0]) + GenerateCode(node.children[1])
            else:
                res = res + GenerateCode(node.children[0])

    if node.type == 'BIN_OP':
        res = res + GenerateCode(node.children[0])

    if node.type == 'REL_OP':
        res = res + GenerateCode(node.children[0])

    if node.type == 'ID_FOLLOW_CALL':
        leng = len(node.children)
        res = res + '(%s)' % ''.join(
            [GenerateCode(c) + (',' if i < leng - 1 else '') for (i, c) in enumerate(node.children)])

    if node.type == 'ID_FOLLOW_DOT':
        is_length_call = False
        try:
            if node.children[0] == 'length' and node.children[1].type == 'ID_FOLLOW_CALL':
                res = res + '.length'
                is_length_call = True
        except:
            pass
        if not is_length_call:
            res = res + '.%s%s' % (GenerateCode(node.children[0]), GenerateCode(node.children[1]))

    if node.type == 'ID_INDEX':
        res = res + '[%s]' % GenerateCode(node.children[0])

    if node.type == 'ID_FOLLOW_EMPTY':
        pass

    if node.type == 'STATIC':
        pass

    if node.type == 'PARAMS':
        if node.children:
            leng = len(node.children)
            res = res + ''.join([GenerateCode(c) + (',' if i < leng - 1 else '') for (i, c) in enumerate(node.children)])

    if node.type == 'PARAM':
        res = res + GenerateCode(node.children[1])

    if node.type == 'BLOCK':
        res = res + '{%s}' % ''.join([GenerateCode(c) for c in node.children])

    if node.type == 'LOCAL_DEFINE_LIST':
        return ' '.join([GenerateCode(c) for c in node.children])

    if node.type == 'LOCAL_VAR_DEFINE':
        res = res + 'let %s=%s;' % (GenerateCode(node.children[1]), GenerateCode(node.children[2]))

    if node.type == 'CODE_LIST':
        res = res + ''.join([GenerateCode(c) for c in node.children])

    if node.type == 'CODE':
        res = res + GenerateCode(node.children[0])

    if node.type == 'NORMAL_STATE_ASSIGN':
        res = res + '%s%s=%s;' % tuple([GenerateCode(c) for c in node.children])

    if node.type == 'NORMAL_STATE_CALL':
        is_system_out_println = False
        try:
            if node.children[0] == 'System':
                if node.children[1].type == 'ID_FOLLOW_DOT':
                    if node.children[1].children[0] == 'out':
                        if node.children[1].children[1].type == 'ID_FOLLOW_DOT':
                            if node.children[1].children[1].children[0] == 'println':
                                res = res + 'console.log%s;' % (GenerateCode(node.children[1].children[1].children[1]))
                                is_system_out_println = True
        except:
            pass
        if not is_system_out_println:
            res = res + '%s%s;' % (GenerateCode(node.children[0]), GenerateCode(node.children[1]))

    if node.type == 'NORMAL_STATE_CONTROL':
        res = res + GenerateCode(node.children[0])

    if node.type == 'SELECT_STATE':
        res = res + 'if(%s){%s}%s' % tuple([GenerateCode(c) for c in node.children])

    if node.type == 'SELECT_FOLLOW':
        if node.children[0] is not None and node.children[0].type != 'EMPTY':
            res = res + 'else{%s}' % GenerateCode(node.children[0])

    if node.type == 'LOOP_STATE':
        return GenerateCode(node.children[0])

    if node.type == 'FOR_LOOP':
        res = 'for(%s;%s;%s){%s}' % tuple([GenerateCode(c) for c in node.children])

    if node.type == 'WHILE_LOOP':
        res = 'while(%s){%s}' % (GenerateCode(node.children[0]), GenerateCode(node.children[1]))

    if node.type == 'RETURN_STATE':
        if len(node.children) == 0:
            res = res + 'return;'
        else:
            res = res + 'return %s;' % GenerateCode(node.children[0])

    if node.type == 'EMPTY':
        pass
    return res


def GenerateProgram(root):
    res = GenerateCode(root);
    res = res + 'main();'
    return res
