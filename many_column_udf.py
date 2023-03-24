import sys

for line in sys.stdin:
    line=line.strip("\n\r")
    country,order_num,quantity = line.split("\t")
    quantity=int(quantity)
    quantity=quantity*1000
    result='\t'.join([country,order_num,str(quantity)])
    print(result)