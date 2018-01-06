/*
 * localizer.h
 *
 * Header for localizer functions
 *
 *  Created on: 30 Dec 2017
 *      Author: VinayVishnumurthy
 */

#ifndef LOCALIZER_H_
#define LOCALIZER_H_
#include <iostream>
#include <stdlib.h>
#include <vector>

using namespace std;

//initialize the beliefs
vector<vector<float> > initialize_beliefs(vector<vector<char> > grid);

//sense method
vector<vector<float> > sense(char color, vector<vector<char> > grid,
		vector<vector<float> > beliefs, float p_hit, float p_miss);

//move method
vector<vector<float> > move(int dy, int dx, vector<vector<float> > beliefs,
		float blurring);

#endif /* LOCALIZER_H_ */
