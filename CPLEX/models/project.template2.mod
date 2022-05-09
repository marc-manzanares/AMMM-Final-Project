// PLEASE ONLY CHANGE THIS FILE WHERE INDICATED.

// Length of codes.
int m = ...;

// Number of codes.
int n = ...;

// Codes.
// Input should satisfy the following precondition:
// the 0-th code is n zeroes: 000..000
int S[0..n-1][0..m-1] = ...;

// Range of code indices, including code 000...000.
range N0 = 0..n-1;

// Range of code indices, excluding code 000...000.
range N1 = 1..n-1;

// Define here your decision variables and 
// any other auxiliary program variables you need.
// You can run an execute block if needed.

dvar boolean prev_next_code[i in N0, j in N0];
dvar boolean kjth_code[k in N1, j in N1];
int flips[i in N0, j in N0];

// Pre-processing
execute {
  // Calculate the 'digits to flip' matrix
  for (var i = 0; i <= n-1; i++) {
    for (var j = 0; j <= n-1; j++) {  
      var num_flips = 0;
      for (var k = 0; k <= m-1; k++) {
        if (j == 0 && i == 0) {
           flips[i][j] = 0;
        }
      	else {
      	  if (S[i][k] != S[j][k]) {
      	    num_flips++;
      	  }
      	}
      }
      flips[i][j] = num_flips;
    }
  }
}

minimize sum(i in N0, j in N0) flips[i,j] * prev_next_code[i,j]; // Write here the objective function.

subject to {

    // Write here the constraints.
    
    // Constraint 1: x0 is the opening code
    forall (j in N1)
      prev_next_code[0, j] == kjth_code[1, j];
    
    // Constraint 2: xn is again x0, the closing code
    forall (i in N1)
      prev_next_code[i, 0] == kjth_code[n-1, i];
    
    // Constraint 3
    forall (k in N1)
      sum (j in N1) kjth_code[k,j] == 1;
    
    // Constraint 4
    forall (j in N1)
      sum (k in N1) kjth_code[k,j] == 1;
      
    // Constraint 5
    forall (k in 1..n-2) 
    	forall(i in N1, j in N1)
      		kjth_code[k,i] + kjth_code[k+1,j] - prev_next_code[i,j] <= 1;

}

// You can run an execute block if needed.
