"""
!!! **DON't** change any comment in this file !!!

"""

import ply.yacc as yacc

"""
!!! **DON't** delete the following import !!!

"""
from lexical import tokens


class ASTNode:
    def __init__(self, type_, children=None):
        self.type = type_
        self.children = children

    def __repr__(self):
        res = '<{}>'.format(self.type) + '\n'
        child_res = []
        if self.children is not None and len(self.children) > 0:
            for child in self.children:
                child_res.append(child.__repr__())
        for r in child_res:
            res = res + '-'
            lines = r.split('\n')
            for line in lines:
                line = '  ' + line
                res = res + line + '\n'
        return res


start = 'PROGRAM'

precedence = (
    ('right', 'inc', 'not'),
    ('left', 'or'),
    ('left', 'and'),
    ('left', 'equal', 'neq'),
    ('left', 'less', 'greater', 'leq', 'geq'),
    ('left', 'add', 'sub'),
    ('left', 'mul', 'div'),
    ('left', 'assign')
)


def p_program(p):
    'PROGRAM : IMPORT_STATE PERMISSION class id lc DEFINE_LIST rc'
    p[0] = ASTNode('PROGRAM', [p[1], p[2], p[4], p[6]])


def p_import_state(p):
    '''IMPORT_STATE : empty
                    | import java dot BUILT_IN_PACKAGE dot BUILT_IN_CLASS semi'''
    if len(p) > 2:
        p[0] = ASTNode('IMPORT_STATE', [p[2], p[4], p[6]])


def p_built_in_package(p):
    '''BUILT_IN_PACKAGE : util'''
    p[0] = ASTNode('BUILT_IN_PACKAGE', [p[1]])


def p_non_primitive_built_in_class(p):
    '''BUILT_IN_CLASS : Stack
                      | Scanner'''
    p[0] = ASTNode("BUILT_IN_CLASS", [p[1]])


def p_permission(p):
    '''PERMISSION : private
                  | protected
                  | public'''
    p[0] = ASTNode('PERMISSION', [p[1]])


def p_define_list(p):
    '''DEFINE_LIST : VAR_DEFINE DEFINE_LIST
                   | FUNC_DEFINE DEFINE_LIST
                   | ARRAY_DEFINE DEFINE_LIST
                   | empty'''
    if len(p) == 3:
        children = [p[1]]
        if p[2].children[0] is not None:
            children += p[2].children[:]
    else:
        children = [None]
    p[0] = ASTNode('DEFINE_LIST', children)


def p_var_define(p):
    'VAR_DEFINE : TYPE id assign EXP semi'
    p[0] = ASTNode('VAR_DEFINE', [p[1], p[2], p[4]])


def p_array_define(p):
    'ARRAY_DEFINE : TYPE_BEGIN lb rb id assign new TYPE_BEGIN lb EXP rb semi'
    p[0] = ASTNode('ARRAY_DEFINE', [p[1], p[4], p[7], p[9]])


def p_func_define(p):
    'FUNC_DEFINE : PERMISSION STATIC TYPE id lp PARAMS rp BLOCK'
    p[0] = ASTNode('FUNC_DEFINE', [p[1], p[2], p[3], p[4], p[6], p[8]])


def p_type(p):
    'TYPE : TYPE_BEGIN TYPE_FOLLOW'
    t = p[1].children[0]
    f = p[2].children[0]
    if f is not None:
        t = t + f
    p[0] = ASTNode('TYPE', [t])


def p_type_begin(p):
    '''TYPE_BEGIN : boolean
                  | char
                  | int
                  | string
                  | void
                  | object
                  | float'''
    p[0] = ASTNode('TYPE_BEGIN', [p[1]])


def p_type_follow(p):
    '''TYPE_FOLLOW : lb rb
                   | empty'''
    if len(p) == 3:
        children = [p[1] + p[2]]
    else:
        children = [None]
    p[0] = ASTNode('TYPE_FOLLOW', children)


def p_exp(p):
    '''EXP : EXP BIN_OP EXP
           | UN_OP EXP
           | TERM'''
    p[0] = ASTNode('EXP', p[1:])


def p_term(p):
    '''TERM : lp EXP rp
            | id ID_FOLLOW
            | chr
            | str
            | integer
            | neginteger
            | null
            | true
            | false '''
    p[0] = ASTNode('TERM', p[1:] if len(p) < 4 else [p[2]])


def p_binop(p):
    '''BIN_OP : add
              | sub
              | mul
              | div
              | and
              | or
              | equal
              | neq
              | less
              | greater
              | leq
              | geq'''
    p[0] = ASTNode('BIN_OP', p[1:])


def p_unop(p):
    '''UN_OP : inc
             | not'''
    p[0] = ASTNode('UN_OP', p[1:])


def p_id_follow_call(p):
    'ID_FOLLOW : lp ARGS rp'
    p[0] = ASTNode('ID_FOLLOW_CALL', p[2].children[:])


def p_id_follow_dot(p):
    'ID_FOLLOW : dot id ID_FOLLOW'
    p[0] = ASTNode('ID_FOLLOW_DOT', p[2:])


def p_id_index(p):
    'ID_FOLLOW : lb EXP rb'
    p[0] = ASTNode('ID_FOLLOW_INDEX', [p[2]])


def p_id_follow_empty(p):
    'ID_FOLLOW : empty'
    p[0] = ASTNode('ID_FOLLOW_EMPTY', None)


def p_static(p):
    '''STATIC : static
              | empty'''
    p[0] = ASTNode('STATIC', p[1:])


def p_params(p):
    '''PARAMS : PARAM_LIST
              | empty'''
    children = p[1].children[:] if p[1] is not None else None
    p[0] = ASTNode('PARAMS', children)


def p_param_list(p):
    'PARAM_LIST : PARAM PARAM_FOLLOW'
    children = [p[1]]
    if p[2].children[0] is not None:
        children += p[2].children[:]
    p[0] = ASTNode('PARAM_LIST', children)


def p_param(p):
    'PARAM : TYPE id'
    p[0] = ASTNode('PARAM', p[1:])


def p_param_follow(p):
    '''PARAM_FOLLOW : comma PARAM PARAM_FOLLOW
                    | empty'''
    if len(p) == 4:
        children = [p[2]]
        if p[3].children[0] is not None:
            children += p[3].children[:]
    else:
        children = [None]
    p[0] = ASTNode('PARAM_FOLLOW', children)


def p_block(p):
    'BLOCK : lc LOCAL_DEFINE_LIST CODE_LIST rc'
    children = []
    if p[2].children[0] is not None:
        children += [p[2]]
    if p[3].children[0] is not None:
        children += [p[3]]
    if len(children) == 0:
        children = None
    p[0] = ASTNode('BLOCK', children)


def p_local_define_list(p):
    '''LOCAL_DEFINE_LIST : LOCAL_VAR_DEFINE LOCAL_DEFINE_LIST
                         | LOCAL_ARRAY_DEFINE LOCAL_DEFINE_LIST
                         | LOCAL_VAR_DEFINE_WITH_CONSTRUCTOR LOCAL_DEFINE_LIST
                         | empty'''
    if len(p) > 2:
        children = [p[1]]
        if p[2].children[0] is not None:
            children += p[2].children[:]
    else:
        children = [None]
    p[0] = ASTNode('LOCAL_DEFINE_LIST', children)


def p_local_var_define(p):
    '''LOCAL_VAR_DEFINE : TYPE id assign EXP semi'''
    p[0] = ASTNode('LOCAL_VAR_DEFINE', p[1:3] + [p[4]])


def p_local_var_define_with_constructor(p):
    '''LOCAL_VAR_DEFINE_WITH_CONSTRUCTOR : BUILT_IN_CLASS id assign new BUILT_IN_CLASS lp ARGS rp semi'''
    if len(p) > 2:
        p[0] = ASTNode('LOCAL_VAR_DEFINE_WITH_CONSTRUCTOR', p[1:3] + p[5:])


def p_local_array_define(p):
    'LOCAL_ARRAY_DEFINE : TYPE_BEGIN lb rb id assign new TYPE_BEGIN lb EXP rb semi'
    p[0] = ASTNode('LOCAL_ARRAY_DEFINE', [p[1], p[4], p[7], p[9]])


def p_code_list(p):
    '''CODE_LIST : CODE CODE_LIST
                 | empty'''
    if len(p) == 3:
        children = [p[1]]
        if p[2].children[0] is not None:
            children += p[2].children[:]
    else:
        children = [None]
    p[0] = ASTNode('CODE_LIST', children)


def p_code(p):
    '''CODE : NORMAL_STATE semi
            | SELECT_STATE
            | LOOP_STATE
            | RETURN_STATE semi'''
    p[0] = ASTNode('CODE', p[1:])


def p_normal_state_assign(p):
    'NORMAL_STATE : id ID_FOLLOW assign EXP'
    p[0] = ASTNode('NORMAL_STATE_ASSIGN', [p[1], p[2], p[4]])


def p_normal_state_call(p):
    'NORMAL_STATE : id ID_FOLLOW'
    p[0] = ASTNode('NORMAL_STATE_CALL', [p[1], p[2]])


def p_normal_state_control(p):
    '''NORMAL_STATE : break
                    | continue'''
    p[0] = ASTNode('NORMAL_STATE_CONTROL', p[1:])


def p_select_state(p):
    'SELECT_STATE : if lp EXP rp lc CODE_LIST rc SELECT_FOLLOW'
    p[0] = ASTNode('SELECT_STATE', [p[3], p[6], p[8]])


def p_select_follow(p):
    '''SELECT_FOLLOW : else lc CODE_LIST rc
                     | empty'''
    p[0] = ASTNode('SELECT_FOLLOW', [p[3]] if len(p) > 2 else p[1:])


def p_loop_state(p):
    '''LOOP_STATE : FOR_LOOP
                  | WHILE_LOOP'''
    p[0] = ASTNode('LOOP_STATE', p[1:])


def p_for_loop(p):
    'FOR_LOOP : for lp NORMAL_STATE semi EXP semi NORMAL_STATE rp lc CODE_LIST rc'
    p[0] = ASTNode('FOR_LOOP', [p[3], p[5], p[7], p[10]])


def p_while_loop(p):
    'WHILE_LOOP : while lp EXP rp lc CODE_LIST rc'
    p[0] = ASTNode('WHILE_LOOP', [p[3], p[6]])


def p_return_state(p):
    'RETURN_STATE : return RETURN_FOLLOW'
    p[0] = ASTNode('RETURN_STATE', p[2].children[:])


def p_return_follow(p):
    '''RETURN_FOLLOW : EXP
                     | empty'''
    children = p[1:] if p[1] is not None else []
    p[0] = ASTNode('RETURN_FOLLOW', children)


def p_args(p):
    '''ARGS : ARG_LIST
            | empty'''
    children = p[1].children[:] if p[1] is not None else []
    p[0] = ASTNode('ARGS', children)


def p_arg_list(p):
    'ARG_LIST : EXP ARG_FOLLOW'
    children = [p[1]]
    if p[2].children[0] is not None:
        children += p[2].children[:]
    p[0] = ASTNode('ARG_LIST', children)


def p_arg_follow(p):
    '''ARG_FOLLOW : comma EXP ARG_FOLLOW
                  | empty'''
    if len(p) == 4:
        children = [p[2]]
        if p[3].children[0] is not None:
            children += p[3].children[:]
    else:
        children = [None]
    p[0] = ASTNode('ARG_FOLLOW', children)


def p_empty(p):
    'empty :'
    p[0] = None


def p_error(p):
    print('Syntax error! {}'.format(p))


parser = yacc.yacc(debug=True)
