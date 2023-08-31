def calculateSalary(fixedpay,IT,PF,ug, pg,oth,is_teaching: bool = True):
    if is_teaching:
        ug= ug * 550
        pg= pg * 750        
        ded = IT +PF + oth             
        total = fixedpay -ded  + ug + pg 
        
    else:
        ded2 = (IT+PF+oth)/100* fixedpay
        total = fixedpay - ded2 

   
    net_amt = total 
    return net_amt    
