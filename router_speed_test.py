import datetime
import os
import csv
import sys

import speedtest

class TestRouter:
    def __init__(self, router_number: str = ""):
        """
        Initializes the TestRouter class.

        Args:
            router_number (str): The router number.
        """
        print("Running speedtest...")
        self.todaysDate = datetime.date.today()
        self.todaysTime = datetime.datetime.now().strftime("%H%M%S")
        self.speedtest = speedtest.Speedtest()

        router_number = sys.argv[1] if len(sys.argv) > 1 else router_number

        # Create 'speed_test' folder if it doesn't exist
        self.create_speed_test_folder()

        # Select nearby servers
        self.speedtest.get_servers()
        self.speedtest.get_best_server()

        # Run multiple tests for better accuracy
        num_tests = 3  # You can adjust this value
        results = [self.run_speed_test() for _ in range(num_tests)]

        self.find_or_create_log_location(router_number)
        self.create_log_file(router_number, results)
        print("Test complete")

    def run_speed_test(self):
        """
        Runs a speed test and returns the results.
        """
        download_speed = self.speedtest.download() / 1_000_000  # Convert to Mbps
        upload_speed = self.speedtest.upload() / 1_000_000  # Convert to Mbps
        ping = self.speedtest.results.ping

        return {
            "Download": download_speed,
            "Upload": upload_speed,
            "Ping": ping
        }

    def create_speed_test_folder(self):
        """
        Creates a 'speed_test' folder if it doesn't exist.
        """
        if not os.path.exists("speed_test"):
            os.mkdir("speed_test")
            print("'speed_test' folder does not exist: creating a new folder")

    def find_or_create_log_location(self, router_number: str):
        """
        Checks if the folder for the current date exists, creates it if not.

        Args:
            router_number (str): The router number.
        """
        folder_path = os.path.join("speed_test", str(self.todaysDate))
        if os.path.exists(folder_path):
            print("Folder exists: not creating a new folder")
        else:
            os.mkdir(folder_path)
            print("Folder does not exist: creating a new folder")

    def create_log_file(self, router_number: str, results: list):
        """
        Creates a CSV log file with the speed test results.

        Args:
            router_number (str): The router number.
            results (list): List of speed test results.
        """
        if router_number:
            router_file = f"Router_{router_number}_"

        folder_path = os.path.join("speed_test", str(self.todaysDate))
        csv_file = f"{folder_path}/{router_file}{self.todaysTime}.csv"
        with open(csv_file, "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Test", "Router", "Download", "Upload", "Ping"])
            for idx, test in enumerate(results, start=1):
                csvwriter.writerow([f"{idx}", f"{router_number}", f"{test['Download']:.2f} Mbps", f"{test['Upload']:.2f} Mbps", f"{test['Ping']:.2f} ms"])

if __name__ == "__main__":
    # Command-line argument for router number
    router_number_arg = sys.argv[2] if len(sys.argv) > 2 else ""

    TestRouter(router_number_arg)
