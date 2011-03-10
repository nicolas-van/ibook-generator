# Begin -- grammar generated by Yapps
import sys, re
from yapps import runtime

class FireWolfParserScanner(runtime.Scanner):
    patterns = [
        ('"}"', re.compile('}')),
        ('"{"', re.compile('{')),
        ('","', re.compile(',')),
        ('"\\\\]"', re.compile('\\]')),
        ('"\\\\["', re.compile('\\[')),
        ('"\\\\)"', re.compile('\\)')),
        ('"\\\\("', re.compile('\\(')),
        ('":"', re.compile(':')),
        ('"\\\\?"', re.compile('\\?')),
        ('"end"', re.compile('end')),
        ('"else"', re.compile('else')),
        ('"elseif"', re.compile('elseif')),
        ('"then"', re.compile('then')),
        ('"if"', re.compile('if')),
        ('"$"', re.compile('$')),
        ('\\s+', re.compile('\\s+')),
        ('#.*?\n', re.compile('#.*?\n')),
        ('/.*?\n', re.compile('/.*?\n')),
        ('/\\*.*?\\*/', re.compile('/\\*.*?\\*/')),
        ('identifier', re.compile('[a-zA-Z_][a-zA-Z0-9_]*')),
        ('boolean_litteral', re.compile('true|false')),
        ('float_litteral', re.compile('[0-9]+\\.[0-9]*')),
        ('integer_litteral', re.compile('[0-9]+')),
        ('string_litteral', re.compile('("[^"\n]*(\\"[^"\n]*)*")|(\'[^\'\n]*(\\\'[^\'\n]*)*\')')),
        ('null_litteral', re.compile('null')),
        ('assignment', re.compile('=|\\+=|-=|\\*=|/=|%=')),
        ('logical_or', re.compile('or')),
        ('logical_and', re.compile('and')),
        ('equality', re.compile('==|!=')),
        ('relational', re.compile('<|>|<=|>=')),
        ('additive', re.compile('\\+|-')),
        ('mult', re.compile('\\*|/|%')),
        ('non', re.compile('not')),
    ]
    def __init__(self, str,*args,**kw):
        runtime.Scanner.__init__(self,None,{'#.*?\n':None,'/\\*.*?\\*/':None,'\\s+':None,'/.*?\n':None,},str,*args,**kw)

class FireWolfParser(runtime.Parser):
    Context = runtime.Context
    def litteral(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'litteral', [])
        _token = self._peek('boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', context=_context)
        if _token == 'boolean_litteral':
            boolean_litteral = self._scan('boolean_litteral', context=_context)
            return boolean_litteral == "true"
        elif _token == 'string_litteral':
            string_litteral = self._scan('string_litteral', context=_context)
            return eval(string_litteral)
        elif _token == 'integer_litteral':
            integer_litteral = self._scan('integer_litteral', context=_context)
            return int(integer_litteral)
        elif _token == 'float_litteral':
            float_litteral = self._scan('float_litteral', context=_context)
            return float(float_litteral)
        else: # == 'null_litteral'
            null_litteral = self._scan('null_litteral', context=_context)
            return None

    def program(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'program', [])
        block = self.block(_context)
        self._scan('"$"', context=_context)
        return block

    def block(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'block', [])
        lst = []
        while self._peek('"$"', '"if"', '"elseif"', '"else"', '"end"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) not in ['"$"', '"elseif"', '"else"', '"end"']:
            statement = self.statement(_context)
            lst.append(statement)
        return lst

    def statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'statement', [])
        _token = self._peek('"if"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context)
        if _token != '"if"':
            assignment_expr = self.assignment_expr(_context)
            return assignment_expr
        else: # == '"if"'
            if_statement = self.if_statement(_context)
            return if_statement

    def if_statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'if_statement', [])
        self._scan('"if"', context=_context)
        expression = self.expression(_context)
        self._scan('"then"', context=_context)
        block = self.block(_context)
        while self._peek('"else"', '"elseif"', '"$"', '"end"', context=_context) == '"elseif"':
            self._scan('"elseif"', context=_context)
            expression = self.expression(_context)
            self._scan('"then"', context=_context)
            block = self.block(_context)
        if self._peek('"else"', '"end"', '"$"', '"elseif"', context=_context) == '"else"':
            self._scan('"else"', context=_context)
            block = self.block(_context)
        self._scan('"end"', context=_context)

    def assignment_expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'assignment_expr', [])
        expression = self.expression(_context)
        res = expression;first=True
        while self._peek('assignment', '"if"', '"$"', '"elseif"', '"else"', '"end"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) == 'assignment':
            assignment = self._scan('assignment', context=_context)
            expression = self.expression(_context)
            if first: res = ["=", res];res += [assignment, expression]
        return res

    def expression(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'expression', [])
        cond_expr = self.cond_expr(_context)
        return cond_expr

    def cond_expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'cond_expr', [])
        logical_or_expr = self.logical_or_expr(_context)
        res = logical_or_expr
        if self._peek('"\\\\?"', '"then"', '"\\\\)"', '"\\\\]"', '","', '":"', 'assignment', '"}"', '"if"', '"$"', '"elseif"', '"else"', '"end"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) == '"\\\\?"':
            self._scan('"\\\\?"', context=_context)
            expression = self.expression(_context)
            res = ["?", res, expression]
            self._scan('":"', context=_context)
            expression = self.expression(_context)
            res.append(expression)
        return res

    def logical_or_expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'logical_or_expr', [])
        logical_and_expr = self.logical_and_expr(_context)
        res = logical_and_expr
        while self._peek('logical_or', '"\\\\?"', '"then"', '"\\\\)"', '"\\\\]"', '","', '":"', 'assignment', '"}"', '"if"', '"$"', '"elseif"', '"else"', '"end"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) == 'logical_or':
            logical_or = self._scan('logical_or', context=_context)
            logical_and_expr = self.logical_and_expr(_context)
            res = [logical_or, res, logical_and_expr]
        return res

    def logical_and_expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'logical_and_expr', [])
        equality_expr = self.equality_expr(_context)
        res = equality_expr
        while self._peek('logical_and', 'logical_or', '"\\\\?"', '"then"', '"\\\\)"', '"\\\\]"', '","', '":"', 'assignment', '"}"', '"if"', '"$"', '"elseif"', '"else"', '"end"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) == 'logical_and':
            logical_and = self._scan('logical_and', context=_context)
            equality_expr = self.equality_expr(_context)
            res = [logical_and, res, equality_expr]
        return res

    def equality_expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'equality_expr', [])
        relational_expr = self.relational_expr(_context)
        res = relational_expr
        while self._peek('equality', 'logical_and', 'logical_or', '"\\\\?"', '"then"', '"\\\\)"', '"\\\\]"', '","', '":"', 'assignment', '"}"', '"if"', '"$"', '"elseif"', '"else"', '"end"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) == 'equality':
            equality = self._scan('equality', context=_context)
            relational_expr = self.relational_expr(_context)
            res = [equality, res, relational_expr]
        return res

    def relational_expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'relational_expr', [])
        additive_expr = self.additive_expr(_context)
        res = additive_expr
        while self._peek('relational', 'equality', 'logical_and', 'logical_or', '"\\\\?"', '"then"', '"\\\\)"', '"\\\\]"', '","', '":"', 'assignment', '"}"', '"if"', '"$"', '"elseif"', '"else"', '"end"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) == 'relational':
            relational = self._scan('relational', context=_context)
            additive_expr = self.additive_expr(_context)
            res = [relational, res, additive_expr]
        return res

    def additive_expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'additive_expr', [])
        mult_expr = self.mult_expr(_context)
        res = mult_expr
        while self._peek('additive', 'relational', 'equality', 'logical_and', 'logical_or', '"\\\\?"', '"then"', '"\\\\)"', '"\\\\]"', '","', '":"', 'assignment', '"}"', '"if"', '"$"', '"elseif"', '"else"', '"end"', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) == 'additive':
            additive = self._scan('additive', context=_context)
            mult_expr = self.mult_expr(_context)
            res = [additive, res, mult_expr]
        return res

    def mult_expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'mult_expr', [])
        unary_expr = self.unary_expr(_context)
        res = unary_expr
        while self._peek( context=_context) == 'mult':
            mult = self._scan('mult', context=_context)
            unary_expr = self.unary_expr(_context)
            res = [mult, res, unary_expr]
        return res

    def unary_expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'unary_expr', [])
        _token = self._peek('additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context)
        if _token in ['additive', 'non']:
            tmp = None
            _token = self._peek('additive', 'non', context=_context)
            if _token == 'additive':
                additive = self._scan('additive', context=_context)
                tmp = additive
            else: # == 'non'
                non = self._scan('non', context=_context)
                tmp=non
            unary_expr = self.unary_expr(_context)
            return [tmp, unary_expr] if tmp is not None else unary_expr
        else:
            postfix_expr = self.postfix_expr(_context)
            return postfix_expr

    def postfix_expr(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'postfix_expr', [])
        _token = self._peek('"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context)
        if _token != '"\\\\("':
            rvalue = self.rvalue(_context)
            while self._peek( context=_context) in ['"\\\\["', '"\\\\("']:
                _token = self._peek('"\\\\["', '"\\\\("', context=_context)
                if _token == '"\\\\["':
                    table_acc = self.table_acc(_context)
                else: # == '"\\\\("'
                    function_call = self.function_call(_context)
            return rvalue
        else: # == '"\\\\("'
            self._scan('"\\\\("', context=_context)
            expression = self.expression(_context)
            self._scan('"\\\\)"', context=_context)
            return expression

    def table_acc(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'table_acc', [])
        self._scan('"\\\\["', context=_context)
        expression = self.expression(_context)
        self._scan('"\\\\]"', context=_context)

    def function_call(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'function_call', [])
        self._scan('"\\\\("', context=_context)
        if self._peek('"\\\\)"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) != '"\\\\)"':
            expression = self.expression(_context)
            while self._peek('","', '"then"', '"\\\\)"', '"\\\\]"', '":"', 'assignment', '"}"', '"if"', '"$"', '"elseif"', '"else"', '"end"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) == '","':
                self._scan('","', context=_context)
                expression = self.expression(_context)
            if self._peek('","', '"\\\\)"', context=_context) == '","':
                self._scan('","', context=_context)
        self._scan('"\\\\)"', context=_context)

    def rvalue(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'rvalue', [])
        _token = self._peek('boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context)
        if _token not in ['identifier', '"\\\\["', '"{"']:
            litteral = self.litteral(_context)
            return ('litteral',litteral)
        elif _token == 'identifier':
            identifier = self._scan('identifier', context=_context)
            return ('identifier',identifier)
        elif _token == '"\\\\["':
            list = self.list(_context)
            return ('list',list)
        else: # == '"{"'
            dictionary = self.dictionary(_context)
            return ('dictionary',dictionary)

    def list(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'list', [])
        self._scan('"\\\\["', context=_context)
        if self._peek('"\\\\]"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) != '"\\\\]"':
            expression = self.expression(_context)
            while self._peek('","', '"then"', '"\\\\)"', '"\\\\]"', '":"', 'assignment', '"}"', '"if"', '"$"', '"elseif"', '"else"', '"end"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) == '","':
                self._scan('","', context=_context)
                expression = self.expression(_context)
            if self._peek('","', '"\\\\]"', context=_context) == '","':
                self._scan('","', context=_context)
        self._scan('"\\\\]"', context=_context)

    def dictionary(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'dictionary', [])
        self._scan('"{"', context=_context)
        if self._peek('"}"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) != '"}"':
            expression = self.expression(_context)
            self._scan('":"', context=_context)
            expression = self.expression(_context)
            while self._peek('","', '"then"', '"\\\\)"', '"\\\\]"', '":"', 'assignment', '"}"', '"if"', '"$"', '"elseif"', '"else"', '"end"', 'additive', 'non', '"\\\\("', 'boolean_litteral', 'string_litteral', 'integer_litteral', 'float_litteral', 'null_litteral', 'identifier', '"\\\\["', '"{"', context=_context) == '","':
                self._scan('","', context=_context)
                expression = self.expression(_context)
                self._scan('":"', context=_context)
                expression = self.expression(_context)
            if self._peek('","', '"}"', context=_context) == '","':
                self._scan('","', context=_context)
        self._scan('"}"', context=_context)


def parse(rule, text):
    P = FireWolfParser(FireWolfParserScanner(text))
    return runtime.wrap_error_reporter(P, rule)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print parse(argv[1], f.read())
    else: print >>sys.stderr, 'Args:  <rule> [<filename>]'
# End -- grammar generated by Yapps
