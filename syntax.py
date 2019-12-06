import ply.yacc as yacc

from lexical import tokens


class ASTNode:
    def __init__(self, type_, children=None):
        if children is None:
            children = []
        self.type = type_
        self.children = children


start = 'PROGRAM'


def p_program(p):
    'PROGRAM : CLASS_CONTAINER'
    p[0] = ASTNode('PROGRAM', [p[1]])


def p_class_container(p):
    'CLASS_CONTAINER : PERMISSION class id lc DEFINE_LIST rc'
    p[0] = ASTNode('CLASS_CONTAINER', [p[1], p[3], p[5]])


def p_permission(p):
    '''PERMISSION : private
                  | protected
                  | public'''
    p[0] = ASTNode('PERMISSION', [p[1]])


def p_define_list(p):
    '''DEFINE_LIST : VAR_DEFINE
                   | FUNC_DEFINE'''
    p[0] = ASTNode('DEFINE_LIST', p[1])


def p_var_define(p):
    'VAR_DEFINE : TYPE id assign EXP semi'
    p[0] = ASTNode('VAR_DEFINE', [p[1], p[2], p[4]])


def p_func_define(p):
    'FUNC_DEFINE : PERMISSION STATIC TYPE id lp PARAMS rp BLOCK'
    p[0] = ASTNode('FUNC_DEFINE', [p[1], p[2], p[3], p[4], p[6], p[8]])


def p_type(p):
    'TYPE : TYPE_BEGIN TYPE_FOLLOW'
    p[0] = ASTNode('TYPE', p[1:])


def p_type_begin(p):
    '''TYPE_BEGIN : boolean
                  | char
                  | int
                  | string
                  | void'''
    p[0] = ASTNode('TYPE', [p[1]])


def p_type_follow(p):
    '''TYPE_FOLLOW : lb rb
                   | empty'''
    p[0] = ASTNode('TYPE_FOLLOW', p[1:])


def p_exp(p):
    'EXP : COMPUTE_EXP RELATION_EXP'
    p[0] = ASTNode('EXP', p[1:])


def p_compute_exp(p):
    'COMPUTE_EXP : TERM TERM_FOLLOW'
    p[0] = ASTNode('COMPUTE_EXP', p[1:])

def p_term_follow(p):
    '''TERM_FOLLOW : BIN_OP EXP
                   | empty'''
    p[0] = ASTNode('TERM_FOLLOW', p[1:])

def p_relation_exp(p):
    '''RELATION_EXP : REL_OP COMPUTE_EXP
                    | empty'''
    p[0] = ASTNode('RELATION_EXP', p[1:])


def p_term(p):
    '''TERM : lp EXP rp
            | id ID_FOLLOW
            | chr
            | str
            | integer
            | null
            | true
            | false'''
    p[0] = ASTNode('TERM', p[1:] if len(p) < 3 else [p[2]])


def p_bin_op(p):
    '''BIN_OP : add
              | sub
              | mul
              | div
              | and
              | or
              | assign
              | addassign
              | subassign
              | mulassign
              | divassign'''
    p[0] = ASTNode('BIN_OP', p[1:])


def p_rel_op(p):
    '''REL_OP : equal
              | neq
              | less
              | greater
              | leq
              | geq'''
    p[0] = ASTNode('REL_OP', p[1:])


def p_id_follow(p):
    '''ID_FOLLOW : lp ARGS rp
                 | dot ATTRIBUTE
                 | lb integer rb
                 | empty'''
    p[0] = ASTNode('ID_FOLLOW', p[1:])

def p_attribute(p):
    '''ATTRIBUTE : id ID_FOLLOW
                 | empty'''
    p[0] = ASTNode('ATTRIBUTE', p[1:])


def p_static(p):
    '''STATIC : static
              | empty'''
    p[0] = ASTNode('STATIC', p[1:])


def p_params(p):
    '''PARAMS : PARAM_LIST
              | empty'''
    p[0] = ASTNode('PARAMS', p[1:])


def p_param_list(p):
    'PARAM_LIST : PARAM PARAM_FOLLOW'
    p[0] = ASTNode('PARAM_LIST', p[1:])


def p_param(p):
    'PARAM : TYPE id'
    p[0] = ASTNode('PARAM', p[1:])


def p_param_follow(p):
    '''PARAM_FOLLOW : comma PARAM PARAM_FOLLOW
                    | empty'''
    p[0] = ASTNode('PARAM_FOLLOW', p[1:])


def p_block(p):
    'BLOCK : lc LOCAL_DEFINE_LIST CODE_LIST rc'
    p[0] = ASTNode('BLOCK', p[2:4])


def p_local_define_list(p):
    '''LOCAL_DEFINE_LIST : LOCAL_VAR_DEFINE LOCAL_DEFINE_LIST
                         | empty'''
    p[0] = ASTNode('LOCAL_DEFINE_LIST', p[1:])


def p_local_var_define(p):
    'LOCAL_VAR_DEFINE : TYPE id assign EXP semi'
    p[0] = ASTNode('LOCAL_VAR_DEFINE', p[1:3])


def p_code_list(p):
    '''CODE_LIST : CODE CODE_LIST
                 | empty'''
    p[0] = ASTNode('CODE_LIST', p[1:])


def p_code(p):
    '''CODE : NORMAL_STATE
            | SELECT_STATE
            | LOOP_STATE
            | RETURN_STATE'''
    p[0] = ASTNode('CODE', p[1:])


def p_normal_state_assign(p):
    'NORMAL_STATE : id ID_FOLLOW assign EXP semi'
    p[0] = ASTNode('NORMAL_STATE_ASSIGN', [p[1], p[3]])


def p_normal_state_call(p):
    'NORMAL_STATE : id ID_FOLLOW semi'
    p[0] = ASTNode('NORMAL_STATE_CALL', [p[1], p[3]])


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
    'FOR_LOOP : for lp EXP semi EXP semi EXP rp lc CODE_LIST rc'
    p[0] = ASTNode('FOR_LOOP', [p[3], p[5], p[7], p[10]])


def p_while_loop(p):
    'WHILE_LOOP : while lp EXP rp lc CODE_LIST rc'
    p[0] = ASTNode('WHILE_LOOP', [p[3], p[6]])


def p_return_state(p):
    'RETURN_STATE : return RETURN_FOLLOW semi'
    p[0] = ASTNode('RETURN_STATE', [p[2]])


def p_return_follow(p):
    '''RETURN_FOLLOW : EXP
                     | empty'''
    p[0] = ASTNode('RETURN FOLLOW', p[1:])


def p_args(p):
    '''ARGS : ARG_LIST
            | empty'''
    p[0] = ASTNode('ARGS', p[1:])


def p_arg_list(p):
    'ARG_LIST : EXP ARG_FOLLOW'
    p[0] = ASTNode('ARG_LIST', p[1:])


def p_arg_follow(p):
    '''ARG_FOLLOW : comma id ID_FOLLOW ARG_FOLLOW
                  | empty'''
    p[0] = ASTNode('ARG_FOLLOW', p[2:] if len(p) > 2 else p[1:])


def p_empty(p):
    'empty :'
    p[0] = None


def p_error(p):
    print('Syntax error!')


precedence = (
    ('left', 'assign'),
    ('left', 'or'),
    ('left', 'and'),
    ('left', 'equal', 'neq'),
    ('left', 'less', 'greater', 'leq', 'geq'),
    ('left', 'add', 'sub'),
    ('left', 'mul', 'div')
)

parser = yacc.yacc(debug=True)
