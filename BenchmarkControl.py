import csv
import threading
import time
import subprocess
import psutil
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt
from Common import display_scrollable_message, sieve_is_running, ram_is_running, data_is_running, aritm_is_running, logic_is_running
from Common import set_aritm_running, set_data_running, set_logic_running, set_sieve_running, set_ram_running


# Colors
WHITE = "#FFFFFF"
GREY = "#808080"
BLUE = "#007ba7"
ORANGE = "#FFA500"
CRIMSON = "#DC143C"
ROYAL_BLUE = "#4169E1"
PINE_GREEN = "#01796F"
PURPLE = "#800080"




def run_sieve_benchmark(figure_plot_disk, line_graph, benchmark_data, data, count):
    benchmark_data['time'].clear()
    benchmark_data['cpu usage'].clear()
    benchmark_data['ram usage'].clear()

    last_time = data['time'][-1] if data['time'] else 0
    last_cpu_usage = data['cpu usage'][-1] if data['cpu usage'] else 0
    last_ram_usage = data['ram usage'][-1] if data['ram usage'] else 0

    benchmark_data['time'].append(last_time)
    benchmark_data['cpu usage'].append(last_cpu_usage)
    benchmark_data['ram usage'].append(last_ram_usage)
    count[0] += 1

    set_sieve_running(True)

    def monitor_resource_usage(count):
        try:
            while sieve_is_running.is_set():
                benchmark_data['time'].append(count[0])
                count[0] += 1
                benchmark_data['cpu usage'].append(psutil.cpu_percent())
                benchmark_data['ram usage'].append(psutil.virtual_memory().percent)
                time.sleep(1)
        finally:
            set_sieve_running(False)

    monitor_sieve_thread = threading.Thread(target=monitor_resource_usage, args=(count,))
    monitor_sieve_thread.start()

    def execute_sieve():
        try:
            result = subprocess.run(["prime.exe"], check=True, capture_output=True, text=True)

            with open("prime.csv", "r") as file:
                file_content = file.read()

            display_scrollable_message("C++ Program Output", file_content)

            for key in data:
                if key in benchmark_data:
                    data[key].extend(benchmark_data[key])

            plot_sieve_benchmark_data(figure_plot_disk, line_graph)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running the C++ program: {e}")
            set_sieve_running(False)
        except FileNotFoundError:
            messagebox.showerror("Error", "C++ executable not found!")
            set_sieve_running(False)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            set_sieve_running(False)
        finally:
            set_sieve_running(False)
            monitor_sieve_thread.join()

    threading.Thread(target=execute_sieve).start()

def run_arithmetic_benchmark(figure_plot_disk, line_graph, benchmark_data, data, count):

    benchmark_data['time'].clear()
    benchmark_data['cpu usage'].clear()
    benchmark_data['ram usage'].clear()

    last_time = data['time'][-1] if data['time'] else 0
    last_cpu_usage = data['cpu usage'][-1] if data['cpu usage'] else 0
    last_ram_usage = data['ram usage'][-1] if data['ram usage'] else 0

    benchmark_data['time'].append(last_time)
    benchmark_data['cpu usage'].append(last_cpu_usage)
    benchmark_data['ram usage'].append(last_ram_usage)
    count[0] += 1

    set_aritm_running(True)

    def monitor_resource_usage(count):
        try:
            while aritm_is_running.is_set():
                benchmark_data['time'].append(count)
                count[0] += 1
                benchmark_data['cpu usage'].append(psutil.cpu_percent())
                benchmark_data['ram usage'].append(psutil.virtual_memory().percent)
                time.sleep(1)
        finally:
            set_aritm_running(False)

    monitor_aritm_thread = threading.Thread(target=monitor_resource_usage, args=(count,))
    monitor_aritm_thread.start()

    def execute_aritm():
        try:
            result = subprocess.run(["aritm.exe"], check=True, capture_output=True, text=True)

            with open("aritm.csv", "r") as file:
                file_content = file.read()

            display_scrollable_message("C++ Program Output", file_content)

            for key in data:
                if key in benchmark_data:
                    data[key].extend(benchmark_data[key])

            load_and_plot_csv_data_aritm(figure_plot_disk, line_graph)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running the C++ program: {e}")
            set_aritm_running(False)
        except FileNotFoundError:
            messagebox.showerror("Error", "C++ executable not found!")
            set_aritm_running(False)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            set_aritm_running(False)
        finally:
            set_aritm_running(False)
            monitor_aritm_thread.join()

    threading.Thread(target=execute_aritm).start()

def run_logic_benchmark(figure_plot_disk, line_graph, benchmark_data, data, count):

    benchmark_data['time'].clear()
    benchmark_data['cpu usage'].clear()
    benchmark_data['ram usage'].clear()

    last_time = data['time'][-1] if data['time'] else 0
    last_cpu_usage = data['cpu usage'][-1] if data['cpu usage'] else 0
    last_ram_usage = data['ram usage'][-1] if data['ram usage'] else 0

    benchmark_data['time'].append(last_time)
    benchmark_data['cpu usage'].append(last_cpu_usage)
    benchmark_data['ram usage'].append(last_ram_usage)
    count[0] += 1

    set_logic_running(True)

    def monitor_resource_usage(count):
        try:
            while logic_is_running.is_set():
                benchmark_data['time'].append(count[0])
                count[0] += 1
                benchmark_data['cpu usage'].append(psutil.cpu_percent())
                benchmark_data['ram usage'].append(psutil.virtual_memory().percent)
                time.sleep(1)
        finally:
            logic_is_running.clear()

    monitor_logic_thread = threading.Thread(target=monitor_resource_usage, args=(count,))
    monitor_logic_thread.start()

    def execute_logic():
        try:
            result = subprocess.run(["logic.exe"], check=True, capture_output=True, text=True)

            with open("logic.csv", "r") as file:
                file_content = file.read()

            display_scrollable_message("C++ Program Output", file_content)

            for key in data:
                if key in benchmark_data:
                    data[key].extend(benchmark_data[key])

            load_and_plot_csv_data_logic(figure_plot_disk, line_graph)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running the C++ program: {e}")
            set_logic_running(False)
        except FileNotFoundError:
            messagebox.showerror("Error", "C++ executable not found!")
            set_logic_running(False)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            set_logic_running(False)
        finally:
            set_logic_running(False)
            monitor_logic_thread.join()

    threading.Thread(target=execute_logic).start()

def run_data_benchmark(figure_plot_disk, line_graph, benchmark_data, data, count):

    benchmark_data['time'].clear()
    benchmark_data['cpu usage'].clear()
    benchmark_data['ram usage'].clear()

    last_time = data['time'][-1] if data['time'] else 0
    last_cpu_usage = data['cpu usage'][-1] if data['cpu usage'] else 0
    last_ram_usage = data['ram usage'][-1] if data['ram usage'] else 0

    benchmark_data['time'].append(last_time)
    benchmark_data['cpu usage'].append(last_cpu_usage)
    benchmark_data['ram usage'].append(last_ram_usage)
    count[0] += 1

    set_data_running(True)

    def monitor_resource_usage(count):
        try:
            while data_is_running.is_set():
                benchmark_data['time'].append(count[0])
                count[0] += 1
                benchmark_data['cpu usage'].append(psutil.cpu_percent())
                benchmark_data['ram usage'].append(psutil.virtual_memory().percent)
                time.sleep(1)
        finally:
            set_data_running(False)

    monitor_data_thread = threading.Thread(target=monitor_resource_usage, args=(count,))
    monitor_data_thread.start()

    def execute_data():
        try:
            result = subprocess.run(["data.exe"], check=True, capture_output=True, text=True)

            with open("data.csv", "r") as file:
                file_content = file.read()

            display_scrollable_message("C++ Program Output", file_content)

            for key in data:
                if key in benchmark_data:
                    data[key].extend(benchmark_data[key])

            load_and_plot_csv_data_dspeed(figure_plot_disk, line_graph)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running the C++ program: {e}")
            set_data_running(False)
        except FileNotFoundError:
            messagebox.showerror("Error", "C++ executable not found!")
            set_data_running(False)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            set_data_running(False)
        finally:
            set_data_running(False)
            monitor_data_thread.join()

    threading.Thread(target=execute_data).start()

def run_ram_benchmark(figure_plot_disk, line_graph, benchmark_data, data, count):

    benchmark_data['time'].clear()
    benchmark_data['cpu usage'].clear()
    benchmark_data['ram usage'].clear()

    last_time = data['time'][-1] if data['time'] else 0
    last_cpu_usage = data['cpu usage'][-1] if data['cpu usage'] else 0
    last_ram_usage = data['ram usage'][-1] if data['ram usage'] else 0

    benchmark_data['time'].append(last_time)
    benchmark_data['cpu usage'].append(last_cpu_usage)
    benchmark_data['ram usage'].append(last_ram_usage)
    count[0] += 1

    set_ram_running(True)

    def monitor_resource_usage(count):
        try:
            while ram_is_running.is_set():
                benchmark_data['time'].append(count[0])
                count[0] += 1
                benchmark_data['cpu usage'].append(psutil.cpu_percent())
                benchmark_data['ram usage'].append(psutil.virtual_memory().percent)
                time.sleep(1)
        finally:
            set_ram_running(False)

    monitor_ram_thread = threading.Thread(target=monitor_resource_usage, args=(count,))
    monitor_ram_thread.start()

    def execute_data():
        try:
            result = subprocess.run(["ram.exe"], check=True, capture_output=True, text=True)

            with open("ram.csv", "r") as file:
                file_content = file.read()

            display_scrollable_message("C++ Program Output", file_content)

            for key in data:
                if key in benchmark_data:
                    data[key].extend(benchmark_data[key])
                    
            load_and_plot_csv_data_rspeed(figure_plot_disk, line_graph)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running the C++ program: {e}")
            set_ram_running(False)
        except FileNotFoundError:
            messagebox.showerror("Error", "C++ executable not found!")
            set_ram_running(False)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            set_ram_running(False)
        finally:
            set_ram_running(False)
            monitor_ram_thread.join()

    threading.Thread(target=execute_data).start()




def plot_sieve_benchmark_data(figure_plot_disk, line_graph):
    try:
        data = pd.read_csv("prime.csv")

        if "limit" in data.columns and "execution_time" in data.columns:
            x = data['limit']
            y = data['execution_time']

            figure_plot_disk.clear()
            figure_plot_disk.plot(x, y, color=ORANGE, label="Sieve of Eratosthenes Execution Time")
            figure_plot_disk.set_title("Sieve of Eratosthenes Benchmark")
            figure_plot_disk.set_xlabel("Limit", fontsize = 10)
            figure_plot_disk.set_ylabel("Execution Time (ms)", fontsize=10, color="black", rotation=90, labelpad=4)
            figure_plot_disk.legend()
            line_graph.draw()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading CSV data: {e}")

def load_and_plot_csv_data_aritm(figure_plot_disk, line_graph):
    try:
        data = pd.read_csv("aritm.csv")

        if "file_size" in data.columns and "time_add" in data.columns and "time_sub" in data.columns and "time_mul" in data.columns and "time_div" in data.columns:
            x = data['file_size']
            y_add = data['time_add']
            y_sub = data['time_sub']
            y_mul = data['time_mul']
            y_div = data['time_div']

            figure_plot_disk.clear()

            figure_plot_disk.plot(x, y_add, color=CRIMSON, label="Addition (ADD)")
            figure_plot_disk.plot(x, y_sub, color=ROYAL_BLUE, label="Subtraction (SUB)")
            figure_plot_disk.plot(x, y_mul, color=ORANGE, label="Multiplication (MUL)")
            figure_plot_disk.plot(x, y_div, color=PURPLE, label="Division (DIV)")

            figure_plot_disk.set_title("Arithmetic Operations Benchmark")
            figure_plot_disk.set_xlabel("Size Of File (mb)", fontsize=10)
            figure_plot_disk.set_ylabel("Encryption Execution Time (s)", fontsize=10, color="black", rotation=90, labelpad=4)

            figure_plot_disk.legend()
            line_graph.draw()
        else:
            messagebox.showerror("Error", "CSV file format is incorrect. Please ensure the columns are 'num_operations', 'time_add', 'time_sub', 'time_mul', and 'time_div'.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading CSV data: {e}")

def load_and_plot_csv_data_logic(figure_plot_disk, line_graph):
    try:
        data = pd.read_csv("logic.csv")

        if "file_size" in data.columns and "time_not" in data.columns and "time_and" in data.columns and "time_or" in data.columns and "time_xor" in data.columns:
            x = data['file_size']
            y_not = data['time_not']
            y_and = data['time_and']
            y_or = data['time_or']
            y_xor = data['time_xor']

            figure_plot_disk.clear()

            figure_plot_disk.plot(x, y_not, color=CRIMSON, label="NOT")
            figure_plot_disk.plot(x, y_and, color=ROYAL_BLUE, label="AND")
            figure_plot_disk.plot(x, y_or, color=ORANGE, label="OR")
            figure_plot_disk.plot(x, y_xor, color=PURPLE, label="XOR")

            figure_plot_disk.set_title("Logical Operations Benchmark")
            figure_plot_disk.set_xlabel("Size Of File (mb)", fontsize=10)
            figure_plot_disk.set_ylabel("Encryption Execution Time (s)", fontsize=10, color="black", rotation=90, labelpad=4)

            figure_plot_disk.legend()
            line_graph.draw()
        else:
            messagebox.showerror("Error", "CSV file format is incorrect. Please ensure the columns are 'num_operations', 'time_not', 'time_and', 'time_or', and 'time_xor'.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading CSV data: {e}")

def load_and_plot_csv_data_dspeed(figure_plot_disk, line_graph):
    try:
        data = pd.read_csv("data.csv")

        if "file_size" in data.columns and "read_speed" in data.columns and "write_speed" in data.columns:
            x = data['file_size']
            y_read = data['read_speed']
            y_write = data['write_speed']

            figure_plot_disk.clear()

            figure_plot_disk.plot(x, y_read, color=CRIMSON, label="Read Speed")
            figure_plot_disk.plot(x, y_write, color=ORANGE, label="Write Speed")

            figure_plot_disk.set_title("Data Transfer Speed Benchmark")
            figure_plot_disk.set_xlabel("Data Size", fontsize=10)
            figure_plot_disk.set_ylabel("Transfer speed (mb/s)", fontsize=10, color="black", rotation=90, labelpad=4)

            figure_plot_disk.legend()
            line_graph.draw()
        else:
            messagebox.showerror("Error", "CSV file format is incorrect.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading CSV data: {e}")

def load_and_plot_csv_data_rspeed(figure_plot_disk, line_graph):
    try:
        data = pd.read_csv("ram.csv")

        if "file_size" in data.columns and "read_speed" in data.columns and "write_speed" in data.columns:
            x = data['file_size']
            y_read = data['read_speed']
            y_write = data['write_speed']

            figure_plot_disk.clear()

            figure_plot_disk.plot(x, y_read, color=CRIMSON, label="Read Speed")
            figure_plot_disk.plot(x, y_write, color=ORANGE, label="Write Speed")

            figure_plot_disk.set_title("Data Transfer Speed Benchmark")
            figure_plot_disk.set_xlabel("Data Size", fontsize=10)
            figure_plot_disk.set_ylabel("Transfer speed (mb/s)", fontsize=10, color="black", rotation=90, labelpad=4)

            figure_plot_disk.legend()
            line_graph.draw()
        else:
            messagebox.showerror("Error", "CSV file format is incorrect.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading CSV data: {e}")



def calculate_score():
    total_time_add = 0
    total_time_sub = 0
    total_time_mul = 0
    total_time_div = 0
    total_rows = 0

    with open('aritm.csv', newline='') as csvfile1:
        csvreader = csv.DictReader(csvfile1)
        
        for row in csvreader:
            total_time_add += float(row['time_add'])
            total_time_sub += float(row['time_sub'])
            total_time_mul += float(row['time_mul'])
            total_time_div += float(row['time_div'])
            total_rows += 1

    avg_time_add = total_time_add / total_rows
    avg_time_sub = total_time_sub / total_rows
    avg_time_mul = total_time_mul / total_rows
    avg_time_div = total_time_div / total_rows

    avg_of_averages = (avg_time_add + avg_time_sub + avg_time_mul + avg_time_div) / 4

    scoreA = (
        10 if avg_of_averages <= 2 else
        9 if avg_of_averages <= 3 else
        8 if avg_of_averages <= 4 else
        7 if avg_of_averages <= 5 else
        6 if avg_of_averages <= 6 else
        5 if avg_of_averages <= 7 else
        4 if avg_of_averages <= 8 else
        3 if avg_of_averages <= 9 else
        2 if avg_of_averages <= 10 else
        1
    )

    total_time_not = 0
    total_time_and = 0
    total_time_or = 0
    total_time_xor = 0
    total_rows = 0

    with open('logic.csv', newline='') as csvfile2:
        csvreader = csv.DictReader(csvfile2)
        
        for row in csvreader:
            total_time_not += float(row['time_not'])
            total_time_and += float(row['time_and'])
            total_time_or += float(row['time_or'])
            total_time_xor += float(row['time_xor'])
            total_rows += 1

    avg_time_not = total_time_not / total_rows
    avg_time_and = total_time_and / total_rows
    avg_time_or = total_time_or / total_rows
    avg_time_xor = total_time_xor / total_rows

    avg_of_averages = (avg_time_not + avg_time_and + avg_time_or + avg_time_xor) / 4

    scoreL = (
        10 if avg_of_averages <= 3 else
        9 if avg_of_averages <= 4 else
        8 if avg_of_averages <= 5 else
        7 if avg_of_averages <= 6 else
        6 if avg_of_averages <= 8 else
        5 if avg_of_averages <= 10 else
        4 if avg_of_averages <= 12 else
        3 if avg_of_averages <= 14 else
        2 if avg_of_averages <= 15 else
        1
    )

    total_read_speed = 0
    total_write_speed = 0
    total_rows = 0

    with open('data.csv', newline='') as csvfile3:
        csvreader = csv.DictReader(csvfile3)
        
        for row in csvreader:
            total_read_speed += float(row['read_speed'])
            total_write_speed += float(row['write_speed'])
            total_rows += 1

    avg_read_speed = total_read_speed / total_rows
    avg_write_speed = total_write_speed / total_rows

    avg_disk_transfer_speed = (avg_read_speed + avg_write_speed) / 2

    scoreD = (
        10 if avg_disk_transfer_speed >= 225 else
        9 if avg_disk_transfer_speed >= 200 else
        8 if avg_disk_transfer_speed >= 175 else
        7 if avg_disk_transfer_speed >= 150 else
        6 if avg_disk_transfer_speed >= 125 else
        5 if avg_disk_transfer_speed >= 100 else
        4 if avg_disk_transfer_speed >= 75 else
        3 if avg_disk_transfer_speed >= 50 else
        2 if avg_disk_transfer_speed >= 25 else
        1
    )

    total_read_speed_ram = 0
    total_write_speed_ram = 0
    total_rows_ram = 0

    with open('ram.csv', newline='') as csvfile4:
        csvreader = csv.DictReader(csvfile4)
        
        for row in csvreader:
            read_speed = float(row['read_speed']) if row['read_speed'] != 'inf' else 0
            write_speed = float(row['write_speed']) if row['write_speed'] != 'inf' else 0
            
            total_read_speed_ram += read_speed
            total_write_speed_ram += write_speed
            total_rows_ram += 1

    avg_read_speed_ram = total_read_speed_ram / total_rows_ram
    avg_write_speed_ram = total_write_speed_ram / total_rows_ram

    avg_ram_transfer_speed = (avg_read_speed_ram + avg_write_speed_ram) / 2

    scoreR = (
        10 if avg_ram_transfer_speed >= 15000 else
        9 if avg_ram_transfer_speed >= 13000 else
        8 if avg_ram_transfer_speed >= 11000 else
        7 if avg_ram_transfer_speed >= 9000 else
        6 if avg_ram_transfer_speed >= 7000 else
        5 if avg_ram_transfer_speed >= 5000 else
        4 if avg_ram_transfer_speed >= 3000 else
        3 if avg_ram_transfer_speed >= 2000 else
        2 if avg_ram_transfer_speed >= 1000 else
        1
    )

    total_execution_time = 0
    total_rows_prime = 0

    with open('prime.csv', newline='') as csvfile5:
        csvreader = csv.DictReader(csvfile5)
        
        for row in csvreader:
            total_execution_time += float(row['execution_time'])
            total_rows_prime += 1

    avg_execution_time = total_execution_time / total_rows_prime

    scoreS = (
        10 if avg_execution_time <= 500 else
        9 if avg_execution_time <= 1000 else
        8 if avg_execution_time <= 1500 else
        7 if avg_execution_time <= 1750 else
        6 if avg_execution_time <= 1900 else
        5 if avg_execution_time <= 2000 else
        4 if avg_execution_time <= 3000 else
        3 if avg_execution_time <= 4000 else
        2 if avg_execution_time <= 5000 else
        1
    )

    final_score = round((scoreA + scoreD + scoreL + scoreR + scoreS) / 5)
    return final_score, (scoreA, scoreL, scoreD, scoreR, scoreS)
