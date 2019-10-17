from scipy.optimize import linear_sum_assignment
import numpy as np
'''
This function can also solve a generalization of the classic assignment problem where the cost matrix is rectangular. 
If it has more rows than columns, then not every row needs to be assigned to a column, and vice versa.(反之亦然)
#即如果行多则列的每个顶点都会匹配，如果列多则行的每个顶点都会匹配
#我们需要的是最大权值和匹配
'''
#cost = np.array([[4.5, 1, 3], [2, 0, 5], [3, 2, 2],[9,0,1]]) * -1#
cost = np.array([[1,2,3],[3,4,5]])
row_ind, col_ind = linear_sum_assignment(cost)
print(row_ind)
print(col_ind)
print(cost[row_ind, col_ind].sum()*-1)#因原算法是最小权值匹配所以要乘-1