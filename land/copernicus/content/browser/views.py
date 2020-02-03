import subprocess


def remoteUrl_exists(location):
    try:
        res = subprocess.check_call(['/usr/bin/curl', '-I', '-f', location])
        res = res
        return True
    except subprocess.CalledProcessError:
        return False
