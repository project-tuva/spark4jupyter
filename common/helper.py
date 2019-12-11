import argparse
import subprocess


def get_argparser():
    parser = argparse.ArgumentParser(description='NVCCPlugin params')
    parser.add_argument("-t", "--timeit", action='store_true',
                        help='flag to return timeit result instead of stdout')
    return parser


# https://thraxil.org/users/anders/posts/2008/03/13/Subprocess-Hanging-PIPE-is-your-enemy/
def popen(command,
          cwd=".",
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          print_stdout=True,
          print_stderr=True):


    child = subprocess.Popen([command],
                              shell=True,
                              cwd=cwd,
                              stdout=stdout,
                              stderr=stderr)
    out, err = child.communicate()
    print("Executed command\n'{}'\n\
    from directory {}\n\
    PID {}\n\
    Return code {}"
    .format(command,cwd, child.pid, child.returncode))

    # out and err contain info even if child didn't exit properly
    if(print_stdout):
        print("stdout:\n{}".format(out.decode("utf-8")))
    if(print_stderr):
        print("stderr:\n{}".format(err.decode("utf-8")))

    if(child.returncode):
        print("WARNING! command return code different from zero\n\
        stderr:\n{}\n\
        Press 0 to continue, 1 (!=0) to abort:\n".format(err.decode("utf-8")))

        choice=int(input("-->"))

        if(choice):
            raise RuntimeError("Execution of {} broke.".format(command))
