#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define pi 2*acos(0)
double Four_Link_Type(double Len[],int);
double Rotational_Range(double Len[]);
double Position_Analysis(double Len[],int,double);
double Angular_Velocity_Analysis(double Len[], double arg[],double);

int main()
{
	using namespace std;

	/* 請使用者輸入四連桿機構各桿件長度 */
	double Link[4];
	int i;
	for (i = 0; i < 4; i++) {
		cout << "[Length of Link]: " << i+1 << endl;
		cin >> Link[i];
	}


	/* 選擇機構型態 */
	int configuration;
	cout << "[Configuration] [ Open type ---> 0 or Crossed type ---> 1 ]: ";
	cin >> configuration;
	

	/* 輸入耦點位置的兩個參數 */
	double Lp;
	double beta;
	cout << "[Length of Lp]:" << endl;
	cin >> Lp;
	cout << "[Angle of Lp]:" << endl;
	cin >> beta;


	/* 顯示輸出桿件可運動角度範圍 */
	double Len[4] = { Link[0],Link[1],Link[2],Link[3] };
	double arg_2p;
	Four_Link_Type(Len,4);
	arg_2p=Rotational_Range(Len);
	printf("[Rotation Range]: %f\n", arg_2p);
	
	
	/* 請使用者輸入 Input Link 初始角度及初始角速度 */
	double deg_2;	/＊宣告一變數(非矩陣，存取使用者輸入值) ＊/
	double omega_2;
	cout << "[Initial Angle of Input Link]: " << endl;
	cin >> deg_2;
	cout << "[Initial Angular Velocity of Input Link]:" << endl;
	cin >> omega_2;

	cout << "arg_2p= " << arg_2p << endl;
	cout << "2*(pi-arg_2p)= " << 2 * (pi - arg_2p) << endl;


	/* 分析位置即角速度 */
	double arg_2 = deg_2 * pi / 180;
	while (arg_2 > -arg_2p && arg_2 < arg_2p) {
		arg_2 = arg_2 + pi / 36;
		double arg_4;
		arg_4 = Position_Analysis(Len, configuration, arg_2);
		/*cout << "Position step: " << arg_2;*/

		double arg[2] = { arg_2,arg_4 };
		double omega_4;
		omega_4 = Angular_Velocity_Analysis(Len, arg, omega_2);
		/*cout << " Angular Velocity step: " << omega_4 << endl;*/
	}
	while (arg_2 > arg_2p && arg_2 < 2 * (pi - arg_2p)) {
		arg_2 = arg_2 + pi / 36;
		double arg_4;
		arg_4 = Position_Analysis(Len, configuration, arg_2);
		cout << "Position step: " << arg_2;

		double arg[2] = { arg_2,arg_4 };
		double omega_4;
		omega_4 = Angular_Velocity_Analysis(Len, arg, omega_2);
		cout << " Angular Velocity step: " << omega_4 << endl;
	}
	return 0;
}

double Four_Link_Type(double Len[],int num) {
	using namespace std;
	int i, j;
	double L, S;
	L = 0;
	S = 10001;
	for (i = 0; i < num; i++) {
		if (Len[i] > L) {
			L = Len[i];
		}
	}
	for (j = 0; j < num; j++) {
		if (Len[j] < S) {
			S = Len[j];
		}
	}
	double LT;
	int k;
	LT = 0;
	for (k = 0; k < num; k++) {
		LT = LT + Len[k];
	}
	if (L + S < LT - L - S && (S == Len[1] || S == Len[3])) {
		cout << "[Crank and Rocker]" << endl;
	}
	else if (L + S < LT - L - S && S == Len[0]) {
		cout << "[Double Crank (Drag Linkage)]" << endl;
	}
	else if (L + S == LT - L - S) {
		cout << "[Folding Linkage]" << endl;
	}
	else if (L + S > LT - L - S) {
		cout << "[Double Rocker of Second Kind (Triple Rocker)]" << endl;
	}
	cout << "L: " << L << " S:" << S << endl;
	return L + S;
}
double Rotational_Range(double Len[]) {
	double arg_2p;
	if (Len[0] + Len[1] <= Len[2] + Len[3] && abs(Len[0] - Len[1]) >= abs(Len[2] - Len[3])) {
		arg_2p = 360.0;
		printf("[Crank Rotate Range]: %f\n",arg_2p);
		return arg_2p;
	}
	else if (Len[0] + Len[1] > Len[2] + Len[4] && abs(Len[0] - Len[1]) >= abs(Len[2] - Len[3])) {
		arg_2p = acos((pow(Len[0], 2) + pow(Len[1], 2) - (Len[2] + Len[3]) * (Len[2] + Len[3])) / (2 * Len[0] + Len[1]));
		printf("[Half Range of Internal Rotation]: %f\n", arg_2p);
		return arg_2p;
	}
	else if (Len[0] + Len[1] <= Len[2] + Len[3] && abs(Len[0] - Len[1]) < abs(Len[2] - Len[3])) {
		arg_2p = acos((pow(Len[0], 2) + pow(Len[1], 2) - (Len[2] - Len[3]) * (Len[2] - Len[3])) / (2 * Len[0] * Len[1]));
		printf("[Start Angle of External Rotation]: %f\n", arg_2p);
		return arg_2p;
	}
	else {
		double gama_min;
		double gama_max;
		gama_min = (pow(Len[3], 2) + pow(Len[2], 2) - (Len[0] - Len[1]) * (Len[0] - Len[1])) / (2 * Len[3] * Len[2]);
		gama_max = (pow(Len[3], 2) + pow(Len[2], 2) - (Len[1] + Len[0]) * (Len[1] + Len[0])) / (2 * Len[3] * Len[2]);
		printf("gama_min: %f\n", gama_min);
		printf("gama_max: %f\n", gama_max);
	}
}
double Position_Analysis(double Len[],int configuration,double arg_2) {
	using namespace std;
	double t = tan(arg_2 / 2);
	/*cout << "arg_2: " << arg_2 << " t: " << t << endl;*/

	double A, B, C, D;
	double arg_4;
	arg_4 = 0.0;
	double a1, a2, c1, c2;
	a1 = Len[0] - Len[1] - Len[3];
	a2 = Len[0] + Len[1] - Len[3];
	c1 = Len[0] - Len[1] + Len[3];
	c2 = Len[0] + Len[1] + Len[3];
	A = (pow(a1, 2) - pow(Len[2], 2)) + (pow(a2, 2) - pow(Len[2], 2)) * t * t;
	B = 0 - 8 * Len[1] * Len[3] * t;
	C = (pow(c1, 2) - pow(Len[2], 2)) + (pow(c2, 2) - pow(Len[2], 2)) * t * t;
	D = B * B - 4 * A * C;
	/*cout << "A:" << A << " B:" << B << " C:" << C << " D:" << D << endl;*/

	double u1, u2;
	if (D > 0) {
		u1 = (-B + sqrt(D)) / (2 * A);
		u2 = (-B - sqrt(D)) / (2 * A);
		/*cout << "sqrt(D): " << sqrt(D) << endl;*/
		/*cout << "u1:" << u1 << " u2:" << u2 << endl;*/

		if (configuration == 1) {
			arg_4 = atan(u1) * 2;
			cout << "arg_4(1): " << arg_4 << endl;
			return arg_4;
		}
		else if (configuration == 0) {
			arg_4 = atan(u2) * 2;
			cout << "arg_4(2): " << arg_4 << endl;
			return arg_4;
		}
	}
	else if (D == 0) {
		u1 = -B / (2 * A);
		arg_4 = atan(u1) * 2;
		cout << "arg_4(3): " << arg_4 << endl;
		return arg_4;
	}
	else {
		cout << ("[Out of Rotation Range]\n");
		cout << "arg_4(4): " << arg_4 << endl;
		return arg_4;
	}
}
double Angular_Velocity_Analysis(double Len[], double arg[],double omega_2) {
	using namespace std;
	double arg_3;
	double ar3;
	ar3 = Len[3] * sin(arg[1]) - Len[1] * sin(arg[0]);
	arg_3 = asin(ar3 / Len[2]);
	/*cout << "sin(arg_4): " << sin(arg[1]) << " sin(arg_2): " << sin(arg[0]) << endl;
	cout << "arg_3: " << arg_3 << endl;*/

	double omega_3;
	double omega_4;
	omega_3 = -(Len[1] * sin(arg[0] - arg[1]) * omega_2) / (Len[2] * sin(arg_3 - arg[1]));
	omega_4 = -(Len[1] * sin(arg[0] - arg_3) * omega_2) / (Len[3] * sin(arg_3 - arg[1]));
	//cout << "sin(arg_2 - arg_4): " << sin(arg[0] - arg[1]) << endl;
	//cout << "sin(arg_3 - arg_4): " << sin(arg_3 - arg[1]) << endl;
	/*cout << "omega_3: " << omega_3 << endl;
	cout << "omega_4: " << omega_4 << endl;*/
	return omega_4;
}
