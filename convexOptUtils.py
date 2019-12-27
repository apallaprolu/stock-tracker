# Utilities for mean-variance portfolio convex optimization

import numpy as np
import pandas as pd
from cvxopt import matrix, solvers
import matplotlib.pyplot as plt

def getReturns(quoteTable):
    rTable = []
    vecRep = quoteTable.values.tolist()
    shiftVecRep = quoteTable.values.tolist()
    del shiftVecRep[0]
    for i in range(len(shiftVecRep)):
        quoteVec = np.array(shiftVecRep[i][1:])
        previousQuoteVec = np.array(vecRep[i][1:])
        diffVec = [shiftVecRep[i][0]] + list(quoteVec - previousQuoteVec)
        rTable.append(diffVec)
    
    returnsTable = pd.DataFrame(rTable, columns=quoteTable.columns)
    return returnsTable

def getMeanCov(returnsTable):
    desc = returnsTable.describe()
    mVector = []
    for i in desc.columns.tolist():
        mVector.append(desc[i]['mean'])
    return (np.array(mVector), np.cov(np.array(returnsTable[[x for x in returnsTable.columns if x != 'DATE']]).T))


def getPortfolio(mVector, covMatrix, mode=0):
    # Mode 0: Minimize risk and maximize return
    # Mode 1: Minimize risk exclusively
    # Mode 2: Maximize return exclusively

    # Cost function is w^T(Cov)w - w^T(Mean)
    # We are solving 1/2w^T(Cov)w + (Mean)^Tw
    # Subject to Gw <= H and Aw = b
    # Constraints on w are w >= 0 and w < 1 and sum(w) = 1

    if mode == 0:
        P = matrix(list(map(lambda x: list(x), list(covMatrix * 2.0))))
        q = matrix(list(map(lambda x: x * -1.0, list(mVector))))
    elif mode == 1:
        P = matrix(list(map(lambda x: list(x), list(covMatrix * 2.0))))
        q = matrix(list(np.zeros(len(mVector))))
    elif mode == 2:
        P = matrix(list(map(lambda x: list(x), list(np.zeros((len(mVector), len(mVector)))))))
        q = matrix(list(map(lambda x: x * -1.0, list(mVector))))

    G = []
    H = []
    for k in range(len(mVector)):
        tmp = [0]*(2*len(mVector)) # w_i >= 0 and w_i < 1 makes it two constraints per asset.
        tmp[2*k] = -1.0 # 
        tmp[2*k + 1] = 1.0
        G.append(tmp)
    
    for k in range(2*len(mVector)):
        if k % 2 == 0:
            H.append(0.0)
        else:
            H.append(1.0)

    H = matrix(H)
    G = matrix(G)

    A = matrix([[1.0]]*len(mVector))
    b = matrix(1.0)

    sol = solvers.qp(P, q, G, H, A, b)

    return list(map(lambda x: round(x, 4), list(sol['x'])))



def plotMarkowitz(N_iter, mean, cov):
    # Monte-carlo generation of the Markowitz-Pareto boundary.
    # Will return the statistical risk averse and maximum return portfolio.
    stoch = np.random.rand(N_iter, len(mean))
    stoch = stoch/stoch.sum(axis=1)[:,None].tolist()

    exp_return = []
    exp_volatility = []
    wvec = []

    for i in stoch:
        exp_return.append(np.dot(i, mean))
        exp_volatility.append(np.sqrt(np.dot(i, np.dot(cov, np.transpose(i)))))
        wvec.append(i)

    plt.scatter(exp_volatility, exp_return)
    plt.savefig("MarkowitzPareto.png")

    riskAversePortfolio = stoch[exp_volatility.index(min(exp_volatility))]
    maxReturnPortfolio = stoch[exp_return.index(max(exp_return))]

    return riskAversePortfolio, maxReturnPortfolio 


