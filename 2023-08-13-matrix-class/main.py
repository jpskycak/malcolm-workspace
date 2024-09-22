from matrix import *

# TO DO
# - mutiply_row_by_scalar
# - add_multiples_of_rows
# - swap_rows
# - rref
# - inverse
# - eigenvectors/eigenvalues

X = Matrix([[-1, 0, 1, 1, 0, 0], [1, 1, 0, -1, -1, 0], [1, -2, 0, 4, -5, 0],
            [1, -2, 3, 0, 0, 0], [0, 0, 3, -4, 5, 0], [0, 1, 1, 0, -1, 0],
            [1, 1, 0, 0, 0, -1], [0, 0, 0, 1, 1, -1]])

for i in range(X.num_cols - 1):
  X.reduce_col(i)

X.show()

y = Matrix([[1], [2], [3], [4]])

#v = X.inverse()
#v.show()
#Test = calculus_calculator("+-+-+-+-+-")
#Test.get_term(2)
#print(Test.function)
