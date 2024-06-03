import urllib.request
import time
import sys
import socket
from statistics import stdev
from amiya.utils.helper import *

class InternetSpeedTest:
    def __init__(self, test_url=None, chunk_size=1024*1024, runtime=15):  # Set smaller chunk size for frequent updates
        if test_url is None:
            self.test_url = "https://www.thinkbroadband.com/download/2GB" #http://speedtest.tele2.net/1GB.zip"
        else:
            self.test_url = test_url
            
        self.chunk_size = chunk_size
        self.runtime = runtime
        
        self.max_speed = 50
        
        self.prefix_space = get_prefix_space()

    def show_downloads(self):
        aprint(Printer.to_lightblue("Internet speed test download links:"))
        print(f" - {self.test_url}")

    def get_content_length(self, url):
        try:
            request = urllib.request.Request(url, method='HEAD')
            response = urllib.request.urlopen(request)
            return int(response.headers['Content-Length'])
        except Exception as e:
            print(f"Error getting content length: {str(e)}")
            return None

    def ping(self, url):
        host = urllib.request.urlparse(url).hostname
        try:
            ping_times = []
            for _ in range(10):  # Take 10 pings to calculate average and jitter
                start_time = time.time()
                socket.create_connection((host, 80), timeout=2)
                ping_times.append((time.time() - start_time) * 1000)  # Convert to milliseconds
            avg_ping = sum(ping_times) / len(ping_times)
            jitter = stdev(ping_times)
            return avg_ping, jitter
        except Exception as e:
            print(f"Error pinging {host}: {str(e)}")
            return None, None

    def print_speed_bar(self, speed_mbps):
        bar_length = 50  # Length of the horizontal bar
        filled_length = int(bar_length * speed_mbps / self.max_speed)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"{self.prefix_space} - Current speed:  |{bar}| {speed_mbps:.2f} Mbps{' ' * 8}")

    def download_speed(self, url):
        total_size = self.get_content_length(url)
        if total_size is None:
            return None, None, None, None, None

        avg_ping, jitter = self.ping(url)

        start_time = time.time()
        downloaded_size = 0
        last_report_time = start_time
        total_chunks = 0
        lost_chunks = 0
        speed_samples = []
        try:
            response = urllib.request.urlopen(url)
            while True:
                if time.time() - start_time >= self.runtime and self.runtime != -1:
                    break 
                
                chunk = response.read(self.chunk_size)
                if not chunk:
                    break
                total_chunks += 1
                if len(chunk) != self.chunk_size:
                    lost_chunks += 1
                downloaded_size += len(chunk)
                current_time = time.time()
                elapsed_time = current_time - last_report_time
                if elapsed_time >= 1:  # Update less frequently with larger elapsed time
                    size_mb = downloaded_size / (1024 * 1024)  # Convert bytes to megabytes
                    speed_mbps = (size_mb / (current_time - start_time)) * 8  # Convert MB/s to Mbps
                    speed_samples.append(speed_mbps)
                    loss_percentage = (lost_chunks / total_chunks) * 100 if total_chunks > 0 else 0
                    self.print_speed_bar(speed_mbps)
                    print(f"{self.prefix_space} - Packet loss:    {loss_percentage:.2f}%{' ' * 8}")
                    print(f"{self.prefix_space} - Latency:        {avg_ping:.2f} ms{' ' * 8}")
                    print(f"{self.prefix_space} - Jitter:         {jitter:.2f} ms{' ' * 8}")
                    self.setback_cursor()
                    last_report_time = current_time
        except Exception as e:
            print(f"Error: {str(e)}")
            return None, None, None, None, None

        end_time = time.time()
        total_duration = end_time - start_time
        size_mb = downloaded_size / (1024 * 1024)  # Convert bytes to megabytes
        average_speed_mbps = (size_mb / total_duration) * 8  # Convert MB/s to Mbps
        loss_percentage = (lost_chunks / total_chunks) * 100 if total_chunks > 0 else 0
        return average_speed_mbps, loss_percentage, total_size / (1024 * 1024), avg_ping, jitter  # Return additional metrics



    def test_speed(self):
        results = {}
        print(f"{self.prefix_space} {Printer.to_purple('> Testing URL')}: {Printer.to_lightgrey(self.test_url)}")
        print(f"{self.prefix_space} - Current speed:  starting...")
        print(f"{self.prefix_space} - Packet loss:    starting...")
        print(f"{self.prefix_space} - Latency:        calculating...")
        print(f"{self.prefix_space} - Jitter:         calculating...")
        self.setback_cursor()

        speed, loss, total_size, avg_ping, jitter = self.download_speed(self.test_url)
        if speed is not None:
            results = (round(speed, 4), loss, total_size, avg_ping, jitter)
        else:
            results = ("Error during download", "N/A", "N/A", "N/A", "N/A")
        print("\n")
        return results
        
    def setback_cursor(self):
        print("\033[F\033[F\033[F\033[F", end="")
        
    def reset_cursor(self):
        print("\n\n\n\n", flush=True)
        

    @staticmethod
    def run():
        speed_test = InternetSpeedTest()
        aprint(Printer.to_lightblue("Starting internet speed test. Press CTRL+C to stop anytime."))
        
        try:
            # speed_test.show_downloads()
            results = speed_test.test_speed()
        except KeyboardInterrupt:
            speed_test.reset_cursor()
            raise KeyboardInterrupt()

        print("\n")
        aprint(f"{Printer.to_lightblue("Results:")} Average Speed: {results[0]} Mbps, Packet Loss: {results[1]}%, Total Size: {results[2]} MB")


