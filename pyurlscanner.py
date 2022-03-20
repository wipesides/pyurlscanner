import multiprocessing
import time
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import argparse

class SubEnum:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="A website subdirectory scanner.With given list and URL,it makes requests to the address and prints whether request is successful or not.")
        self.parser._action_groups.pop()
        self.required_ones = self.parser.add_argument_group('REQUIRED ARGUMENTS')
        self.required_ones.add_argument('-u', metavar='--url', help='URL of the target', required=True)
        self.required_ones.add_argument('-w', metavar='--wordlist', help='List of subdirectories to enumerate', required=True)

        self.optional_ones = self.parser.add_argument_group('OPTIONAL ARGUMENTS')
        self.optional_ones.add_argument('-v', help='Enable verbose mode to view ALL attempts. Default=False', action='store_true')
        self.optional_ones.add_argument('-s', metavar='--sleep', help='Amount of time to sleep between requests', default=0, nargs='?')
        self.optional_ones.add_argument('-t', metavar='--timeout', help='Amount of timeout time. Default=1', default=1, nargs='?')
        self.args = self.parser.parse_args()

        self.TOTAL_CPUS = multiprocessing.cpu_count()
        self.URL = self.args.u
        self.LIST_PATH = self.args.w
        self.VERBOSE = self.args.v
        self.TIMEOUT = self.args.t
        self.SLEEP = self.args.s
        self.LIST_RAW = open(f"{self.LIST_PATH}").read().splitlines()
        self.LIST_SEPARATED = [directories for directories in self.LIST_RAW]

    def handler(self,list2): # Reads the file line by line and making requests to given URL.Then checks it.
        for subdirectory in list2:
            generated_url = f"{self.URL}/{subdirectory}"
            try:
                attempt = requests.get(generated_url, timeout=self.TIMEOUT)
                response_code = attempt.status_code
                time.sleep(self.SLEEP)
            except Exception as e:
                if self.VERBOSE:
                    print(f"{e} : {generated_url}")
            else:
                if int(response_code) == 200:
                    print(f"Valid URL : {generated_url}")
                else:
                    if self.VERBOSE:
                        print(f"Invalid URL : {generated_url}")
    def thread_2(self): # Uses threads to run handler()
        with ThreadPoolExecutor(max_workers=self.TOTAL_CPUS) as pe:
            for domains in self.LIST_SEPARATED:
                pe.submit(self.handler, (domains,))

if __name__ == '__main__':
    timer = datetime.now()
    run = SubEnum().thread_2()
    print("Scan is completed in " + str(datetime.now() - timer))
