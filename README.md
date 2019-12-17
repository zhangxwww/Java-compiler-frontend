start = 'PROGRAM'

PROGRAM : PERMISSION class id lc DEFINE_LIST rc

PERMISSION : private
            | protected
            | public

DEFINE_LIST: VAR_DEFINE DEFINE_LIST
            | FUNC_DEFINE DEFINE_LIST
            | empty

VAR_DEFINE : TYPE id assign **EXP** semi

FUNC_DEFINE : PERMISSION STATIC TYPE id '(' PARAMS ')' BLOCK **这里的id改成id ID_FOLLOW**

TYPE : TYPE_BEGIN TYPE_FOLLOW

TYPE_BEGIN : boolean
            | char
            | int
            | string
            | void

TYPE_FOLLOW : '[' ']'
             | empty

PARAMS : PARAM_LIST
        | empty

PARAM_LIST : PARAM PARAM_FOLLOW

PARAM : TYPE id

PARAM_FOLLOW : comma PARAM PARAM_FOLLOW
              | empty

NORMAL_STATE_WITHOUT_SEMI : id ID_FOLLOW assign EXP
              | id ID_FOLLOW
              | empty

CONTROL_STATE : continue semi
               | break semi
              

SELECT_STATE : if lp EXP rp lc CODE_LIST rc SELECT_FOLLOW

SELECT_FOLLOW : else lc CODE_LIST rc
               | empty



BIN_OP : add
        | sub
        | mul
        | div
        | and
        | or
        | assign

LOOP_STATE : FOR_LOOP
            | WHILE_LOOP

FOR_LOOP : for lp NORMAL_STATE_WITHOUT_SEMI semi exp semi NORMAL_STATE_WITHOUT_SEMI rp lc BLOCK rc

WHILE_LOOP : while lp EXP rp lc BLOCK rc

RETURN_STATE: return RETURN_FOLLOW semi

RETURN_FOLLOW : EXP
               | empty

```
1.感觉与COMPUTE_EXP、RELATION_EXP相关的产生式规则都不太好，可以试着统一一下计算和关系比较，然后支持一下precedence:
下面的production rule不确定是对的。。再斟酌下
EXP: EXP BIN_OP EXP
    | (EXP)
    | id ID_FOLLOW
    | integer

2. BLOCK的产生式规则改一下 :
FUNC_DEFINE : PERMISSION STATIC TYPE id lp PARAMS rp lc BLOCK rc
BLOCK : LOCAL_VAR_DEFINE BLOCK
       | NORMAL_STATE_WITHOUT_SEMI semi BLOCK
       | SELECT_STATE BLOCK
       | LOOP_STATE BLOCK
       | RETURN_STATE BLOCK
       | CONTROL_STATE BLOCK
       | empty
3. 增加一下对import的支持
```

