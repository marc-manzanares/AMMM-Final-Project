/*********************************************
 * OPL 20.1.0.0 Model
 * Author: marcm
 * Creation Date: May 6, 2022 at 8:14:11 PM
 *********************************************/
main {
	// Store initial time
  	var start = new Date();
  	var startTime = start.getTime();
	
	// Set a file for output
  	var out = new IloOplOutputFile("solutions.txt");
      
	var src = new IloOplModelSource("project.template2.mod"); // load model
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	
	// load data files
	var data_files = new Array();
	data_files[0] = "project.1.dat";
	data_files[1] = "project.2.dat";
	data_files[2] = "project.3.dat";
	data_files[3] = "project.4.dat";
	data_files[4] = "project.5.dat";
	data_files[5] = "project.6.dat";
	data_files[6] = "project.7.dat";
	data_files[7] = "project.8.dat";
	data_files[8] = "project.9.dat";
	
	for (var i = 0; i <= 8; i++) {
	  	out.writeln("Solution #" + (i+1));
	  
	  	var model = new IloOplModel(def, cplex);
	  	var data = new IloOplDataSource(data_files[i]);

      	model.addDataSource(data);
      	model.generate();
    	
    	cplex.tilim=1800; // 30 mins
		cplex.epgap = 0.01; // GAP 1%
    	
    	if (cplex.solve()) {
			out.writeln ( "OBJECTIVE: " + cplex.getObjValue() );
			var prev = 0;
			for (var j = 1; j <= model.n-1; j++) {
				for (var k = 1; k <= model.n-1; k++) {
				  if (model.kjth_code[j][k] == 1) {
				    out.writeln(prev + " --> " + k);
				    prev = k;    
				  }
				}
			}
			out.writeln(prev + " --> " + 0);
		}
		else {
			out.writeln("No solution found");
		}
		model.end();
		data.end();
	}
	
	
	def.end();
	cplex.end();
	src.end();
	
	// Write execution time
  	var end = new Date();
  	var endTime = end.getTime();
  	writeln("Execution time: " + (endTime - startTime) + "ms");
};