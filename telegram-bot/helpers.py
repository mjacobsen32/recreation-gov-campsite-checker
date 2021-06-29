from subprocess import PIPE, Popen

def get_available(cmd):
    with Popen(cmd, stdout=PIPE, stderr=None, shell=True) as process:
        output = process.communicate()[0].decode("utf-8")
    return(output)