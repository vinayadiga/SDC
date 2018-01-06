/*
 * simulate.h
 *
 *  Created on: 30 Dec 2017
 *      Author: VinayVishnumurthy
 */

#ifndef SIMULATE_H_
#define SIMULATE_H_
#include <iostream>
#include <vector>
using namespace std;

// class header file
class Simulation {
private:
	vector<char> get_colors();
public:
	vector<vector<char> > grid;
	vector<vector<float> > beliefs;

	float blur, p_hit, p_miss, incorrect_sense_prob;

	int height, width, num_colors;

	std::vector<int> true_pose;
	std::vector<int> prev_pose;

	vector<char> colors;
	Simulation(vector<vector<char> >, float, float, vector<int>);
};

#endif /* SIMULATE_H_ */
