import re

# We keep these for post-processing identifiers
KEYWORDS = {'class', 'constructor', 'function', 'method', 'field', 'static', 
            'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 
            'this', 'let', 'do', 'if', 'else', 'while', 'return'}
SYMBOLS = r'{}()\[\].,;+\-*/&|<>=~'

# Token specification
TOKEN_SPEC = [
    ('INT_CONST', r'\d+'),
    ('STRING_CONST',  r'"[^"]*"'), # A quote, followed by anything but a quote, then a closing quote
    ('IDENTIFIER',    r'[a-zA-Z_]\w*'),
    ('SYMBOL',        f'[{re.escape(SYMBOLS)}]'), # Match any single character from our symbols string
    ('SKIP',          r'\s+'),           # Skip one or more whitespace characters
    ('MISMATCH',      r'.'),              # Any other character is a mismatch/error
]

# Master regex that matches any of the patterns
TOKEN_REGEX = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC))



class JackTokenizer:
    def __init__(self, filepath: str):
        with open(filepath, 'r') as f:
            code = f.read()

        # Remove comments first
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        self.code = re.sub(r'//.*', '', code)

    def tokenize(self):
        """Yields (token_type, token_value) tuples."""
        
        for match in TOKEN_REGEX.finditer(self.code):
            token_type = match.lastgroup  # The name of the group that matched
            token_value = match.group()

            if token_type == 'SKIP':
                continue
            elif token_type == 'MISMATCH':
                raise RuntimeError(f"Unexpected character: {token_value}")
            
            # Post-processing steps
            if token_type == 'STRING_CONST':
                # As per spec, strip the quotes
                token_value = token_value[1:-1]
            elif token_type == 'IDENTIFIER' and token_value in KEYWORDS:
                # If an identifier is a keyword, change its type
                token_type = 'KEYWORD'
                
            yield token_type, token_value
            
            
            
if __name__ == '__main__':
    tokenizer = JackTokenizer('bloxors/Level.jack')
    for token_type, value in tokenizer.tokenize():
        print(f'<{token_type}> {value} </{token_type}>')
