import math
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as pp

# A class to represent matrix basis vectors and multiply them

def basis_vector_class(dim):
    # Build a pair from int
    def pair(k):
        if k!=None and k>=0:
            return (k/dim, k%dim)
        else:
            return (None, None)
    # and back
    def unpair(i,j):
        return dim*i+j
    # Define the class
    class E(object):
        # The constructor
        def __init__(self, i, j=None):
            if i!=None:
                if j!=None:
                    self.i = i
                    self.j = j
                    self.k = unpair(i,j)
                else:
                    self.k = i
                    self.i, self.j = pair(self.k)
            else:
                self.i = None
                self.j = None
                self.k = None
        # A multiplication
        def __mul__(self, e):
            if self.i!=None and e.j!=None and self.j==e.i:
                return E(self.i, e.j)
            else:
                return E(None, None)
        def mat(self):
            result = np.zeros((dim,dim))
            if self.k!=None:
                result[self.i, self.j] = 1
            return result
        def vec(self):
            result = np.zeros(dim*dim)
            if self.k!=None:
                result[self.k] = 1
            return result
        def __repr__(self):
            if self.k!=None:
                return 'e_{},{}'.format(self.i, self.j)
            else:
                return '0'
    # Returns the class
    return E

# Build tha right basis
def build_basis(dim):
    E = basis_vector_class(dim)
    # Build the product tensor
    T = np.zeros((dim**2,dim**2,dim**2))
    for i in xrange(dim**2):
        for j in xrange(dim**2):
            k = (E(i)*E(j)).k
            if k!=None:
                T[i,j,k] = 1
    # A utility to get a view
    def mat(T, n):
        N = len(T.shape)
        d = T.shape[n]
        D = np.prod(T.shape)/d
        M = T.transpose([(i+n)%N for i in xrange(N)]).reshape(d, D)
        # a test
        # pp.imshow(np.dot(M, M.T)).set_interpolation('nearest')
        pp.imshow(M).set_interpolation('nearest')
        pp.show()
        return la.eigh(np.dot(M,M.T))[1]
    # We return the projections
    return mat(T,0), mat(T,1), mat(T,2)

# Some tests
N = 2
E = basis_vector_class(N)

print build_basis(N)

# pp.imshow(A).set_interpolation('nearest')
# pp.show()