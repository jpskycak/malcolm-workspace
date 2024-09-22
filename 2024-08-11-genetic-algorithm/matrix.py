import random

class Matrix:

  def __init__(self, rows):
    self.rows = rows
    self.num_rows = len(self.rows)
    self.num_cols = len(self.rows[0])

  def show(self):
    for row in self.rows:
      print(row)

  def scalar_mult(self, scalar):
    new_rows = []

    for row in self.rows:
      new_row = []

      for element in row:
        new_element = element * scalar
        new_row.append(new_element)

      new_rows.append(new_row)

    scaled_matrix = Matrix(new_rows)
    return scaled_matrix

  def is_square(self):
    return self.num_rows == self.num_cols

  def get_sub_matrix(self, row_index, col_index):
    sub_matrix_rows = []

    for r in range(self.num_rows):
      row = self.rows[r]
      new_row = []

      for c in range(self.num_cols):
        if c != col_index:
          new_row.append(row[c])

      if r != row_index:
        sub_matrix_rows.append(new_row)

    sub_matrix = Matrix(sub_matrix_rows)
    return sub_matrix

  def det(self):
    if self.is_square():
      if self.num_rows == 2:
        return self.rows[0][0] * self.rows[1][1] - self.rows[1][0] * self.rows[
          0][1]

      sign_tracker = 1
      det_tracker = 0

      for i in range(self.num_rows):
        sub_matrix = self.get_sub_matrix(0, i)
        signed_element = sign_tracker * self.rows[0][i]
        det_tracker += sub_matrix.det() * signed_element
        sign_tracker *= -1
      return det_tracker

  def dot(self, v1, v2):
    if len(v1) != len(v2):
      raise Exception('Dimensions not compatible')

    dot_product = 0
    for i in range(len(v1)):
      dot_product += v1[i] * v2[i]
    return dot_product

  def column(self, col_index):
    col = []
    for i in range(self.num_rows):
      col.append(self.rows[i][col_index])
    return col
  
  def mult(self, other_matrix):
    if self.num_cols != other_matrix.num_rows:
      raise Exception(f'Dimensions not compatible: {self.num_cols} cols vs {other_matrix.num_rows} rows')
      
    rows = []
    for i in range(self.num_rows):
      new_row = []
      
      for j in range(other_matrix.num_cols):
        row = self.rows[i]
        col = other_matrix.column(j)
        new_value = self.dot(row, col)
        new_row.append(new_value)
        
      rows.append(new_row)
      
    product = Matrix(rows)
    return product

  def mult_row_by_scalar(self, row_index, scalar):
    row = self.rows[row_index]
    for i in range(len(row)):
      row[i] *= scalar
    self.rows[row_index] = row

  def add_row(self, row_index_same, row_index_change):
    row_same = self.rows[row_index_same]
    row_change = self.rows[row_index_change]

    for i in range(len(row_same)):
      row_change[i] += row_same[i]

  def add_mult_of_row(self, row_index_same, row_index_change, scalar):
    self.mult_row_by_scalar(row_index_same, scalar)
    self.add_row(row_index_same, row_index_change)
    self.mult_row_by_scalar(row_index_same, 1/scalar)

  def fix_diagonal_zero(self, col_index):
    if col_index == self.num_rows - 1:
      raise Exception('No Inverse')
      
    for i in range(col_index + 1,self.num_rows):
      
      if self.rows[i][col_index] != 0:
        self.add_mult_of_row(i, col_index, 1)
        break
        
    diagonal_entry = self.rows[col_index][col_index]
    
    if diagonal_entry == 0:
      raise Exception('No Inverse')
      
    return diagonal_entry

  def reduce_col(self, col_index):
    
    diagonal_entry = self.rows[col_index][col_index]
    
    if diagonal_entry == 0:
      diagonal_entry = self.fix_diagonal_zero(col_index)
      
    self.mult_row_by_scalar(col_index, 1/diagonal_entry)
    
    for i in range(self.num_rows):
      
      if i != col_index:
        entry_to_be_zeroed = self.rows[i][col_index]
        
        if entry_to_be_zeroed != 0:
          self.add_mult_of_row(col_index, i, -1*entry_to_be_zeroed)

  def swap_rows(self, row_index1, row_index2):
    # I don't think we ever use this
    row1 = self.rows[row_index1]
    row2 = self.rows[row_index2]
    self.rows[row_index1] = row2
    self.rows[row_index2] = row1
  
  def inverse(self):
    if not self.is_square:
      raise Exception('Not Square')

    inverse = self
      
    for r in range(inverse.num_rows):
      for c in range(inverse.num_rows):
        
        if r == c:
          inverse.rows[r].append(1)
        else:
          inverse.rows[r].append(0)

    for c in range(inverse.num_cols):
      inverse.reduce_col(c)
  
    for r in range(inverse.num_rows):
      for c in range(inverse.num_rows):
        del inverse.rows[r][0]

    return inverse

  def transpose(self):
    new_rows = []
    for c in range(self.num_cols):
      new_row = []
      for r in range(self.num_rows):
        new_row.append(self.rows[r][c])
      new_rows.append(new_row)

    new_matrix = Matrix(new_rows)
    return new_matrix

  def pseudo_inverse(self):
    square_matrix = self.transpose().mult(self)
    inv_square_matrix = square_matrix.inverse()
    pseudo_inverse = inv_square_matrix.mult(self.transpose())
    return pseudo_inverse

  def best_fit_solution(self, right_hand_matrix):
    # self is the coefficient matrix
    pseudo_inverse = self.pseudo_inverse()
    variable_matrix = pseudo_inverse.mult(right_hand_matrix)
    return variable_matrix


  def make_random_copy(self, variance):
    new_matrix = []
    for row in self.rows:
      new_row = []
      for weight in row:
        new_weight = weight + (random.random() - 0.5) * variance
        new_row.append(new_weight)
      new_matrix.append(new_row)
    new_matrix = Matrix(new_matrix)

    return new_matrix