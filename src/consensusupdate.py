#!/usr/bin/env python2

# TODO: Will daemonizing the exitmap process lead to the asynch call to be
# daemonized as well? Check and test the same.


import sys
from stem.descriptor.remote import DescriptorDownloader
import multiprocessing
from time import sleep


def updateConsensus():
    """
    Asynchronous process for updating the process
    """
    consensus_downloader = DescriptorDownloader(
    use_mirrors = True,
    retries = 10,
    timeout = 30,
    )

    query = consensus_downloader.get_server_descriptors()
    try:
        for desc in query.run():
            if desc.exit_policy.is_exiting_allowed():
                print '  %s (%s)' % (desc.nickname, desc.fingerprint)
    except Exception as exc:
      print 'Unable to retrieve the server descriptors: %s' % exc

def run():
    """
    Main function to create process Pool and call
    """
    pool = multiprocessing.Pool()
    while (True):
        pool.apply_async(updateConsensus, args = ())
    pool.close()
    pool.join()


def main():
    """
    Default settings when run from the command line
    """
