
parser FireWolfParser:

ignore: "\\s+"
ignore: "#.*?\n"
ignore: "/.*?\n"
ignore: "/\*.*?\*/"
token identifier: "[a-zA-Z_][a-zA-Z0-9_]*"
token boolean_litteral: "true|false"
token float_litteral: "[0-9]+\.[0-9]*"
token integer_litteral: "[0-9]+"
token string_litteral: "(\"[^\"\n]*(\\\"[^\"\n]*)*\")|('[^'\n]*(\\'[^'\n]*)*')"
token null_litteral: "null"

token assignment: "=|\\+=|-=|\\*=|/=|%="
token logical_or: "or"
token logical_and: "and"
token equality: "==|!="
token relational: "<|>|<=|>="
token additive: "\\+|-"
token mult: "\\*|/|%"
token non: "not"

rule litteral: boolean_litteral {{ return boolean_litteral == "true" }} |
    string_litteral {{ return eval(string_litteral) }} |
    integer_litteral {{ return int(integer_litteral) }} |
    float_litteral {{ return float(float_litteral) }} |
    null_litteral {{ return None }}

rule program: block "$" {{ return block }}
rule block: {{ lst = [] }} (statement {{ lst.append(statement) }}) * {{ return lst }}
rule statement : assignment_expr {{ return assignment_expr }} | 
    if_statement {{ return if_statement }}

rule if_statement : "if" expression "then" block ("elseif" expression "then" block)* ["else" block] "end"
rule assignment_expr :  expression {{res = expression;first=True}}
    (assignment expression {{if first: res = ["=", res];res += [assignment, expression]}})* {{return res}}

rule expression : cond_expr {{return cond_expr}}
rule cond_expr : logical_or_expr {{res = logical_or_expr}} ["\\?" expression {{res = ["?", res, expression]}}
    ":" expression {{res.append(expression)}}] {{return res}}
rule logical_or_expr : logical_and_expr {{res = logical_and_expr}}
    (logical_or logical_and_expr {{res = [logical_or, res, logical_and_expr]}})* {{return res}}
rule logical_and_expr : equality_expr {{res = equality_expr}}
    (logical_and equality_expr {{res = [logical_and, res, equality_expr]}})* {{return res}}
rule equality_expr : relational_expr {{res = relational_expr}}
    (equality relational_expr {{res = [equality, res, relational_expr]}})* {{return res}}
rule relational_expr : additive_expr {{res = additive_expr}} 
    (relational additive_expr {{res = [relational, res, additive_expr]}})* {{return res}}
rule additive_expr : mult_expr {{res = mult_expr}}
    (additive mult_expr {{res = [additive, res, mult_expr]}})* {{return res}}
rule mult_expr : unary_expr {{res = unary_expr}}
    (mult unary_expr {{res = [mult, res, unary_expr]}})* {{return res}}
rule unary_expr : {{tmp = None}}(additive {{tmp = additive}} | non {{tmp=non}})
    unary_expr {{return [tmp, unary_expr] if tmp is not None else unary_expr}} | postfix_expr {{return postfix_expr}}
rule postfix_expr : rvalue (table_acc | function_call)* {{return rvalue}} | "\\(" expression "\\)" {{return expression}}
rule table_acc : "\\[" expression "\\]"
rule function_call : "\\(" [(expression ("," expression)* [","] )] "\\)"
rule rvalue : litteral {{return ('litteral',litteral)}}| identifier {{return ('identifier',identifier)}}
    | list {{return ('list',list)}}| dictionary {{return ('dictionary',dictionary)}}
rule list : "\\[" [( expression ( "," expression  )* [","]  )]  "\\]"
rule dictionary : "{" [( expression ":" expression ( "," expression ":" expression )* [","] )] "}"


 

