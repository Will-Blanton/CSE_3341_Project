from enum import Enum

Fun = Enum('Fun',
	'PROGRAM,\
	BEGIN,\
	END,\
	NEW,\
    INT,\
	REF,\
	INSTANCE,\
	IF,\
	THEN,\
	ELSE,\
	WHILE,\
    OR,\
    AND,\
    READ,\
    WRITE,\
    SHARE,\
    ID,\
    CONST,\
	SEMICOLON,\
	LPAREN,\
	RPAREN,\
	COMMA,\
	ASSIGN,\
	NEGATION,\
	EQUAL,\
	LESS\
	LESSEQUAL,\
	ADD,\
	SUB,\
	MULT,\
    LBRACE,\
    RBRACE,\
	EOS,\
	ERROR'
)