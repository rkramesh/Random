echo "$uninitialized"                                # (blank line)
let "uninitialized += 5"                             # Add 5 to it.
echo "$uninitialized"                                # 5

#  Conclusion:
#  An uninitialized variable has no value, however
#+ it acts as if it were 0 in an arithmetic operation.
#  This is undocumented (and probably non-portable) behavior.