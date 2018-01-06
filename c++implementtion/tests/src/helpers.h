/*
 * helpers.h
 *
 * Helper methods
 *
 *  Created on: 30 Dec 2017
 *      Author: VinayVishnumurthy
 */

#ifndef HELPERS_H_
#define HELPERS_H_
#include <vector>
#include <iostream>
#include <cmath>
#include <string>
#include <fstream>

using namespace std;

vector<vector<float> > normalize(vector<vector<float> > grid);

vector<vector<float> > blur(vector<vector<float> > grid, float blurring);

bool close_enough(vector<vector<float> > g1, vector<vector<float> > g2);

bool close_enough(float v1, float v2);

vector<char> read_line(string s);

vector<vector<char> > read_map(string file_name);

vector<vector<float> > zeros(int height, int width);

#endif /* HELPERS_H_ */
