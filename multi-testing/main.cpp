#include <bits/stdc++.h>

using namespace std;

int main(int argc, char** argv) {
  // printf("args:");
  // for (int i = 0; i < argc; i++) {
  //   printf(" %s", argv[i]);
  // }
  if (argc == 1) {
    cout << "error: file to test was not given" << endl;
    return 0;
  }
  string path = argv[1];
  cerr << "path: " << path << '\n';
  return 0;
}
