/*
For testing solutions in parallel with multiprocessing.

https://stackoverflow.com/questions/23587529/fork-and-system-calls-not-working-as-i-expect

Don't use system() because you get some security issues with making a root shell?
https://stackoverflow.com/questions/27461936/system-vs-execve

TODO: kill all child processes when a test case fails
TODO: find a way to use multi-threading (same address space)!
*/

#include <sys/wait.h>
#include <unistd.h>

#include <cassert>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

const int PROCESSES = 1;
const int TESTS_PER_PROCESS = 10;

int main(int argc, char** argv) {
  printf("args:");
  for (int i = 0; i < argc; i++) {
    printf(" %s", argv[i]);
  }
  if (argc == 1) {
    cout << "error: file to test was not given" << endl;
    return 0;
  }
  if (argc > 2) {
    cout << "error: too many arguments given" << endl;
    return 0;
  }
  const string path = argv[1];
  int i = (int) path.size() - 1;
  while (path[i] != '/') {
    --i;
  }
  const string dir = path.substr(0, i);
  const string sol = dir + "/a";
  const string slow = dir + "/slow";
  // cerr << "dir: " << dir << '\n';
  // cerr << "path: " << path << '\n';
  pid_t pid;
  vector<pid_t> pids;
  for (int p = 0; p < PROCESSES; p++) {
    pid = fork();
    if (pid == 0) {
      break;
    }
    pids.push_back(pid);
  }
  if (pid == 0) {
    // child process

    // make args for the execv process
    char* sol_c_str = new char[sol.size() + 1];
    sol.copy(sol_c_str, sol.size());
    char* const sol_argv[] = {
        sol_c_str,
        // "<",
        nullptr,
    };
    popen()

    for (int test = 0; test < TESTS_PER_PROCESS; test++) {
      int ret = execv(sol_c_str, sol_argv);
      // cerr << "finished executing" << endl;
      assert(ret == 0);
    }
  } else {
    for (int child_pid : pids) {
      waitpid(child_pid, nullptr, 0);
    }
  }
  return 0;
}
