/*********************************************
 * OPL 20.1.0.0 Model
 * Author: marcm
 * Creation Date: May 6, 2022 at 8:14:11 PM
 *********************************************/
main {
	// Store initial time
  	var start = new Date();
  	var startTime = start.getTime();
	
	    
	var src = new IloOplModelSource("project.template2.mod"); // load model
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	var model = new IloOplModel(def, cplex);
	var data = new IloOplDataSource("project.1.dat"); // load instance
	model.addDataSource(data);
	model.generate();
	
	cplex.tilim=1800; // 30 mins
	cplex.epgap = 0.01; // GAP 1%
	
	if (cplex.solve()) {
		writeln ( "OBJECTIVE: " + cplex.getObjValue() );
		var prev = 0;
		for (var i = 1; i <= model.n-1; i++) {
			for (var j = 1; j <= model.n-1; j++) {
			  if (model.kjth_code[i][j] == 1) {
			    writeln(prev + " --> " + j);
			    prev = j;    
			  }
			}
		}
		writeln(prev + " --> " + 0);
	}
	else {
		writeln("No solution found");
	}
	
	model.end();
	data.end();
	def.end();
	cplex.end();
	src.end();
	
	// Write execution time
  	var end = new Date();
  	var endTime = end.getTime();
  	writeln("Execution time: " + (endTime - startTime) + "ms");
};