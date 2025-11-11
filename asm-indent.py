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

def func1(s):
    print(";* Func1")
    asmOps(s)
#

def lAsmOps(s):
    pass
#

# FCC, FCB, RMB can all start without a LABEL
def asmOps(s):
    s  = s.strip()
    #print(";* asmOps: <{0}>".format(s))
    sp = s.split(None, 3)
    l  = len(sp)

    if(line[0] == ' '):
        print("\t{0}\t;*".format(s))
    elif(l == 4):
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
        #   SPC  1
        #   ORG $xxxx
        #   RMB  nnn
        print("\t{0}\t\t;* asmOps?".format(s))
    #
#

#        RTS
#        RTS	*
#        RTS	* Comment
#        ASLB            ;* 
#STR1    ASLB BUFFER     ;* EMPTY BIT TO CARRY XXXXXXXX
#        LDAA #2 SET FOR WRITE
#        STAA 0,X
#        LDAA #$FF SET FOR BINAIRY WRITE
#        STAA 59,X
#
def func2(s):
    s  = s.strip()
    sp = s.split(None, 1)
    l  = len(sp)

    ###
    ### @FIXME: Not handling STAA/LDAA (or LDAB, etc) properly
    ###
    if(l == 2):
        print("\t{0}\t\t;* {1} (l == 2)".format( sp[0], sp[1]))
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
#
def func6(s):
    s  = s.strip()
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
OP = {
    'END':  func2,
    'EQU': asmOps,
    'FCB': asmOps,
    'FCC':  func,
    'FDB': asmOps,
    'LIST': func,
    'NAM':  func,
    'NOOPT':func,
    'OPT':  func,
    'ORG':  func4,
    'PAG':  func,
    'PAGE': func,
    'RMB': asmOps,
    'SPC':  func,
    'TITLE':func,
    'TTL':  func,
    'x': asmOps
}

# No labels
# mnemonics
NM = {
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
    'CMP':  func1,
    'CMPA': func1,
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
    'END':  func2,
    'EOR':  func5,
    'EORA': func2,
    'EORB': func2,
    'EQU':  func,
    'FCB':  func,
    'FCC':  func,
    'FDB':  func,
    'INC':  func6,
    'INCA': func2,
    'INCB': func2,
    'INS':  func2,
    'INX':  func2,
    'LDA':  func5,
    'LDAA': func2,
    'LDAB': func2,
    'LIST': func,
    'LSR':  func6,
    'LSRA': func2,
    'LSRB': func2,
    'NAM':  func,
    'NEG':  func6,
    'NEGA': func2,
    'NEGB': func2,
    'NOOPT':func,
    'NOP':  func2,
    'OPT':  func,
    'ORA':  func5,
    'ORAA': func2,
    'ORAB': func2,
    'ORG':  func4,
    'PAG':  func,
    'PAGE': func,
    'PSH':  func6,
    'PSHA': func2,
    'PSHB': func2,
    'PUL':  func6,
    'PULA': func2,
    'PULB': func2,
    'RMB':  func,
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
    'SPC':  func,
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
    'TITLE':func,
    'TPA':  func2,
    'TST':  func6,
    'TSTA': func2,
    'TSTB': func2,
    'TSX':  func2,
    'TTL':  func,
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

            # Blank lines
            if line.isspace() or line == '\n':
                print(line)
                continue
            #

            # If the line starts with a ; print it out and skip to the next line
            if line.startswith(';'):
                print(line)
                continue
            #

            # If the line starts with a * convert to ;* line...
            if line.startswith('*'):
                comments(line)
                #print(";{0}".format(line))
                continue
            #

            # The difference is that if line is an empty string, line[:1]
            # will evaluate to an empty string while line[0] will
            # raise an IndexError
            #
            #yRe  = re.compile(r"^\s+|^\s+\*")
            #yRe  = re.compile(r"^\s*\*|^\s*\n")
            myRe  = re.compile(r"^[\t ].*")
            match = re.search(myRe, line)
            if match:
                #print("### '" + line + "' ###")
                instructions(line)
                # Handle blank and comment lines
                # Handle blank and lines that start with comments
                #comments(line)
            elif(line[:1].isalpha()):
                # Handle labels (and equates)
                # Label OP VALUE Comment...
                labels(line)
            else:
                print(";* ??? {0}: {1}".format(ln, line))
            #
        #
    #
except FileNotFoundError:
    msg = "Sorry, the file "+ filename + "does not exist."
    print(msg) # Sorry, the file John.txt does not exist.
#

# =[ Fini ]=====================================================================
"""
Problem with NAM, OPT, SPC, RMB (with no label),LDAA, STAA, etc.

A line is:
     <OP> [<values>] <comment>                  | @FIXME lines (user will need to fix)
     <OP> [<values>]                            | include,nam
     <OP>                                       |
    <LABEL> <OP> <VALUE> <Comment...>           | LABEL LDA A ,X Comment 
    <LABEL> <OP> <Comment...>                   | LABEL RTS Comment
     <OP> <VALUE> <Comment...>                  |       STA A ,X Comment
     <OP> <Comment...>                          |       CLR A Comment
     <OP>                                       |       NOP

Things like STA A or LDA B need to be converted to STAA and LDAB

- A Label always starts in Column 0
- There is always whitespace before an <OP>
- An <OP> can have {0,1}<VALUE>
- A <VALUE> can never have whitespace in it
- A <Comment...> always starts with whitespace

INC        ;* ERRTOT
should be
        INC  ERRTOT

Also

        CMPA            ;* #$D    |  CMPA #$D
        BEQ  NXTLQ      ;*        |  BEQ NXTLQ
        INX             ;*        |  INX
        CMPA            ;* #':    |  CMPA #':
        BEQ  CONTL      ;*        |  BEQ  CONTL
        LDAA            ;* #4     |  LDAA #4

"""
