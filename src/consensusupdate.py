#!/usr/bin/env python2

# TODO: Will daemonizing the exitmap process lead to the asynch call to be
# daemonized as well? Check and test the same.

# Exitmap ---> Consensus Update
#   ||	     	||
#   ||		    ||
#   \/		    ||
#   \/		    \/
#   \/ 	Fork a process using mp --------> Use process and schedule module
# 	\/			                 	      to periodically update consensus
#   \/                                                  ||
#   \/                                                  ||
#   \/                                                  \/
#   \/                                                  \/
#   \/                                                  \/


import time
import sys
import multiprocessing
from stem.descriptor.remote import DescriptorDownloader

UPDATETIME = 180


def update(save_to_cache=True):
    """
    Function for updating the process update_time specifies the interval at which the consensus is updated.
    """
    consensus_downloader = DescriptorDownloader(
    use_mirrors = True,
    retries = 10,
    timeout = 30,
    )
    query = consensus_downloader.get_server_descriptors()
    desc_objects = []
    try:
        for desc in query.run():
            if desc.exit_policy.is_exiting_allowed():
                # Implement save_to_cache
                desc_objects += [desc]
                print desc.fingerprint, desc.nickname
    except Exception as exc:
        print 'Unable to retrieve the server descriptors: %s' % exc
    if save_to_cache:
        return save_to_cache(desc_objects)
    else:
        return


def save_to_cache(descs):
    """
    Overwrites the local cached-consensus file used by exitmap to allow
    for fresher micro-descriptors.
    """
    return


def initialize():
    """
    Initialization step. Asynchronous process created apart from exitmap to
    update the consensus micro-descriptors in the background
    """
    pool = multiprocessing.Pool(processes=1)
    # Find better way to detect exit by the main exitmap process
    try:
        print "Went into the process pool."
        while True:
            pool.apply_async(update, (), dict(save_to_cache = False))
            time.sleep(UPDATETIME)
    except SystemExit:
        print "Caught exit signal, exitting gracefully."
        pool.join()
        pool.close()
    return


def main():
    """
    Steps to run when executed directly from the command line
    """
    sys.exit(update())


if __name__ == '__main__':
     sys.exit(main())
