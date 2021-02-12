from genelang import *

engine = Engine(Lexer(Pattern(name='KW_PATTERN', mode='str', expr='@', flag=0, ignore=False), Pattern(name='KW_MATCH', mode='str', expr='$', flag=0, ignore=False), Pattern(name='KW_CALL', mode='str', expr='>', flag=0, ignore=False), Pattern(name='KW_RE', mode='kw', expr='re', flag=0, ignore=False), Pattern(name='KW_KW', mode='kw', expr='kw', flag=0, ignore=False), Pattern(name='KW_STR', mode='kw', expr='str', flag=0, ignore=False), Pattern(name='KW_IGNORE', mode='kw', expr='ignore', flag=0, ignore=False), Pattern(name='KW_AS', mode='kw', expr='as', flag=0, ignore=False), Pattern(name='KW_IN', mode='kw', expr='in', flag=0, ignore=False), Pattern(name='KW_WHILE', mode='kw', expr='while', flag=0, ignore=False), Pattern(name='KW_FORK', mode='kw', expr='fork', flag=0, ignore=False), Pattern(name='KW_ANY', mode='kw', expr='any', flag=0, ignore=False), Pattern(name='KW_OPTIONAL', mode='kw', expr='optional', flag=0, ignore=False), Pattern(name='KW_BUILD', mode='kw', expr='build', flag=0, ignore=False), Pattern(name='KW_BLOC', mode='kw', expr='bloc', flag=0, ignore=False), Pattern(name='KW_L_UNARY', mode='kw', expr='l_unary', flag=0, ignore=False), Pattern(name='KW_R_UNARY', mode='kw', expr='r_unary', flag=0, ignore=False), Pattern(name='KW_BINARY', mode='kw', expr='binary', flag=0, ignore=False), Pattern(name='VAR', mode='re', expr='[a-zA-Z_][a-zA-Z0-9_]*', flag=0, ignore=False), Pattern(name='INT', mode='re', expr='[0-9]+', flag=0, ignore=False), Pattern(name='STR', mode='re', expr="'.*?'", flag=16, ignore=False), Pattern(name='STR', mode='re', expr='".*?"', flag=16, ignore=False), Pattern(name='EQUAL', mode='str', expr='=', flag=0, ignore=False), Pattern(name='LP', mode='str', expr='(', flag=0, ignore=False), Pattern(name='RP', mode='str', expr=')', flag=0, ignore=False), Pattern(name='LS', mode='str', expr='{', flag=0, ignore=False), Pattern(name='RS', mode='str', expr='}', flag=0, ignore=False), Pattern(name='LB', mode='str', expr='[', flag=0, ignore=False), Pattern(name='RB', mode='str', expr=']', flag=0, ignore=False), Pattern(name='COMA', mode='str', expr=',', flag=0, ignore=False), Pattern(name='WHITESPACE', mode='re', expr='[ \t\n]', flag=16, ignore=True), Pattern(name='ERROR', mode='re', expr='.+', flag=16, ignore=False)), Parser(Build('Pattern', Branch(LUnary('KW_PATTERN', As('name', Match('VAR')), As('mode', Any(Match('KW_RE'), Match('KW_STR'), Match('KW_KW'))), As('expr', Match('STR')), Optional(As('flag', Match('INT'))), Optional(As('ignore_', Match('KW_IGNORE')))))), Build('Match', Branch(LUnary('KW_MATCH', As('name', Match('VAR'))))), Build('Call', Branch(LUnary('KW_CALL', As('name', Match('VAR'))))), Build('While', Branch(LUnary('KW_WHILE', Call('InstructionList')))), Build('Optional', Branch(LUnary('KW_OPTIONAL', Call('InstructionList')))), Build('Any', Branch(LUnary('KW_ANY', Call('InstructionList')))), Build('Branch', Branch(Call('InstructionList'))), Build('Bloc', Branch(LUnary('KW_BLOC', Bloc('LP', 'RP', As('left', Match('VAR')), Match('COMA'), As('right', Match('VAR'))), Call('InstructionList')))), Build('LUnary', Branch(LUnary('KW_L_UNARY', Bloc('LP', 'RP', As('name', Match('VAR'))), Call('InstructionList')))), Build('RUnary', Branch(LUnary('KW_R_UNARY', Bloc('LP', 'RP', As('name', Match('VAR'))), Call('InstructionList')))), Build('Binary', Branch(LUnary('KW_BINARY', Bloc('LP', 'RP', As('name', Match('VAR'))), Bloc('LS', 'RS', As('left', Call('Instruction')), As('right', Call('Instruction')))))), Build('In', Branch(Binary('KW_IN', As('process', Call('RawInstruction')), As('name', Match('VAR'))))), Build('As', Branch(Binary('KW_AS', As('process', Call('RawInstruction')), As('name', Match('VAR'))))), Build('Build', Branch(LUnary('KW_BUILD', Bloc('LP', 'RP', As('name', Match('VAR'))), As('process', Call('Instruction'))))), Build('NamedProcess', Branch(As('name', Match('VAR')), As('process', Call('Branch')))), Build('Parser', Branch(While(In('builds', Any(Call('Build'), Call('NamedProcess')))))), Build('Lexer', Branch(While(In('patterns', Call('Pattern'))))), NamedProcess('InstructionList', Branch(Bloc('LS', 'RS', While(In('items', Call('Instruction')))))), NamedProcess('RawInstruction', Branch(Any(Call('Match'), Call('Call'), Call('While'), Call('Optional'), Call('Any'), Call('Build'), Call('Bloc'), Call('LUnary'), Call('RUnary'), Call('Binary'), Call('NamedProcess'), Call('Branch')))), NamedProcess('Instruction', Branch(Any(Call('In'), Call('As'), Call('RawInstruction')))), Build('Engine', Branch(As('lexer', Call('Lexer')), As('parser', Call('Parser'))))))
