expr 3 + 5
#returns 8

expr 5 % 3
#returns 2

expr 1 / 0
#returns the error message, expr: division by zero

#Illegal arithmetic operations not allowed.

expr 5 \* 3
#returns 15

#The multiplication operator must be escaped when used in an arithmetic expression with expr.

y=`expr $y + 1`
#Increment a variable, with the same effect as let y=y+1 and y=$(($y+1)). This is an example of arithmetic expansion.

z=`expr substr $string $position $length`
#Extract substring of $length characters, starting at $position.