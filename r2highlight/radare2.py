# -*- coding: utf-8 -*-
"""
    pygments.lexers.radare2
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Radare2 commandline output and Visual Mode.

"""

from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import *

__all__ = ['Radare2Lexer']

class Radare2Lexer(RegexLexer):
    name = 'Radare2'
    aliases = ['r2', 'radare2']
    filenames = []

    tokens = {
        'root': [
            (r'\n', Text),
            (r'^\[', Text, 'cmdprompt'),
            (r'^sys', String, 'dmoutput'),
            (r'0[Xx]',String, 'addroutput'),
            (r'^[|\\/ ]', Keyword, 'pdoutput'),
            (r'^-> % ', Keyword, 'bashprompt'),
            (r'^[^[]', Text, 'stroutput'),
        ],

        'bashprompt': [
            (r'[^|\n]+', Text),
            (r'\|', Operator)
        ],

        'dmoutput': [
        #    #(r'(\s+)([0-9.]+)(.)(\s)(0[Xx][0-9a-f]+)(\s)(.)(\s)(0[Xx][0-9a-f])(\s)(.)(\s)([-rwx]+)(\s)
            (r'[0-9.]+(?:M|K)', Keyword),
            (r'0[Xx][0-9a-f]+', Number.Hex),
            (r'\bs\b', Text),
            (r'[rwx-]{4}', Operator),
            #(r'-|\*|/|_', Operator),
            (r'[-*/_.;[\]]', Operator),
            (r' ', Text),
            (r'[A-Za-z0-9]+', Text)
        ],

        'pdoutput': [
            (r'--', Text, 'stroutput'),
            (r'/|\||\\', Keyword),
            (r'[,`][=-]+[<>]', Keyword),
            (r' ', Text),
            (r';$', Text),
            (r',', Operator),
            (r';', Comment, 'comment'),
            (r'(\()(.+?)(\))', bygroups(Text, Operator, Text)),
            (r'([A-Za-z]{3})(\.)([A-Za-z]{3})(\.)(\w+)', bygroups(Keyword, Operator, Keyword, Operator, Text)),
            (r'([A-Za-z]{3})(\.)(\w+)', bygroups(Keyword, Operator, Text)),
            (r'\(\)', Text),
            (r'(0[Xx][0-9a-f]{8,})([ ]+)([0-9a-f]+\.?)([ ]+)', bygroups(String, Text, Text, Text)),
            include('stackops'),
            include('arithmeticops'),
            include('logicops'),
            include('ipops'),
            include('otherops'),
            include('registers'),
            (r'0[Xx][0-9a-f]+', Number.Hex),
            (r'[0-9a-f]', Number)
        ],


        'comment': [
            (r'.+$', Comment, '#pop')
        ],

        'cmdprompt': [
            (r'(0[xX][0-9a-f]+)(\])(>)(\s+)(\w+)?(.*)', bygroups(Number.Hex, Text, Operator, Text, Name.Function, Text)),
            (r'.+', Text)
        ],

        'addroutput': [
            (r'([0-9a-f]+)(\s{2})(.+)(\s{2})(.+)$', bygroups(String, Text, Number.Hex, Text, Text)),
            #(r'^\[', Text, '#pop'),
            #(r'(0[Xx][0-9a-f])(\s+)(.+)$', bygroups(Number.Hex, Text, Text))
        ],

        'stroutput': [
            (r'[A-Za-z%_)<>]+', Text),
            (r' ', Text),
            (r'(?:0[Xx])?[0-9a-f]+', Number.Hex),
            (r'[.:+/-]', Operator),
            (r'[|]', Keyword),
        ],

        'registers': [
            (words(('rsp', 'esp', 'spl', 'rbp', 'ebp', 'bpl', 'rax', 'eax', 'ah', 'al', 'rbx', 'ebx', 'bh', 'bl', 'rcx', 'ecx', 'cx', 'ch', 'cl', 'rdx', 'edx', 'dx', 'dh', 'dl', 'rdi', 'edi', 'dil', 'rsi', 'esi', 'sil', 'r15', 'r14', 'r13', 'r12', 'r10', 'r9', 'r9d', 'r8', 'fs:', 'gs:')),
            Keyword)
        ],

        'otherops': [
            (words(('in', 'byte', 'sbb', 'clc', 'nop', '.qword', 'qword', 'dword', 'local_', '[', 'h]', ']', '-', '+')),
            Text)
        ],

        'stackops': [
            (words(('push', 'pop'), prefix=r'\b', suffix=r'\b'),
            Keyword)
        ],

        'logicops': [
            (words(('and', 'or', 'not', 'xor', 'cmp'), suffix=r'\b', prefix=r'\b'),
            String)
        ],

        'arithmeticops': [
            (words(('leave', 'mov', 'movzx', 'movsx', 'lea', 'add', 'sub', 'imul', 'mul', 'shl', 'shr', 'sar', 'sal'), suffix=r'\b', prefix=r'\b'),
            Operator)
        ],

        'ipops': [
            (words(('je', 'jmp', 'jne', 'jae', 'jbe', 'call', 'ret'), suffix=r'\b', prefix=r'\b'),
            Name.Function)
        ]
    }

