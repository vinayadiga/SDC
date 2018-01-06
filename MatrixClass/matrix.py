import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I
    
def dot_product(vector_one, vector_two):
        dot_prod = 0
        for i in range(len(vector_one)):
            dot_prod += vector_one[i] * vector_two[i]
        return dot_prod
    
class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices larger than 2x2.")
        if self.w > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices larger than 2x2.")
        if self.h == 1 and self.w == 1:
            return self.g[0][0]
        det_i = self.g[0][0]*self.g[1][1] - self.g[0][1]*self.g[1][0]
        if det_i == 0:
            raise(ValueError, "Cannot calculate determinant if the denominator is 0")
        det = 1.0/(self.g[0][0]*self.g[1][1] - self.g[0][1]*self.g[1][0])
        return det

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        trace = 0
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        if self.h == 1 and self.w == 1:
            trace = self.g[0][0]
            return trace
        for i in range(len(self.g)):
            for j in range(len(self.g[i])):
                if i == j:
                    trace += self.g[i][j]
        return trace
        
    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        if self.w > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        
        inv = zeroes(self.h, self.w)        

        if len(self.g) == 1 and len(self.g[0]) == 1:            
            inv[0][0] = (1.0/self.g[0][0])
            return inv
        determinant_value = self.determinant()
        
        inv = Matrix([
            [determinant_value*float(self.g[1][1]), -(float(self.g[0][1])*determinant_value)],
            [-(determinant_value*float(self.g[1][0])), determinant_value*float(self.g[0][0])]
        ])
        return inv

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        matrix_transpose = zeroes(self.w, self.h)
        rows = self.h
        cols = self.w
        for i in range(cols):
            col = []
            for j in range(rows):
                matrix_transpose[i][j] = self.g[j][i]
   
        return matrix_transpose

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        # initialize matrix to hold the results
        matrixSum = zeroes(self.h, self.w)
        # matrix to hold a row for appending sums of each element
        row = []
        for i in range(len(self.g)):
            for j in range(len(other[i])):
                matrixSum[i][j] = self.g[i][j] + other[i][j]
    
        return matrixSum

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        neg_Matrix = zeroes(self.h, self.w)
        for i in range(len(self.g)):
            for j in range(len(self.g[i])):
                if self.g[i][j] != 0.0:
                    neg_Matrix[i][j] = -float(self.g[i][j])
                else:
                    neg_Matrix[i][j] = float(self.g[i][j])
        
        return neg_Matrix
        

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be subtracted if the dimensions are the same") 
        # initialize matrix to hold the results
        matrixSub = zeroes(self.h, self.w)
        # matrix to hold a row for appending sums of each element
        row = []
        for i in range(len(self.g)):
            for j in range(len(other[i])):
                matrixSub[i][j] = self.g[i][j] - other[i][j]
    
        return matrixSub

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        if self.w != other.h:
            raise(ValueError, "Matrices can only be multiple if the width(m1) and height(m2) are the same") 
        product = zeroes(self.h, other.w)
        matrixB_T = other.T()
        dot_prod = 0
        for i in range(len(self.g)):
            for j in range(matrixB_T.h):          
                dot_prod = dot_product(self.g[i], matrixB_T[j])
                product[i][j] = dot_prod

        return product
        

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
            rmul_value = []
            rmul_value_row = []
            for i in range(len(self.g)):
                for j in range(len(self.g[i])):
                    rmul_value_row.append(other*float(self.g[i][j]))
                rmul_value.append(rmul_value_row)
                rmul_value_row = []
            rmul_Matrix = Matrix(rmul_value)
            return rmul_Matrix
        return None