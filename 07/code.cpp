#include <iostream>
#include <string>

using namespace std;

int mmat[3001][3001];
int summ[3001][3001];

int char_to_num(char c) {
	if (c == '.') {
		return 0;
	} else if (c >= 'a' and c <= 'z') {
		return -(c - 'a' + 1);
	} else {
		return c - 'A' + 1;
	}
}

bool is_infinity(int N, int M) {
	for (int row = 0; row < N; row++) {
		int sum = 0;
		for (int col = 0; col < M; col++) {
			sum += mmat[row][col];
		}
		if (sum > 0) {
			return true;
		}
	}

	for (int col = 0; col < M; col++) {
		int sum = 0;
		for (int row = 0; row < N; row++) {
			sum += mmat[row][col];
		}
		if (sum > 0) {
			return true;
		}
	}
	return false;
}

string solve(int N, int M) {
	if (is_infinity(N, M)) {
		return "INFINITY";
	}

	for (int repr = 0; repr <= 2; repr++) {
		for (int repc = 0; repc <= 2; repc++) {
			if (repc == 0 && repr == 0) {
				continue;
			}
			for (int row = 0; row < N; row++) {
				for (int col = 0; col < M; col++) {
					mmat[N*repr+row][M*repc+col] = mmat[row][col];
				}
			}
		}
	}
	for (int row = 0; row < 3*N; row++) {
		for (int col = 0; col < 3*M; col++) {
			summ[row][col+1] = summ[row][col] + mmat[row][col];
		}
	}
	int best_val = 0;
	for (int sc = 0; sc < 3*M; sc++) {
		for (int ec = sc; ec < 3*M; ec++) {
			int cur_val = 0;
			for (int row = 0; row < 3*N; row++) {
				int v = summ[row][ec+1] - summ[row][sc];
				if (cur_val < 0) {
					cur_val = v;
				} else {
					cur_val += v;
				}
				if (cur_val > best_val) {
					best_val = cur_val;
				}
			}
		}
	}
	return to_string(best_val);
}

int main() {
	int C,N,M;
	char c; 
	cin >> C;
	for (int cs = 1; cs <= C; cs++) {
		cin >> N >> M;
		bool more_cols = M > N;
		for (int i = 0; i < N; i++) {
			summ[i][0] = 0;
			for (int j = 0; j < M; j++) {
				cin >> c;
				int num = char_to_num(c);
				if (more_cols) {
					mmat[j][i] = num; 
				} else {
					mmat[i][j] = num; 
				}
			}
		}
		// transpose the matrix if M > N, since this algo is O(M^2 * N)
		string val = more_cols ?  solve(M, N) : solve(N, M);
		cout << "Case #" << cs << ": " << val << endl;
	}
}