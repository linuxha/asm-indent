#!/usr/bin/python3

# http://www.8bit-era.cz/6800.html
import os, sys
import re
import traceback

#
ln = 0

# Read in asm file, reformat

help = """
HELP
asm-indent.py <filename> |& tee <newfilename>
"""

if(len(sys.argv) != 2) :
    # put help here
    print(help, file=sys.stderr)
    exit(-1);
#

# Examples
#       	NAM RT68-V2
# SYSMOD	RMB	1	* RT MODE 0=USER 1=EXEC
# BEGADR	RMB	2
# STACK		EQU	*	* MONITOR STACK
# LOAD		LDAB	#$3C	* TAPE ON CONSTANTS
# 		LDAA	#$11	* READER ON CODE
#       STA A M12 * STORE A IN M12
#		BSR	INCH	*
#       NOP
#		RTS		*
#
# LABEL OP VALUE Comment...
#
def func(s):
    asmOps(s)
#

def lAsmOps(s):
    pass
#

#
def asmOps(s):
    s  = s.strip()
    sp = s.split(None, 3)
    #if(len(sp[0]) < 6):
    #    sp[0] = sp[0] + '\t'
    #
    l  = len(sp)
    if(l == 4):
        if(len(sp[1]) < 4):
            sp[1] = sp[1] + ' '
        #
        if(len(sp[2]) < 4):
            sp[2] = sp[2] + '  '
        #
        print("{0}\t{1} {2}\t;* {3}".format( sp[0], sp[1], sp[2], sp[3]))
    elif(l == 3):
        if(len(sp[1]) < 4):
            sp[1] = sp[1] + ' '
        #
        if(len(sp[2]) < 4):
            sp[2] = sp[2] + '  '
        #
        print("{0}\t{1} {2}\t;* ".format( sp[0], sp[1], sp[2]))
    else:
        # If 2
        #   LDA  #1
        print("1?:{0}".format(s))
    #
#

# 	RTS	*
# 	RTS	* Comment
# Oops
#       ASLB            ;* 
#STR1    ASLB BUFFER     ;* EMPTY BIT TO CARRY XXXXXXXX

def func2(s):
    s  = s.strip()
    sp = s.split(None, 1)
    l  = len(sp)

    if(l == 2):
        print("\t{0}\t\t;* {1}".format( sp[0], sp[1]))
    elif(l == 1):
        print("\t{0}\t\t;* ".format( sp[0]))
    else:
        print("2?:\t{0}\t\t;* {1} ({2})".format(s, l, sp[0]))
    #
#

# @2
# P:LOAD3 LDAB #$34 TAPE OFF CONSTANTS (3)
# 3:LOAD3 LDAB    * #$34 TAPE OFF CONSTANTS
# #3
# P:LOAD3 LDAB #$34 TAPE OFF CONSTANTS (3)
# 3:LOAD3 LDAB    * #$34 TAPE OFF CONSTANTS
def func3(s):
    s = s.strip()
    sp = s.split(None, 3)       # This causes issues
    l  = len(sp)
    if(l == 4):
        if(len(sp[1]) < 4):
            sp[1] = sp[1] + ' '
        #
        if(len(sp[2]) < 3):
            sp[2] = sp[2] + '\t'
        #
        print("{0}\t{1} {2}\t;* {3} XXXXXXXX".format( sp[0], sp[1], sp[2], sp[3]))
    elif(l == 3):
        if(len(sp[1]) < 4):
            sp[1] = sp[1] + ' '
        #
        if(len(sp[2]) < 4):
            sp[2] = sp[2] + '  '
        #
        print("{0}\t{1} {2}\t;*".format( sp[0], sp[1], sp[2]))
    elif(l == 2):
        #if(len(sp[0]) < 4):
        #    sp[0] = sp[0] + ' '
        #
        print("{0}\t{1}\t\t;* (LABEL/NM only?)".format( sp[0], sp[1]))
    else:
        print("3?:{0}\t;* {1} ({2})".format(s, l, sp[0]))
    #
#

#
# 	BRA	LOAD2	*
# 	BRA	LOAD2	* Branch always
def func4(s):
    s = s.strip()
    sp = s.split(None, 2)
    l  = len(sp)
    if(l == 3):
        if(len(sp[0]) < 4):
            sp[0] = sp[0] + ' '
        #
        if(len(sp[1]) < 4):
            sp[1] = sp[1] + ' '
        #
        print("\t{0} {1}\t;* {2}".format( sp[0], sp[1], sp[2]))
    elif(l == 2):
        if(len(sp[0]) < 4):
            sp[0] = sp[0] + ' '
        #
        if(len(sp[1]) < 4):
            sp[1] = sp[1] + ' '
        #
        print("\t{0} {1}\t;* ".format( sp[0], sp[1]))
    elif(l == 1):
        print("\t{0}\t\t;* ".format( sp[0]))
    else:
        print("4?:\t{0}\t\t;* {1} ({2})".format(s, l, sp[0]))
    #
#

# <LABEL> STAA VALUE <Comment...>
# <LABEL> STA A VALUE <Comment...>
def func5(s):
    s = s.strip()
    sp = s.split(None, 1)
    l  = len(sp)
    if(l == 2):
        print("{0}\t\t;* {1}".format( sp[0], sp[1]))
    elif(l == 1):
        print("{0}\t\t;* ".format( sp[0]))
    else:
        print("5?:{0}".format(s))
    #
#

# <LABEL> ASLA VALUE <Comment...>
# <LABEL> ASL A      <Comment...>
def func6(s):
    s = s.strip()
    sp = s.split(None, 1)
    l  = len(sp)
    if(l == 2):
        print("{0}\t\t;* {1}".format( sp[0], sp[1]))
    elif(l == 1):
        print("{0}\t\t;* ".format( sp[0]))
    else:
        print("5?:{0}".format(s))
    #
#

def comments(s):
    # Handle blank and lines that start with comments
    # line with line ending
    #print("# Comment")
    print(';{0}'.format(s), end = '')
#

def labels(s):
    # Handle labels (and equates)
    # Label OP VALUE Comment...
    #print("# Label")
    try:
        op = s.split()[1]

        # run the function
        if(op in OP):
            OP[op](s)
        else:
            func3(s)
        #
    except:
        print(s)
        #print("BOOM!")
        #print(traceback.format_exc())
        #print("{0}: {1}".format(ln, s))
    #
#

def instructions(s):
    # Eat the whitespace
    #print("# Instruction")
    s  = s.lstrip()
    nm = s.split()[0]
    nm = nm.upper()

    if(nm in NM):
        NM[nm](s)
    else:
        #print("P:\t" + line, end = '')
        func4(s)
    #
#

# -[ Main ]---------------------------------------------------------------------
filename = sys.argv[1];
# @FIXME: Still needs the Asm Instructions
# LABEL	LSRA
# LABEL LSRA		*
# LABEL ADDA #$30
# LABEL ADDA #$30	*
OP = {'RMB': asmOps,
      'EQU': asmOps,
      'FDB': asmOps,
      'FCB': asmOps,
        'FCC':  func,
        'OPT':  func,
        'PAG':  func,
        'NAM':  func,
        'NOOPT':func,
        'SPC':  func,
        'LIST': func,
        'TITLE':func,
        'PAGE': func,
        'ORG':  func4,
        'END':  func2,
        'TTL':  func,
      'x': asmOps
}

# No labels
# mnemonics
NM = {  'RMB':  func,
        'FDB':  func,
        'FCB':  func,
        'EQU':  func,
        'FCC':  func,
        'OPT':  func,
        'PAG':  func,
        'NAM':  func,
        'NOOPT':func,
        'SPC':  func,
        'LIST': func,
        'TITLE':func,
        'PAGE': func,
        'ORG':  func4,
        'END':  func2,
        'TTL':  func,
      'ABA':  func2,
      'ABX':  func2,
      'ADC':  func5,
      'ADCA': func2,
      'ADCB': func2,
      'ADD':  func5,
      'ADDA': func2,
      'ADDB': func2,
      'AND':  func5,
      'ANDA': func2,
      'ANDB': func2,
      'ASL':  func5,
      'ASLA': func2,
      'ASLB': func2,
      'ASR':  func6,
      'ASRA': func2,
      'ASRB': func2,
      'BIT':  func5,
      'BITA': func2,
      'BITB': func2,
      'CBA':  func2,
      'CLC':  func2,
      'CLI':  func2,
      'CLR':  func6,
      'CLRA': func2,
      'CLRB': func2,
      'CLV':  func2,
      'CMP':  func5,
      'CMPA': func2,
      'CMPB': func2,
      'COM':  func6,
      'COMA': func2,
      'COMB': func2,
      'DAA':  func2,
      'DEC':  func6,
      'DECA': func2,
      'DECB': func2,
      'DES':  func2,
      'DEX':  func2,
      'EOR':  func5,
      'EORA': func2,
      'EORB': func2,
      'INC':  func6,
      'INCA': func2,
      'INCB': func2,
      'INS':  func2,
      'INX':  func2,
      'LDA':  func5,
      'LDAA': func2,
      'LDAB': func2,
      'LSR':  func6,
      'LSRA': func2,
      'LSRB': func2,
      'NEG':  func6,
      'NEGA': func2,
      'NEGB': func2,
      'NOP':  func2,
      'ORA':  func5,
      'ORAA': func2,
      'ORAB': func2,
      'PSH':  func6,
      'PSHA': func2,
      'PSHB': func2,
      'PUL':  func6,
      'PULA': func2,
      'PULB': func2,
      'ROL':  func6,
      'ROLA': func2,
      'ROLB': func2,
      'ROR':  func6,
      'RORA': func2,
      'RORB': func2,
      'RTI':  func2,
      'RTS':  func2,
      'SBA':  func2,
      'SBC':  func5,
      'SBCA': func2,
      'SBCB': func2,
      'SEC':  func2,
      'SEI':  func2,
      'SEV':  func2,
      'STA':  func5,
      'STAA': func2,
      'STAB': func2,
      'SUB':  func5,
      'SUBA': func2,
      'SUBB': func2,
      'SWI':  func2,
      'TAB':  func2,
      'TAP':  func2,
      'TBA':  func2,
      'TPA':  func2,
      'TST':  func6,
      'TSTA': func2,
      'TSTB': func2,
      'TSX':  func2,
      'TXS':  func2,
      'WAI':  func2
}
# NM[idx](str)
try:
    with open(filename) as f:
        print(';*[ Start ]*********************************************************************')

        ln = 0
        while True:
            # Get next line from file
            line = f.readline()
            ln = ln + 1
  
            # if line is empty
            # end of file is reached
            if not line:
                print(';*[ Fini ]**********************************************************************')
                break
            #
            
            if line.isspace() or line == '\n':
                print(line)
                continue
            #

            # If the line starts with a ; print it out and skip to the next line
            if line.startswith(';'):
                print(line)
                continue
            #

            # The difference is that if line is an empty string, line[:1]
            # will evaluate to an empty string while line[0] will
            # raise an IndexError
            #
            #myRe  = re.compile(r"^\s+|^\s+\*")
            myRe  = re.compile(r"^\s*\*|^\s*\n")
            match = re.search(myRe, line)
            if match:
                # Handle blank and comment lines
                # Handle blank and lines that start with comments
                comments(line)
            elif(line[:1].isalpha()):
                # Handle labels (and equates)
                # Label OP VALUE Comment...
                labels(line)
            else:
                #print("### '" + line + "' ###")
                instructions(line)
            #
        #
    #
except FileNotFoundError:
    msg = "Sorry, the file "+ filename + "does not exist."
    print(msg) # Sorry, the file John.txt does not exist.
#

# =[ Fini ]=====================================================================
"""
      'PSHB': func2,
      'ASLA': func2,
      'ASLB': func2,
      'LSRA': func2,
      'LSRB': func2,
      'TAB':  func2,
      'ABA':  func2,
      'PULB': func2,
      'PSHA': func2,
      'PULA': func2,
      'INX':  func2,
      'DECA': func2,
      'DECB': func2,
      'DEX':  func2,
      'INCA': func2,
      'INCB': func2,
      'INX':  func2,
      'INS':  func2,
      'CLRA': func2,
      'CLRB': func2,
      'TSX':  func2,
      'TXS':  func2,

      'ADC':  func5,
      'ADD':  func5,
      'AND':  func5,
      'ASL':  func6,
      'ASR':  func6,
      'BIT':  func5,
      'CLR':  func6,
      'CMP':  func5,
      'COM':  func6,
      'DEC':  func6,
      'EOR':  func5,
      'INC':  func6,
      'LDA':  func5,
      'LSL':  func6, ???
      'LSR':  func6,
      'NEG':  func6,
      'ORA':  func5,
      'PSH':  func6,
      'PUL':  func6,
      'ROL':  func6,
      'ROR':  func6,
      'SBC':  func5,
      'STA':  func5,
      'SUB':  func5,
      'TST':  func6,
"""
