import re
import sys

# Assumes the regex-based JackTokenizer class is defined above this.

class JackParser:
    def __init__(self, tokenizer_generator, output_file):
        """Prepares the parser by buffering all tokens."""
        self._tokens = list(tokenizer_generator)
        self._current_token_index = 0
        self._output = output_file
        self._indent_level = 0

    # --- Core Engine: Token Navigation and State ---

    def _advance(self):
        """Advances the token stream by one token."""
        if self._current_token_index < len(self._tokens):
            self._current_token_index += 1

    @property
    def current_token_type(self):
        """Returns the type of the current token."""
        if self._current_token_index < len(self._tokens):
            return self._tokens[self._current_token_index][0]
        return None

    @property
    def current_token_value(self):
        """Returns the value of the current token."""
        if self._current_token_index < len(self._tokens):
            return self._tokens[self._current_token_index][1]
        return None

    def _peek_next_token(self):
        """Looks at the next token without consuming the current one."""
        if self._current_token_index + 1 < len(self._tokens):
            return self._tokens[self._current_token_index + 1]
        return (None, None)

    # --- XML Writing and Token Consumption ---

    def _write_xml(self, tag):
        """Helper to write indented XML tags."""
        indent = "  " * self._indent_level
        self._output.write(f"{indent}<{tag}>\n")

    def _eat(self, expected_type=None, expected_values=None):
        """
        Asserts the current token, writes its XML, and advances.
        Handles single strings or collections for expected types/values.
        """
        if self.current_token_type is None:
            raise SyntaxError("Unexpected end of file.")

        token_type = self.current_token_type
        token_value = self.current_token_value

        if expected_type:
            allowed_types = {expected_type} if isinstance(expected_type, str) else set(expected_type)
            if token_type not in allowed_types:
                raise SyntaxError(f"Expected type(s) {allowed_types} but got '{token_type}' for value '{token_value}'")

        if expected_values:
            allowed_values = {expected_values} if isinstance(expected_values, str) else set(expected_values)
            if token_value not in allowed_values:
                raise SyntaxError(f"Expected value(s) {allowed_values} but got '{token_value}'")

        xml_tag = token_type.lower().replace('_const', 'Constant')
        xml_value = token_value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        self._write_xml(f"{xml_tag}> {xml_value} </{xml_tag}")
        self._advance()

    # --- Program Structure Compilation ---

    def compile_class(self):
        """'class' className '{' classVarDec* subroutineDec* '}'"""
        self._write_xml("class")
        self._indent_level += 1
        self._eat(expected_type='KEYWORD', expected_values='class')
        self._eat(expected_type='IDENTIFIER')
        self._eat(expected_type='SYMBOL', expected_values='{')
        while self.current_token_value in ('static', 'field'):
            self.compile_class_var_dec()
        while self.current_token_value in ('constructor', 'function', 'method'):
            self.compile_subroutine()
        self._eat(expected_type='SYMBOL', expected_values='}')
        self._indent_level -= 1
        self._write_xml("/class")

    def compile_class_var_dec(self):
        """('static' | 'field') type varName (',' varName)* ';'"""
        self._write_xml("classVarDec")
        self._indent_level += 1
        self._eat(expected_type='KEYWORD', expected_values=('static', 'field'))
        self._eat(expected_type=('KEYWORD', 'IDENTIFIER')) # type
        self._eat(expected_type='IDENTIFIER') # varName
        while self.current_token_value == ',':
            self._eat(expected_type='SYMBOL', expected_values=',')
            self._eat(expected_type='IDENTIFIER')
        self._eat(expected_type='SYMBOL', expected_values=';')
        self._indent_level -= 1
        self._write_xml("/classVarDec")

    def compile_subroutine(self):
        """('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody"""
        self._write_xml("subroutineDec")
        self._indent_level += 1
        self._eat(expected_type='KEYWORD', expected_values=('constructor', 'function', 'method'))
        self._eat(expected_type=('KEYWORD', 'IDENTIFIER')) # 'void' or type
        self._eat(expected_type='IDENTIFIER') # subroutineName
        self._eat(expected_type='SYMBOL', expected_values='(')
        self.compile_parameter_list()
        self._eat(expected_type='SYMBOL', expected_values=')')
        self.compile_subroutine_body()
        self._indent_level -= 1
        self._write_xml("/subroutineDec")

    def compile_parameter_list(self):
        """((type varName) (',' type varName)*)? """
        self._write_xml("parameterList")
        self._indent_level += 1
        if self.current_token_value != ')':
            self._eat(expected_type=('KEYWORD', 'IDENTIFIER')) # type
            self._eat(expected_type='IDENTIFIER') # varName
            while self.current_token_value == ',':
                self._eat(expected_type='SYMBOL', expected_values=',')
                self._eat(expected_type=('KEYWORD', 'IDENTIFIER'))
                self._eat(expected_type='IDENTIFIER')
        self._indent_level -= 1
        self._write_xml("/parameterList")

    def compile_subroutine_body(self):
        """'{' varDec* statements '}'"""
        self._write_xml("subroutineBody")
        self._indent_level += 1
        self._eat(expected_type='SYMBOL', expected_values='{')
        while self.current_token_value == 'var':
            self.compile_var_dec()
        self.compile_statements()
        self._eat(expected_type='SYMBOL', expected_values='}')
        self._indent_level -= 1
        self._write_xml("/subroutineBody")

    def compile_var_dec(self):
        """'var' type varName (',' varName)* ';'"""
        self._write_xml("varDec")
        self._indent_level += 1
        self._eat(expected_type='KEYWORD', expected_values='var')
        self._eat(expected_type=('KEYWORD', 'IDENTIFIER')) # type
        self._eat(expected_type='IDENTIFIER') # varName
        while self.current_token_value == ',':
            self._eat(expected_type='SYMBOL', expected_values=',')
            self._eat(expected_type='IDENTIFIER')
        self._eat(expected_type='SYMBOL', expected_values=';')
        self._indent_level -= 1
        self._write_xml("/varDec")

    # --- Statement Compilation ---

    def compile_statements(self):
        """A sequence of statements."""
        self._write_xml("statements")
        self._indent_level += 1
        while self.current_token_value in ('let', 'if', 'while', 'do', 'return'):
            if self.current_token_value == 'let':
                self.compile_let()
            elif self.current_token_value == 'if':
                self.compile_if()
            elif self.current_token_value == 'while':
                self.compile_while()
            elif self.current_token_value == 'do':
                self.compile_do()
            elif self.current_token_value == 'return':
                self.compile_return()
        self._indent_level -= 1
        self._write_xml("/statements")

    def compile_let(self):
        """'let' varName ('[' expression ']')? '=' expression ';'"""
        self._write_xml("letStatement")
        self._indent_level += 1
        self._eat(expected_type='KEYWORD', expected_values='let')
        self._eat(expected_type='IDENTIFIER')
        if self.current_token_value == '[':
            self._eat(expected_type='SYMBOL', expected_values='[')
            self.compile_expression()
            self._eat(expected_type='SYMBOL', expected_values=']')
        self._eat(expected_type='SYMBOL', expected_values='=')
        self.compile_expression()
        self._eat(expected_type='SYMBOL', expected_values=';')
        self._indent_level -= 1
        self._write_xml("/letStatement")

    def compile_if(self):
        """'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?"""
        self._write_xml("ifStatement")
        self._indent_level += 1
        self._eat(expected_type='KEYWORD', expected_values='if')
        self._eat(expected_type='SYMBOL', expected_values='(')
        self.compile_expression()
        self._eat(expected_type='SYMBOL', expected_values=')')
        self._eat(expected_type='SYMBOL', expected_values='{')
        self.compile_statements()
        self._eat(expected_type='SYMBOL', expected_values='}')
        if self.current_token_value == 'else':
            self._eat(expected_type='KEYWORD', expected_values='else')
            self._eat(expected_type='SYMBOL', expected_values='{')
            self.compile_statements()
            self._eat(expected_type='SYMBOL', expected_values='}')
        self._indent_level -= 1
        self._write_xml("/ifStatement")

    def compile_while(self):
        """'while' '(' expression ')' '{' statements '}'"""
        self._write_xml("whileStatement")
        self._indent_level += 1
        self._eat(expected_type='KEYWORD', expected_values='while')
        self._eat(expected_type='SYMBOL', expected_values='(')
        self.compile_expression()
        self._eat(expected_type='SYMBOL', expected_values=')')
        self._eat(expected_type='SYMBOL', expected_values='{')
        self.compile_statements()
        self._eat(expected_type='SYMBOL', expected_values='}')
        self._indent_level -= 1
        self._write_xml("/whileStatement")

    def compile_do(self):
        """'do' subroutineCall ';'"""
        self._write_xml("doStatement")
        self._indent_level += 1
        self._eat(expected_type='KEYWORD', expected_values='do')
        # A subroutine call is a type of term, so we can reuse the logic
        self.compile_term()
        self._eat(expected_type='SYMBOL', expected_values=';')
        self._indent_level -= 1
        self._write_xml("/doStatement")

    def compile_return(self):
        """'return' expression? ';'"""
        self._write_xml("returnStatement")
        self._indent_level += 1
        self._eat(expected_type='KEYWORD', expected_values='return')
        if self.current_token_value != ';':
            self.compile_expression()
        self._eat(expected_type='SYMBOL', expected_values=';')
        self._indent_level -= 1
        self._write_xml("/returnStatement")

    # --- Expression Compilation ---

    def compile_expression(self):
        """term (op term)*"""
        self._write_xml("expression")
        self._indent_level += 1
        self.compile_term()
        while self.current_token_value in '+-*/&|<>=':
            self._eat(expected_type='SYMBOL')
            self.compile_term()
        self._indent_level -= 1
        self._write_xml("/expression")

    def compile_term(self):
        """Compiles a term using proper lookahead."""
        self._write_xml("term")
        self._indent_level += 1

        token_type = self.current_token_type
        token_value = self.current_token_value

        if token_type in ('INT_CONST', 'STRING_CONST') or \
           (token_type == 'KEYWORD' and token_value in ('true', 'false', 'null', 'this')):
            self._eat()
        elif token_type == 'SYMBOL' and token_value in ('-', '~'):
            self._eat(expected_type='SYMBOL', expected_values=('-', '~'))
            self.compile_term()
        elif token_type == 'SYMBOL' and token_value == '(':
            self._eat(expected_type='SYMBOL', expected_values='(')
            self.compile_expression()
            self._eat(expected_type='SYMBOL', expected_values=')')
        elif token_type == 'IDENTIFIER':
            next_type, next_value = self._peek_next_token()
            if next_value == '[':
                self._eat(expected_type='IDENTIFIER')
                self._eat(expected_type='SYMBOL', expected_values='[')
                self.compile_expression()
                self._eat(expected_type='SYMBOL', expected_values=']')
            elif next_value in ('.', '('):
                # Subroutine call
                self._eat(expected_type='IDENTIFIER')
                if next_value == '.':
                    self._eat(expected_type='SYMBOL', expected_values='.')
                    self._eat(expected_type='IDENTIFIER')
                self._eat(expected_type='SYMBOL', expected_values='(')
                self.compile_expression_list()
                self._eat(expected_type='SYMBOL', expected_values=')')
            else:
                self._eat(expected_type='IDENTIFIER')
        else:
            raise SyntaxError(f"Invalid term: cannot start with '{token_value}' of type '{token_type}'")

        self._indent_level -= 1
        self._write_xml("/term")

    def compile_expression_list(self):
        """(expression (',' expression)*)?"""
        self._write_xml("expressionList")
        self._indent_level += 1
        if self.current_token_value != ')':
            self.compile_expression()
            while self.current_token_value == ',':
                self._eat(expected_type='SYMBOL', expected_values=',')
                self.compile_expression()
        self._indent_level -= 1
        self._write_xml("/expressionList")
        
        
        
if __name__ == '__main__':
    from tokenizer import JackTokenizer
    tokenizer = JackTokenizer('bloxors/Level.jack')
    parser = JackParser(tokenizer.tokenize(), open('bloxors/Level.xml', 'w'))
    parser.compile_class()
