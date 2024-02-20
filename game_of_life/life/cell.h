//CPP:life/cell.cpp
#if !defined cell_h
#define cell_h

#include "simulator.h"
#include "event.h"
#include "stdarg.h"

#include "life/constants.h"


class cell: public Simulator { 
// Declare the state,
// output variables
// and parameters

// parameters
double isAlive, maxNeighbors;
char *name;


// state
int neighbors[NEIGHBORS_AMOUNT];
double neighborsUpdated;
double sigma;


public:
	cell(const char *n): Simulator(n) {};
	void init(double, ...);
	double ta(double t);
	void dint(double);
	void dext(Event , double );
	Event lambda(double);
	void exit();
};
#endif
