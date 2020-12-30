from tool.runners.python import SubmissionPy

class Tokenizer(object):
    def __init__(self, src):
        self.src = src
        self.i = 0
    
    def advance(self):
        self.i += 1
        return self.src[self.i - 1]
    
    def peek(self):
        if self.i == len(self.src):
            return None
        return self.src[self.i]
    
    def next_token(self):
        while (c := self.peek()) == ' ':
            self.advance()
        if c is None:
            return None
        return self.advance()

class Parser(object):
    def __init__(self, src):
        self.tokenizer = Tokenizer(src)
        self.cur = None
        self.advance()
    
    def peek(self):
        return self.cur
    
    def advance(self):
        self.cur = self.tokenizer.next_token()

    def match(self, token):
        if self.peek() != token:
            return False
        self.advance()
        return True
    
    def expr(self):
        n = self.term()
        while self.peek() in ['+', '*']:
            if self.match('+'):
                n += self.term()
            elif self.match('*'):
                n *= self.term()
        return n

    def term(self):
        if self.match('('):
            n = self.expr()
            self.match(')')
            return n
        elif c := self.peek():
            self.advance()
            return int(c)
    
    def evaluate(self):
        return self.expr()

class EvqnaSubmission(SubmissionPy):
    def evaluate(self, expr):
        parser = Parser(expr)
        return parser.evaluate()

    def run(self, s):
        return sum([self.evaluate(expr) for expr in s.splitlines()])
