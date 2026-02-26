"""
tests for tokenizer.py and parser.py
run: python3 example.py
"""

import os
import sys
import io
import tempfile

from tokenizer import JackTokenizer
from parser import JackParser

PASS = 0
FAIL = 0

def check(name, got, expected):
    global PASS, FAIL
    if got == expected:
        PASS += 1
    else:
        FAIL += 1
        print(f"    FAIL {name}: got {got!r}, expected {expected!r}")


def tokenize_string(code):
    """dump code to a temp file and tokenize it"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jack', delete=False) as f:
        f.write(code)
        f.flush()
        path = f.name
    try:
        t = JackTokenizer(path)
        return list(t.tokenize())
    finally:
        os.unlink(path)


def parse_string(code):
    """tokenize + parse, return the xml as a string"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jack', delete=False) as f:
        f.write(code)
        f.flush()
        path = f.name
    try:
        t = JackTokenizer(path)
        output = io.StringIO()
        p = JackParser(t.tokenize(), output)
        p.compile_class()
        return output.getvalue()
    finally:
        os.unlink(path)


# -- tokenizer --

def test_keywords():
    print("  basic token types")
    tokens = tokenize_string('class Main { }')
    check("class is KEYWORD", tokens[0], ('KEYWORD', 'class'))
    check("Main is IDENTIFIER", tokens[1], ('IDENTIFIER', 'Main'))
    check("{ is SYMBOL", tokens[2], ('SYMBOL', '{'))
    check("} is SYMBOL", tokens[3], ('SYMBOL', '}'))


def test_all_keywords():
    print("  all 21 keywords")
    all_kw = ['class', 'constructor', 'function', 'method', 'field', 'static',
              'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
              'this', 'let', 'do', 'if', 'else', 'while', 'return']
    code = ' '.join(all_kw)
    tokens = tokenize_string(code)
    for i, kw in enumerate(all_kw):
        check(f"'{kw}' type", tokens[i][0], 'KEYWORD')
        check(f"'{kw}' value", tokens[i][1], kw)


def test_symbols():
    print("  all symbols")
    symbols = '{}()[].,;+-*/&|<>=~'
    tokens = tokenize_string(symbols)
    for i, sym in enumerate(symbols):
        check(f"symbol '{sym}'", tokens[i], ('SYMBOL', sym))


def test_int_constants():
    print("  integer constants")
    tokens = tokenize_string('let x = 42;')
    check("= is symbol", tokens[2], ('SYMBOL', '='))
    check("42 value", tokens[3], ('INT_CONST', '42'))


def test_string_constants():
    print("  string constants (should strip quotes)")
    tokens = tokenize_string('do Output.printString("hello world");')
    string_tokens = [t for t in tokens if t[0] == 'STRING_CONST']
    check("found 1 string", len(string_tokens), 1)
    check("quotes stripped", string_tokens[0][1], 'hello world')


def test_identifiers():
    print("  identifiers vs keywords")
    tokens = tokenize_string('var int myVar;')
    check("var is KEYWORD", tokens[0][0], 'KEYWORD')
    check("int is KEYWORD", tokens[1][0], 'KEYWORD')
    check("myVar is IDENTIFIER", tokens[2][0], 'IDENTIFIER')


def test_single_line_comments():
    print("  single-line comments")
    tokens = tokenize_string('let x = 1; // this is a comment\nlet y = 2;')
    identifiers = [t[1] for t in tokens if t[0] == 'IDENTIFIER']
    check("x and y found", identifiers, ['x', 'y'])
    all_values = [t[1] for t in tokens]
    check("no comment text leaked", 'comment' not in ' '.join(all_values), True)


def test_multiline_comments():
    print("  multi-line comments")
    code = """
    /* This is a
       multi-line comment */
    class Foo { }
    """
    tokens = tokenize_string(code)
    check("class found after comment", tokens[0], ('KEYWORD', 'class'))
    check("only 4 tokens", len(tokens), 4)


def test_api_comment_block():
    print("  /** doc comments")
    code = """
    /** Returns the value.
      * @param none
      */
    class Bar { }
    """
    tokens = tokenize_string(code)
    check("class found", tokens[0], ('KEYWORD', 'class'))


# -- parser --

def test_parse_empty_class():
    print("  empty class")
    xml = parse_string('class Empty { }')
    check("starts with <class>", xml.strip().startswith('<class>'), True)
    check("ends with </class>", xml.strip().endswith('</class>'), True)
    check("has class keyword", 'class' in xml, True)
    check("has class name", 'Empty' in xml, True)


def test_parse_class_var_dec():
    print("  class var declarations")
    code = """
    class Foo {
        field int x, y;
        static boolean flag;
    }
    """
    xml = parse_string(code)
    check("has classVarDec", '<classVarDec>' in xml, True)
    check("has field", 'field' in xml, True)
    check("has static", 'static' in xml, True)


def test_parse_subroutine():
    print("  subroutine")
    code = """
    class Bar {
        function void main() {
            return;
        }
    }
    """
    xml = parse_string(code)
    check("has subroutineDec", '<subroutineDec>' in xml, True)
    check("has subroutineBody", '<subroutineBody>' in xml, True)
    check("has parameterList", '<parameterList>' in xml, True)
    check("has returnStatement", '<returnStatement>' in xml, True)


def test_parse_let_statement():
    print("  let + var dec")
    code = """
    class Test {
        function void main() {
            var int x;
            let x = 42;
            return;
        }
    }
    """
    xml = parse_string(code)
    check("has varDec", '<varDec>' in xml, True)
    check("has letStatement", '<letStatement>' in xml, True)
    check("has expression", '<expression>' in xml, True)


def test_parse_if_while():
    print("  if/while")
    code = """
    class Test {
        function void main() {
            var int x;
            let x = 0;
            while (x < 10) {
                let x = x + 1;
            }
            if (x = 10) {
                return;
            } else {
                return;
            }
            return;
        }
    }
    """
    xml = parse_string(code)
    check("has whileStatement", '<whileStatement>' in xml, True)
    check("has ifStatement", '<ifStatement>' in xml, True)


def test_parse_do_statement():
    print("  do + method call")
    code = """
    class Test {
        function void main() {
            do Output.printInt(42);
            return;
        }
    }
    """
    xml = parse_string(code)
    check("has doStatement", '<doStatement>' in xml, True)
    check("has expressionList", '<expressionList>' in xml, True)


def test_parse_expressions():
    print("  expressions")
    code = """
    class Test {
        function int calc() {
            var int a, b;
            let a = 3 + 4 * 2;
            let b = -a;
            let b = ~b;
            return a + b;
        }
    }
    """
    xml = parse_string(code)
    check("has term", '<term>' in xml, True)
    check("multiple expressions", xml.count('<expression>') >= 4, True)


def test_parse_array_access():
    print("  array access")
    code = """
    class Test {
        function void main() {
            var Array a;
            let a[0] = 100;
            return;
        }
    }
    """
    xml = parse_string(code)
    check("has letStatement", '<letStatement>' in xml, True)
    check("has [ somewhere", '[' in xml or '&lt;' in xml, True)


# -- run on the actual jack files from project 9 --

def test_parse_real_jack_files():
    print("  parsing real .jack files from project 9")
    project9 = os.path.join(os.path.dirname(__file__), '..', 'project09-high-level-language')

    if not os.path.exists(project9):
        print("    SKIP: project09 not found")
        return

    jack_files = []
    for root, dirs, files in os.walk(project9):
        for f in files:
            if f.endswith('.jack'):
                jack_files.append(os.path.join(root, f))

    if not jack_files:
        print("    SKIP: no .jack files found")
        return

    for jack_path in sorted(jack_files):
        rel = os.path.relpath(jack_path, project9)
        try:
            t = JackTokenizer(jack_path)
            tokens = list(t.tokenize())

            t2 = JackTokenizer(jack_path)
            output = io.StringIO()
            p = JackParser(t2.tokenize(), output)
            p.compile_class()
            xml = output.getvalue()

            xml_lines = len(xml.strip().split('\n'))
            ok = xml.strip().startswith('<class>') and xml.strip().endswith('</class>')

            global PASS, FAIL
            if ok:
                PASS += 1
            else:
                FAIL += 1

            status = "OK" if ok else "FAIL"
            print(f"    {rel:>30}  {len(tokens):>4} tokens  {xml_lines:>4} xml lines  {status}")
        except Exception as e:
            FAIL += 1
            print(f"    {rel:>30}  FAIL: {e}")


if __name__ == '__main__':
    print("=== project 10: tokenizer + parser tests ===\n")

    print("-- tokenizer --")
    test_keywords()
    test_all_keywords()
    test_symbols()
    test_int_constants()
    test_string_constants()
    test_identifiers()
    test_single_line_comments()
    test_multiline_comments()
    test_api_comment_block()

    print("\n-- parser --")
    test_parse_empty_class()
    test_parse_class_var_dec()
    test_parse_subroutine()
    test_parse_let_statement()
    test_parse_if_while()
    test_parse_do_statement()
    test_parse_expressions()
    test_parse_array_access()

    print("\n-- integration --")
    test_parse_real_jack_files()

    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
