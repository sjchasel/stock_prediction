import numpy as np
import math
def goodness_of_fit(X, Y):
    xBar = np.mean(X)
    yBar = np.mean(Y)
    SSR = 0
    varX = 0
    varY = 0
    for i in range(0 , len(X)):
        diffXXBar = X[i] - xBar
        diffYYBar = Y[i] - yBar
        SSR += (diffXXBar * diffYYBar)
        varX +=  diffXXBar**2
        varY += diffYYBar**2
    
    SST = math.sqrt(varX * varY)
    return (SSR / SST)**2

def get_rr(x, y, n=73):
    def partition(ls, size):
        return [ls[i:i+size] for i in range(0, len(ls), size)]
    rr = 0
    datal = partition(y, n)
    predl = partition(x, n)
    for i in range(len(datal)):
        dataa = datal[i]
        predd = predl[i]
        rr += goodness_of_fit(predd, dataa)
    print(rr/len(datal))