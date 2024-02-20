#include "cell.h"
void cell::init(double t,...) {
//The 'parameters' variable contains the parameters transferred from the editor.
va_list parameters;
va_start(parameters,t);

// First, capture the parameters from every cell.
char* fvar = va_arg(parameters, char*);
isAlive = getScilabVar(fvar);
fvar = va_arg(parameters, char*);
maxNeighbors = getScilabVar(fvar);
name = va_arg(parameters, char*);

// Initialize the neighbors of each cell with a distinguishable number.
for (int i = 0; i < NEIGHBORS_AMOUNT; i++) {
	neighbors[i] = -1;
}

// Initialize the neighbors updated counter for each cell.
neighborsUpdated = 0;

// Print the initial state.
printLog("%f, %s, %f\n", t, name, isAlive);

// Set transition_time to sigma.
sigma = TRANSITION_TIME;
}
double cell::ta(double t) {
//This function returns a double.
return sigma;
}
void cell::dint(double t) {
sigma = TRANSITION_TIME;
}
void cell::dext(Event x, double t) {
// Update every output recieved in the corresponding port.
double* xv = (double*) x.value;
neighbors[x.port] = xv[0];

// We add the variable according to the cell that called an output.
neighborsUpdated++;

// Once that every cell asociated to the current cell, the update to the current state for the cell begins.
if (neighborsUpdated == maxNeighbors) {	
	
	// First, count every alive cell between the neighbors.
	int livenessCounter = 0;
	for (int i = 0; i < NEIGHBORS_AMOUNT; i++) {
		if (neighbors[i] == 1) {
			livenessCounter++;
		}
	}

	// The state changes from alive to dead, vice versa, or else it remains the same.
	// For change the state, this conditions are to be considered.
	if (isAlive && (livenessCounter < A || livenessCounter > B)) {
		isAlive = 0;	
	} else if (!isAlive && livenessCounter == BIRTH) {
		isAlive = 1;
	}

	// Only print when a change can occur (when all neighbors of the current cell generates an output).
	printLog("%f, %s, %f\n", t, name, isAlive);

	// The counter is reseted.	
	neighborsUpdated = 0;
}

// Update the sigma for the cell, so time can actually advance.
sigma = sigma - e;




}
Event cell::lambda(double t) {
// Return the liveness state of the current cell.
return Event(&isAlive, 0);
}
void cell::exit() {
//Code executed at the end of the simulation.

}
