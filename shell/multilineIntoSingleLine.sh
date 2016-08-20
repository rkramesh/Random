file: Split_22_05_2013
abc
def
ghi
jkl
mno


sed -n 's/[0-3]//;s/ //;p' Split_22_05_2013 | awk -v ORS= '{print $0" ";if(NR%4==0){print "\n"}}'