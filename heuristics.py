'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy

def ord_dh(csp):
    # TODO! IMPLEMENT THIS!
    #pass
    unassigned_var    = csp.get_all_unasgn_vars()
    constraints       = csp.get_all_cons()
    var_in_constraint = dict()
    
    for uvar in unassigned_var:
        branching = 0
        for c in constraints:
            if uvar in c.get_scope():
                branching += 1
        var_in_constraint[uvar] = branching
    
    return max(var_in_constraint, key=var_in_constraint.get)    		


def ord_mrv(csp):
    # TODO! IMPLEMENT THIS!
    #pass
    unassigned_vars   = csp.get_all_unasgn_vars()
    curr_domain_size  = dict()
    
    for uv in unassigned_vars:
        curr_domain_size[uv] = uv.cur_domain_size()
    
    return min(curr_domain_size, key=curr_domain_size.get)
    

def val_lcv(csp, var):
    # TODO! IMPLEMENT THIS!
    #pass
    potential_values = dict()
    constraints      = csp.get_cons_with_var(var)
    
    for assigned_val in var.cur_domain():
        #try to assign a val to the var, causing change on remaining
        # unassigned variables 
        var.assign(assigned_val)
        count = 0
    	
        #now check remaining unassigned variables in each constraint
        # containing the given var to count the unconstrained values
        # assigned from the current domain of each unassigned variable.
        for c in constraints:
            for uv in c.get_unasgn_vars():
                for val in uv.cur_domain():
                    if c.has_support(uv, val) == False:#unconstrained legal value
                        count += 1
    					
        #undo current assignment for next iteration
        var.unassign()
        potential_values[assigned_val] = count
    
    #return a list of values from *least to most unconstrained*
    return sorted(potential_values, key=potential_values.get)
