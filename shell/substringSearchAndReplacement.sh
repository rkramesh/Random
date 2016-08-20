stringZ=abcABC123ABCabc

echo ${stringZ/abc/xyz}           # xyzABC123ABCabc
                                  # Replaces first match of 'abc' with 'xyz'.

echo ${stringZ//abc/xyz}          # xyzABC123ABCxyz
                                  # Replaces all matches of 'abc' with # 'xyz'.