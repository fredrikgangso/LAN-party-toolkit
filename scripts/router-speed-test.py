import datetime
import argparse
import logging
import csv
import os

import speedtest

argparser = argparse.ArgumentParser()

argparser.add_argument("-r", "--router", help="Router number", type=str)
argparser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

args = argparser.parse_args()

logging.basicConfig(level=logging.DEBUG) if args.verbose else None

class RouterSpeedTest:
    def __init__(self):
        """
        initializes the RouterSpeedTest class.
        """
        self.routerNumber = args.router if args.router else "x"
        logging.debug(f"router number: {self.routerNumber}")

        self.currentDate = datetime.date.today()
        self.currentTime = datetime.datetime.now().strftime("%H.%M.%S")
        logging.debug(f"current date: {self.currentDate}, current time: {self.currentTime}")

        self.speedTest = speedtest.Speedtest()

    def locateStorage(self):
        """
        locates the storage location for the speed test results.

        returns:
            str: The storage location for the speed test results.
        """
        logging.debug("running locateStorage()...")

        # Create 'archive' folder if it doesn't exist
        path = os.path.join("archive")
        logging.debug(f"'{path}' folder exists") if os.path.exists(path) else (os.mkdir(path), logging.debug(f"'{path}' folder does not exist: creating a new folder"))

        # Create 'router_speed_test' folder if it doesn't exist
        path = os.path.join(path, "router-speed-test")
        logging.debug(f"'{path}' folder exists") if os.path.exists(path) else (os.mkdir(path), logging.debug(f"'{path}' folder does not exist: creating a new folder"))

        # Create folder for the current date if it doesn't exist
        path = os.path.join(path, str(self.currentDate))
        logging.debug(f"'{path}' folder exists") if os.path.exists(path) else (os.mkdir(path), logging.debug(f"'{path}' folder does not exist: creating a new folder"))

        return path
    
    def runSpeedTest(self):
        """
        runs a speed test and returns the results.

        returns:
            dict: The speed test results.
        """
        logging.debug("running runSpeedTest()...")

        downloadSpeed = self.speedTest.download() / 1_000_000  # Convert to Mbps
        uploadSpeed = self.speedTest.upload() / 1_000_000  # Convert to Mbps
        logging.debug(f"download speed: {downloadSpeed:.2f} Mbps, upload speed: {uploadSpeed:.2f} Mbps")

        return {
            "download": downloadSpeed,
            "upload": uploadSpeed,
        }
    
    def createLogFile(self, results: list, path: str):
        """	
        creates a CSV log file with the speed test results.

        args:
            results (list): List of speed test results.
            path (str): The path to the storage location.
        """
        logging.debug("running createLogFile()...")

        csvFile = f"r{self.routerNumber}-{self.currentTime}.csv"
        logging.debug(f"csv file: {csvFile}")
        
        with open(os.path.join(path, csvFile), "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["test", "download", "upload"])
            for idx, test in enumerate(results, start=1):
                csvwriter.writerow([f"{idx}", f"{test['download']:.2f} Mbps", f"{test['upload']:.2f} Mbps"])

if __name__ == "__main__":
    routerSpeedTest = RouterSpeedTest()
    storageLocation = routerSpeedTest.locateStorage()
    results = [routerSpeedTest.runSpeedTest() for _ in range(3)]
    routerSpeedTest.createLogFile(results, storageLocation)
