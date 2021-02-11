from genelang import *

engine = Engine(
    Lexer(
        Pattern('KW_PATTERN', 'str', '@', 0, False),
        Pattern('KW_MATCH', 'str', '$', 0, False),
        Pattern('KW_CALL', 'str', '>', 0, False),
        Pattern('KW_RE', 'kw', 're', 0, False),
        Pattern('KW_KW', 'kw', 'kw', 0, False),
        Pattern('KW_STR', 'kw', 'str', 0, False),
        Pattern('KW_IGNORE', 'kw', 'ignore', 0, False),
        Pattern('KW_AS', 'kw', 'as', 0, False),
        Pattern('KW_IN', 'kw', 'in', 0, False),
        Pattern('KW_WHILE', 'kw', 'while', 0, False),
        Pattern('KW_FORK', 'kw', 'fork', 0, False),
        Pattern('KW_ANY', 'kw', 'any', 0, False),
        Pattern('KW_OPTIONAL', 'kw', 'optional', 0, False),
        Pattern('KW_BUILD', 'kw', 'build', 0, False),
        Pattern('KW_BLOC', 'kw', 'bloc', 0, False),
        Pattern('KW_L_UNARY', 'kw', 'l_unary', 0, False),
        Pattern('KW_R_UNARY', 'kw', 'r_unary', 0, False),
        Pattern('KW_BINARY', 'kw', 'binary', 0, False),
        Pattern('VAR', 're', '[a-zA-Z_][a-zA-Z0-9_]*', 0, False),
        Pattern('INT', 're', '[0-9]+', 0, False),
        Pattern('STR', 're', "'.*?'", 16, False),
        Pattern('STR', 're', '".*?"', 16, False),
        Pattern('EQUAL', 'str', '=', 0, False),
        Pattern('LP', 'str', '(', 0, False),
        Pattern('RP', 'str', ')', 0, False),
        Pattern('LS', 'str', '{', 0, False),
        Pattern('RS', 'str', '}', 0, False),
        Pattern('LB', 'str', '[', 0, False),
        Pattern('RB', 'str', ']', 0, False),
        Pattern('COMA', 'str', ',', 0, False),
        Pattern('WHITESPACE', 're', '[ \t\n]', 16, True),
        Pattern('ERROR', 're', '.+', 16, False)
    ),
    Parser(
        Build(
            'Pattern',
            Branch(
                Match('KW_PATTERN'),
                As('name', Match('VAR')),
                As('mode', Any(
                    Match('KW_RE'),
                    Match('KW_STR'),
                    Match('KW_KW')
                )),
                As('expr', Match('STR')),
                Optional(
                    As('flag', Match('INT'))
                ),
                Optional(
                    As('ignore_', Match('KW_IGNORE'))
                )
            )
        ),
        Build(
            'Match',
            Branch(
                Match('KW_MATCH'),
                As('name', Match('VAR'))
            )
        ),
        Build(
            'Call',
            Branch(
                Match('KW_CALL'),
                As('name', Match('VAR'))
            )
        ),
        Build(
            'While',
            Branch(
                Match('KW_WHILE'),
                Call('InstructionList')
            )
        ),
        Build(
            'Optional',
            Branch(
                Match('KW_OPTIONAL'),
                Call('InstructionList')
            )
        ),
        Build(
            'Any',
            Branch(
                Match('KW_ANY'),
                Call('InstructionList')
            )
        ),
        Build(
            'Branch',
            Branch(
                Call('InstructionList')
            )
        ),
        Build(
            'Bloc',
            Branch(
                Match('KW_BLOC'),
                Bloc(
                    'LP',
                    'RP',
                    As('left', Match('VAR')),
                    Match('COMA'),
                    As('right', Match('VAR'))
                ),
                Call('InstructionList')
            )
        ),
        Build(
            'LUnary',
            Branch(
                Match('KW_L_UNARY'),
                Bloc(
                    'LP',
                    'RP',
                    As('key', Match('VAR'))
                ),
                Call('InstructionList')
            )
        ),
        Build(
            'RUnary',
            Branch(
                Match('KW_R_UNARY'),
                Bloc(
                    'LP',
                    'RP',
                    As('key', Match('VAR'))
                ),
                Call('InstructionList')
            )
        ),
        Build(
            'Binary',
            Branch(
                Match('KW_BINARY'),
                Bloc(
                    'LP',
                    'RP',
                    As('key', Match('VAR'))
                ),
                Bloc(
                    'LS',
                    'RS',
                    As('left', Call('Instruction')),
                    As('right', Call('Instruction'))
                )
            )
        ),
        Build(
            'In',
            Branch(
                As('process', Call('RawInstruction')),
                Match('KW_IN'),
                As('name', Match('VAR'))
            )
        ),
        Build(
            'As',
            Branch(
                As('process', Call('RawInstruction')),
                Match('KW_AS'),
                As('name', Match('VAR'))
            )
        ),
        Build(
            'Build',
            Branch(
                Match('KW_BUILD'),
                Bloc(
                    'LP',
                    'RP',
                    As('name', Match('VAR'))
                ),
                As('process', Call('Instruction'))
            )
        ),
        Build(
            'NamedProcess',
            Branch(
                As('name', Match('VAR')),
                As('process', Call('Branch'))
            )
        ),
        Build(
            'Parser',
            Branch(
                While(
                    In('builds', Any(
                        Call('Build'),
                        Call('NamedProcess')
                    ))
                )
            )
        ),
        Build(
            'Lexer',
            Branch(
                While(
                    In('patterns', Call('Pattern'))
                )
            )
        ),
        NamedProcess(
            'InstructionList',
            Branch(
                Bloc(
                    'LS',
                    'RS',
                    While(
                        In('instructions', Call('Instruction'))
                    )
                )
            )
        ),
        NamedProcess(
            'RawInstruction',
            Branch(
                Any(
                    Call('Match'),
                    Call('Call'),
                    Call('While'),
                    Call('Optional'),
                    Call('Any'),
                    Call('Build'),
                    Call('Bloc'),
                    Call('LUnary'),
                    Call('RUnary'),
                    Call('Binary'),
                    Call('NamedProcess'),
                    Call('Branch')
                )
            )
        ),
        NamedProcess(
            'Instruction',
            Branch(
                Any(
                    Call('In'),
                    Call('As'),
                    Call('RawInstruction')
                )
            )
        ),
        default=Build(
            'Engine',
            Branch(
                As('lexer', Call('Lexer')),
                As('parser', Call('Parser'))
            )
        )
    )
)
