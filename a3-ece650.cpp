// adapted from https://www.gnu.org/software/libc/manual/html_node/Example-of-Getopt.html
#include <unistd.h>
#include <iostream>
#include <vector>
#include <string.h>
#include <sys/wait.h>
#include <signal.h>
using namespace std;

/// main() must be declared with arguments
/// otherwise command line arguments are ignored
int main (int argc, char **argv)
{
    string cvalue;
    int c;
    int sk=10;
    int nk=5;
    int lk=5;
    int ck=20;

    opterr = 0;

    // expected options are '-s value', '-n value', '-l value',and '-c value'
    while ((c = getopt (argc, argv, "s:n:l:c:")) != -1)
        switch (c)
        {
        case 's':
            cvalue = optarg;
            sk = atoi(cvalue.c_str());
            break;
        case 'n':
            cvalue = optarg;
            nk = atoi(cvalue.c_str());
            break;
        case 'l':
            cvalue = optarg;
            lk = atoi(cvalue.c_str());
            break;
        case 'c':
            cvalue = optarg;
            ck = atoi(cvalue.c_str());
            break;
        case '?':
            cerr << "Error: unknown option" << endl;
            return 1;
        default:
            return 0;
        }

    vector<pid_t> kids;
    // create 2 pipes
    int pipe1[2];
    int pipe2[2];
    pipe(pipe1);
    pipe(pipe2);

    char* argv0[10];
    char* argv1[3];
    char* argv2[2];

    string str[4];

    argv0[0] = (char*)"./rgen";
    argv0[1] = (char*)"-s";
    str[0] = to_string(sk);
    argv0[2] = (char*)str[0].c_str();
    argv0[3] = (char*)"-n";
    str[1] = to_string(nk);
    argv0[4] = (char*)str[1].c_str();
    argv0[5] = (char*)"-l";
    str[2] = to_string(lk);
    argv0[6] = (char*)str[2].c_str();
    argv0[7] = (char*)"-c";
    str[3] = to_string(ck);
    argv0[8] = (char*)str[3].c_str();
    argv0[9] = nullptr;

    argv1[0] = (char*)"/bin/python";
    argv1[1] = (char*)"--version";
    //argv1[1] = (char*)"a1-ece650.py";
    argv1[2] = nullptr;

    argv2[0] = (char*)"./a2-ece650";
    argv2[1] = nullptr;

    pid_t child_pid;
    int res;
    //Porcess for graph generation
    child_pid = fork ();
    if (child_pid == 0)
    {
        //sleep(10);
        close(pipe2[0]);
        close(pipe2[1]);
        // redirect stdout to the pipe write end
        dup2(pipe1[1], STDOUT_FILENO);
        close(pipe1[0]);     // Close this too!
        close(pipe1[1]);

        // start a1 process
        //execv ("./rgen", argv0);
    }
    kids.push_back(child_pid);

    //Process for python finding graphs
    child_pid = fork ();
    if (child_pid == 0)
    {

        // redirect stdin to the pipe read end
        //dup2(pipe1[0], STDIN_FILENO);
        close(pipe1[1]);     // Close this too!
        close(pipe1[0]);
        // redirect stdout from the pipe write end
        //dup2(pipe2[1], STDOUT_FILENO);
        close(pipe2[0]);
        close(pipe2[1]);

        // start a1 process
        cout << "running" << endl;
        execv ("/bin/python", argv1);
    }
    kids.push_back(child_pid);

    //Process for find the shortest path
    child_pid = fork ();
    if (child_pid == 0)
    {
        close(pipe1[1]);     // Close this too!
        close(pipe1[0]);
        // redirect stdin from the pipe read end
        dup2(pipe2[0], STDIN_FILENO);
        close(pipe2[0]);
        close(pipe2[1]);

        // start a2 process
        execv ("./a2-ece650", argv2);
    }
    kids.push_back(child_pid);
    
    child_pid = 0;

    close(pipe1[1]);     // Close this too!
    close(pipe1[0]);
    // redirect stdin from the pipe write end
    //dup2(pipe2[0], STDIN_FILENO);
    dup2(pipe2[1], STDOUT_FILENO);
    close(pipe2[0]);
    close(pipe2[1]);

    //waitpid(kids[1], &res, 0);
    string line;
    while(1){
        getline(cin, line);
        if(!cin){
            if(cin.eof())
                break;
        }
        cout << line << endl;
    }

    kill(kids[0], SIGKILL);
    kill(kids[1], SIGKILL);
    kill(kids[2], SIGKILL);

    waitpid(kids[0], &res, 0);
    waitpid(kids[1], &res, 0);
    waitpid(kids[2], &res, 0);
    //cerr << "Error: EOF, kill all the processes\n";
    return 0;
}
