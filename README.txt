# DFA-NFA

Multiple python programs that perform different operations on DFAs and NFAs:
  - Check if a given DFA/NFA is valid
  - Check if a given word is accepted by a given DFA/NFA
  - Minimize a DFA
  - Convert a NFA to a DFA
  
The structure of a given DFA/NFA input file:

#
#  comment   lines  (skip them)
#
Sigma:
  letter 1 letter 2
  . . .
End
#
#  comment   lines ( skip them )
#
States:
  state1 
  state 2 
  state 3, F
  . . .
  stateK, S
  . . .
End
#
#  comment lines ( skip them )
#
Transitions:
  state X, letter Y, state Z
  state X, letter Y, state Z
  . . .
End
