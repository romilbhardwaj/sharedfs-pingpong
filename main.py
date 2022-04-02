# sharedfs-pingpong - A demo to illustrate sky.Storage's mounting feature.
#
# This program implements coordination between two or more processes using a
# shared file system that they can access.
#
# Simplest example is with two processes - the first process is called ping,
# and the second is pong. The ping process writes to the file, and the pong
# process reads from the file. Pong then writes to the file, and ping reads
# from the file. This continues indefinitely until the user presses Ctrl-C.
#
# Usage:
#   python main.py --process-id 0 --shared-path /tmp/ --num-processes 2
#   python main.py --process-id 1 --shared-path /tmp/ --num-processes 2

import argparse
import os
import time

# Parse command line arguments
parser = argparse.ArgumentParser(
    description='A demo program to illustrate sky.Storage mounting feature.')
parser.add_argument('--process-id', '-p', type=int, default=0,
                    help='The process ID to assign this process. Start at 0.')
parser.add_argument('--num-processes', '-n', type=int, default=2,
                    help='Total number of processes.')
parser.add_argument('--shared-path', '-s', type=str,
                    default='/tmp/sharedfs-pingpong',
                    help='The path to the shared directory (Storage mount '
                         'point)')
args = parser.parse_args()


class PingPong(object):
    def __init__(self, process_id, num_processes, shared_path):
        self.process_id = process_id
        self.num_processes = num_processes
        self.shared_path = shared_path
        self.read_file_path = os.path.join(self.shared_path,
                                           f'{self.process_id}.txt')
        self.write_file_path = os.path.join(self.shared_path,
                                            f'{(self.process_id + 1) % self.num_processes}.txt')

    def write_output(self):
        data = f'This is a message from process {format(self.process_id)}' \
               f' at time {time.time()}'
        with open(self.write_file_path, 'w') as f:
            f.write(data)

    def read_input(self):
        with open(self.read_file_path, 'r') as f:
            data = f.read()
        return data

    def delete_input(self):
        os.remove(self.read_file_path)

    def run_forever(self):
        while True:
            if os.path.exists(self.read_file_path):
                data = self.read_input()
                print(f'[Process {self.process_id}]: Got data: {data}')
                time.sleep(1)
                self.write_output()
                self.delete_input()


def main():
    print("Starting pingpong with args:", args)
    # Initialize the read file if process 0
    if args.process_id == 0:
        with open(os.path.join(args.shared_path, '0.txt'), 'w') as f:
            f.write('This is a test message from process -1 at time 0')
    p = PingPong(args.process_id, args.num_processes, args.shared_path)
    p.run_forever()


if __name__ == '__main__':
    main()
