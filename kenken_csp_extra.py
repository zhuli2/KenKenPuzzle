'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2)
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''

from cspbase import *
import itertools

ADD      = 0
SUBTRACT = 1
DIVIDE   = 2
MULTIPLY = 3


def binary_ne_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    #pass
    n         	 = kenken_grid[0][0]
    domain    	 = [i for i in range(1, n+1)]
    csp 	  	 = CSP(" {}-KenKen".format(n), vars=[])
    var_array 	 = []    
    for i in range(n):
        var_array.append(list())

    #add variable objects to csp object
    for r_idx in range(n):
        for c_idx in range(n):
            new_var = Variable("KK{}{}".format(r_idx+1, c_idx+1), domain)
            csp.add_var(new_var)
            var_array[r_idx].append(new_var)

    cons = []
    #row constraints
    for i in range(n):
        for j in range(n):
            for k in range(len(var_array[i])):
                if k <= j:
                    continue
                var1 = var_array[i][j]
                var2 = var_array[i][k]
                con = Constraint("Cage(KK{}{},KK{}{})".format(i+1, j+1, i+1, k+1), [var1, var2])

                sat_tuples = []
                for t in itertools.product(var1.domain(), var2.domain()):
                    if t[0] != t[1]:
                        sat_tuples.append(t)

                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    #column constraints
    for i in range(n):
        for j in range(n):
            for k in range(len(var_array[i])):
                if k <= i:
                    continue
                var1 = var_array[i][j]
                var2 = var_array[k][j]
                con = Constraint("Cage(KK{}{},KK{}{})".format(i+1, j+1, k+1, j+1), [var1, var2])

                sat_tuples = []
                for t in itertools.product(var1.domain(), var2.domain()):
                    if t[0] != t[1]:
                        sat_tuples.append(t)

                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    for c in cons:
        csp.add_constraint(c)  
		
    return csp, var_array


def nary_ad_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    #pass

    n         	 = kenken_grid[0][0]
    domain    	 = [i for i in range(1, n+1)]
    csp 	  	 = CSP(" {}-KenKen".format(n), vars=[])
    var_array 	 = []    
    for i in range(n):
        var_array.append(list())

    for r_idx in range(n):
        for c_idx in range(n):
            new_var = Variable(name="KK{}{}".format(r_idx+1, c_idx+1), domain=domain)
            csp.add_var(new_var)
            var_array[r_idx].append(new_var)

    cons = []
    #row constraints
    for row in var_array:
        name  = "C("
        scope = []
        for var in row:
            name += var.name + ","
            scope.append(var)
        name = name[:-1] + ")"
        con  = Constraint(name, scope)
        sat_tuples = [t for t in itertools.permutations(list(range(1, n+1)))]
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    #column constraints
    for i in range(n):
        name  = "C("
        scope = []
        for j in range(n):
            name  += var_array[j][i].name + ","
            scope.append(var_array[j][i])
        name = name[:-1] + ")"
        con  = Constraint(name, scope)
        sat_tuples = [t for t in itertools.permutations(list(range(1, n+1)))]
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    for c in cons:
        csp.add_constraint(c)

    return csp, var_array


def kenken_csp_model(kenken_grid):
    # TODO! IMPLEMENT THIS!	
    n         	   = kenken_grid[0][0]
    csp, var_array = binary_ne_grid(kenken_grid)
    #csp, var_array = nary_ad_grid(kenken_grid)

    cons = []   
    for i in range(1, len(kenken_grid)):
        name  = "Cage("
        scope = []
        all_domains = [] 
        sat_tuples  = []
        if len(kenken_grid[i]) == 2:
            cell = kenken_grid[i][0]#=nn            
            target_val = kenken_grid[i][1]
            i = int(str(cell)[0]) - 1#row 
            j = int(str(cell)[1]) - 1#col            
            scope.append(var_array[i][j])
            con = Constraint(name + var_array[i][j].name + ")", scope)
            sat_tuples += [(target_val,)]
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)           
        elif len(kenken_grid[i]) > 2: 
            opr = kenken_grid[i][-1]
            target_val = kenken_grid[i][-2]
            for cell in kenken_grid[i][:-2]:
                i = int(str(cell)[0]) - 1#row
                j = int(str(cell)[1]) - 1#col
                name += var_array[i][j].name + ","
                scope.append(var_array[i][j])
                all_domains.append(var_array[i][j].domain())
            name = name[:-1] + ")"
            con = Constraint(name, scope)
            for t in itertools.product(*all_domains):
                if opr == 0:#add
                    result = t[0]
                    for i in range(1, len(t)):
                        result += t[i]
                    if result == target_val:
                        sat_tuples.append(t)
                elif opr == 1:#subtract
                    for p in itertools.permutations(t):
                        result = p[0]
                        for i in range(1, len(t)):
                            result -= p[i]
                        if result == target_val:
                            sat_tuples.append(t)
                            break
                elif opr == 2:#divide
                    for p in itertools.permutations(t):
                        result = p[0]
                        for i in range(1, len(t)):
                            result /= p[i]
                        if result == target_val:
                            sat_tuples.append(t)
                            break
                elif opr == 3:#multiply
                    result = t[0]
                    for i in range(1, len(t)):
                        result *= t[i]
                    if result == target_val:
                        sat_tuples.append(t)

            con.add_satisfying_tuples(sat_tuples)		 
            cons.append(con)
    
    for c in cons:
        csp.add_constraint(c)

    return csp, var_array


if __name__ == "__main__":
    from cspbase import *
    from propagators import *
    from heuristics import *
    #kenken_grid = [[3],[11,21,3,0],[12,22,2,1],[13,23,33,6,3],[31,32,5,0]]
    kenken_grid = [[4],[11,21,6,3],[12,13,3,0],[14,24,3,1],[22,23,7,0],[31,32,2,2],[33,43,3,1],[34,44,6,3],[41,42,7,0]]
    #kenken_grid = [[5], [11, 21, 4, 1], [12, 13, 2, 2], [14, 24, 1, 1], [15, 25, 1, 1], [22, 23, 9, 0], [31, 32, 3, 1], [33, 34, 44, 6, 3], [35, 45, 9, 0], [41, 51, 7, 0], [42, 43, 3, 1], [52, 53, 6, 3], [54, 55, 4, 1]]
    #kenken_grid = [[6],[11,12,13,2,2],[14,15,3,1],[16,26,36,11,0],[21,22,23,2,2],[24,25,34,35,40,3],[31,41,51,61,14,0],[32,33,42,43,52,53,3600,3],[44,54,64,120,3],[45,46,55,56,1,1],[62,63,5,1],[65,66,5,0]]
    #print(len(kenken_grid) - 1)
    csp, var_array = kenken_csp_model(kenken_grid)
    #print(len(csp.cons))
    #print(len(csp.vars))
    #for k in csp.vars_to_cons.keys():
    #    print(k.name, "====>")
    #    print(len(csp.vars_to_cons[k]))
    #    for c in csp.vars_to_cons[k]:
    #        print(c.name)
    #print(csp.vars)
    #print(var_array)
    #print(csp.vars_to_cons)
    #print(csp.cons[180].name)
    #print(csp.cons[180].sup_tuples)

    #print(csp.vars[0].domain(), csp.vars[0].cur_domain())
    #print(csp.get_all_unasgn_vars())
    solver = BT(csp)
    """
    solver.restore_all_variable_domains()

    solver.unasgn_vars = []
    for v in solver.csp.vars:
        #print(v)
        if not v.is_assigned():
            solver.unasgn_vars.append(v)
    print(len(solver.unasgn_vars))

    status, prunings = prop_FC(solver.csp)
    print(status)
    status = solver.bt_recurse(prop_FC, None, None, 1)
    print(status)
    print(len(solver.unasgn_vars))
    for v in csp.vars:
        print(v.is_assigned())
    """
    #solver.bt_search(prop_FC, ord_mrv)
    #solver.bt_search(prop_FC, ord_mrv, val_lcv)
    #solver.bt_search(prop_FC, ord_dh)
    #solver.bt_search(prop_FC, ord_dh, val_lcv)

    #solver.bt_search(prop_GAC, ord_mrv)
    #solver.bt_search(prop_GAC, ord_mrv, val_lcv)
    #solver.bt_search(prop_GAC, ord_dh)
    solver.bt_search(prop_GAC, ord_dh, val_lcv)

