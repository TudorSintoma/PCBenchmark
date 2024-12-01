import tkinter as tk
from tkinter import Toplevel
import psutil
import platform
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from BenchmarkControl import calculate_score, run_ram_benchmark, run_arithmetic_benchmark, run_logic_benchmark, run_data_benchmark, run_sieve_benchmark
from PIL import Image, ImageTk
from Common import sieve_is_running, ram_is_running, data_is_running, aritm_is_running, logic_is_running

# Colors
WHITE = "#FFFFFF"
GREY = "#808080"
BLUE = "#007ba7"
ORANGE = "#FFA500"
CRIMSON = "#DC143C"
ROYAL_BLUE = "#4169E1"
PINE_GREEN = "#01796F"
PURPLE = "#800080"

count = [1]
data = {'time': [], 'cpu usage': [], 'ram usage': []}
benchmark_data = {'time': [], 'cpu usage': [], 'ram usage': []}

plot_sieve = False
plot_aritmetic =False
plot_logic = False
plot_data = False
plot_ram = False

class CircularProgressBar(tk.Frame):
    def __init__(self, master, radius=50, name="Resource", color="blue"):
        super().__init__(master, bg="black")
        self.name = name
        self.color = color
        self.radius = radius
        self.progress = 0
        self.canvas = tk.Canvas(self, width=radius*2, height=radius*2, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.label = tk.Label(self, text=f"{self.name} Usage: 0%", fg="white", bg="black", font=("Helvetica", 14))
        self.label.pack(pady=10)
        self.draw_circle()

    def draw_circle(self):
        self.canvas.delete("all")
        self.canvas.create_oval(10, 10, 2*self.radius-10, 2*self.radius-10, fill='lightgray', outline='')
        if self.progress > 0:
            angle = (self.progress / 100) * 360
            self.canvas.create_arc(10, 10, 2*self.radius-10, 2*self.radius-10, start=90, extent=-angle, fill=self.color, outline='')

    def set_progress(self, value):
        if 0 <= value <= 100:
            self.progress = value
            self.draw_circle()
            self.label.config(text=f"{self.name} Usage: {self.progress}%")

def update_cpu_usage(cpu_bar):
    global count
    global sieve_is_running, aritm_is_running, logic_is_running, data_is_running, ram_is_running, plot_data, plot_aritmetic, plot_logic, plot_ram, plot_sieve

    if not any([sieve_is_running.is_set(), aritm_is_running.is_set(), logic_is_running.is_set(), data_is_running.is_set(), ram_is_running.is_set()]):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent

        data['time'].append(count[0])
        data['cpu usage'].append(cpu_usage)
        data['ram usage'].append(ram_usage)
        count[0] += 1

        cpu_bar.set_progress(cpu_usage)

        figure_plot_cpu.clear()
        figure_plot_ram.clear()

        figure_plot_cpu.set_title('CPU Usage')
        figure_plot_cpu.tick_params(axis='x')
        figure_plot_cpu.tick_params(axis='y')

        figure_plot_ram.set_title('RAM Usage')
        figure_plot_ram.tick_params(axis='x')
        figure_plot_ram.tick_params(axis='y')

        figure_plot_cpu.plot(data['time'], data['cpu usage'], color='blue', label="CPU Usage")
        figure_plot_ram.plot(data['time'], data['ram usage'], color='green', label="RAM Usage")

        if plot_sieve == True:
            figure_plot_cpu.plot(benchmark_data['time'], benchmark_data['cpu usage'], color='red', label="Sieve Benchmark CPU Usage")
            figure_plot_ram.plot(benchmark_data['time'], benchmark_data['ram usage'], color='red', label="Sieve Benchmark RAM Usage")

        if plot_aritmetic == True:
            figure_plot_cpu.plot(benchmark_data['time'], benchmark_data['cpu usage'], color='red', label="Aritmetic Operations Benchmark CPU Usage")
            figure_plot_ram.plot(benchmark_data['time'], benchmark_data['ram usage'], color='red', label="Aritmetic Operations Benchmark RAM Usage")

        if plot_logic == True:
            figure_plot_cpu.plot(benchmark_data['time'], benchmark_data['cpu usage'], color='red', label="Logic Operations Benchmark CPU Usage")
            figure_plot_ram.plot(benchmark_data['time'], benchmark_data['ram usage'], color='red', label="Logic Operations Benchmark RAM Usage")

        if plot_data == True:
            figure_plot_cpu.plot(benchmark_data['time'], benchmark_data['cpu usage'], color='red', label="DISK Data Transfer Speed Benchmark CPU Usage")
            figure_plot_ram.plot(benchmark_data['time'], benchmark_data['ram usage'], color='red', label="DISK Data Transfer Speed Benchmark RAM Usage")

        if plot_ram == True:
            figure_plot_cpu.plot(benchmark_data['time'], benchmark_data['cpu usage'], color='red', label="RAM Data Transfer Speed Benchmark CPU Usage")
            figure_plot_ram.plot(benchmark_data['time'], benchmark_data['ram usage'], color='red', label="RAM Data Transfer Speed Benchmark RAM Usage")

    line_graph.draw()
    cpu_bar.master.after(1000, update_cpu_usage, cpu_bar)

def update_ram_usage(ram_bar):
    global sieve_is_running, aritm_is_running, logic_is_running, data_is_running, ram_is_running
    if not any([sieve_is_running.is_set(), aritm_is_running.is_set(), logic_is_running.is_set(), data_is_running.is_set(), ram_is_running.is_set()]):
        ram_usage = psutil.virtual_memory().percent
        ram_bar.set_progress(ram_usage)
        ram_bar.master.after(2000, update_ram_usage, ram_bar)

def update_disk_usage(disk_bar):
   global sieve_is_running, aritm_is_running, logic_is_running, data_is_running, ram_is_running
   if not any([sieve_is_running.is_set(), aritm_is_running.is_set(), logic_is_running.is_set(), data_is_running.is_set(), ram_is_running.is_set()]):
        disk_usage = psutil.disk_usage('/').percent
        disk_bar.set_progress(disk_usage)
        disk_bar.master.after(3000, update_disk_usage, disk_bar)


def show_benchmark_options():
    benchmark_window = tk.Toplevel(root)
    benchmark_window.title("Choose Benchmarking Option")
    benchmark_window.geometry("400x400")
    benchmark_window.config(bg="black")

    def on_benchmark_selected(benchmark_option):
        global plot_sieve, plot_aritmetic, plot_logic, plot_data, plot_ram, count
        if benchmark_option == "Arithmetic Operations":
            plot_sieve = False
            plot_data = False
            plot_logic = False
            plot_ram = False
            benchmark_window.destroy()
            run_arithmetic_benchmark(figure_plot_disk, line_graph, benchmark_data, data, count)
            plot_aritmetic = True
        elif benchmark_option == "Logical Operations":
            plot_sieve = False
            plot_aritmetic = False
            plot_data = False
            plot_ram = False
            benchmark_window.destroy()
            run_logic_benchmark(figure_plot_disk, line_graph, benchmark_data, data, count)
            plot_logic = True
        elif benchmark_option == "Sieve Of Erathostenes":
            plot_data = False
            plot_aritmetic = False
            plot_logic = False
            plot_ram = False
            benchmark_window.destroy()
            run_sieve_benchmark(figure_plot_disk, line_graph, benchmark_data, data, count)
            plot_sieve = True
        elif benchmark_option == "DISK Speed":
            plot_sieve = False
            plot_aritmetic = False
            plot_logic = False
            plot_ram = False
            benchmark_window.destroy()
            run_data_benchmark(figure_plot_disk, line_graph, benchmark_data, data, count)
            plot_data = True
        elif benchmark_option == "RAM Speed":
            plot_sieve = False
            plot_aritmetic = False
            plot_logic = False
            plot_data = False
            benchmark_window.destroy()
            run_ram_benchmark(figure_plot_disk, line_graph, benchmark_data, data, count)
            plot_ram = True
        elif benchmark_option == "Clear Previous":
            plot_sieve = False
            plot_aritmetic = False
            plot_logic = False
            plot_data = False
            plot_ram = False
            figure_plot_disk.clear()


    button1 = tk.Button(benchmark_window, text="Sieve Of Erathostenes (CPU stressing)", background=ORANGE, foreground=WHITE, width=30, height=3, command=lambda: on_benchmark_selected("Sieve Of Erathostenes"))
    button1.pack(pady=5)

    button2 = tk.Button(benchmark_window, text="Arithmetic Operations", background=CRIMSON, foreground=WHITE, width=30, height=3, command=lambda: on_benchmark_selected("Arithmetic Operations"))
    button2.pack(pady=5)

    button3 = tk.Button(benchmark_window, text="Logical Operations", background=ROYAL_BLUE, foreground=WHITE, width=30, height=3, command=lambda: on_benchmark_selected("Logical Operations"))
    button3.pack(pady=5)

    button4 = tk.Button(benchmark_window, text="DISK Data Transfer Speed", background=PINE_GREEN, foreground=WHITE, width=30, height=3, command=lambda: on_benchmark_selected("DISK Speed"))
    button4.pack(pady=5)

    button5 = tk.Button(benchmark_window, text="RAM Data Transfer Speed", background="green", foreground=WHITE, width=30, height=3, command=lambda: on_benchmark_selected("RAM Speed"))
    button5.pack(pady=5)

    button6 = tk.Button(benchmark_window, text="Clear Previous", background=GREY, foreground=WHITE, width=30, height=3, command=lambda: on_benchmark_selected("Clear Previous"))
    button6.pack(pady=5)


def toggle_info(event):
    global info_expanded
    if info_expanded:
        canvas.delete("info_labels")
        canvas.create_text(675, 60, text="See PC Info...", fill="white", font=("Fixedsys", 14), tags="info")
    else:
        canvas.delete("info")
        y_position = 10
        labels = [
            f"Logical Cores: {logical_cores}",
            f"Physical Cores: {physical_cores}",
            f"Architecture: {architecture}",
            f"Processor: {processor}",
            f"Machine Type: {machine_type}",
        ]
        font_size = 9
        max_font_size = 12
        max_lines = (canvas.winfo_height() - 20) // font_size
        if len(labels) > max_lines:
            labels = labels[:max_lines]
        while y_position + len(labels) * font_size > canvas.winfo_height() and font_size < max_font_size:
            font_size += 1
        line_spacing = font_size + 10
        for label_text in labels:
            canvas.create_window(10, y_position, anchor="nw", window=tk.Label(canvas, text=label_text, fg="white", bg="black", font=("Helvetica", font_size)), tags="info_labels")
            y_position += line_spacing
    info_expanded = not info_expanded


def generate_report():
    final_score, (scoreA, scoreL, scoreD, scoreR, scoreS) = calculate_score()

    report_message = (
        f"PC Performance Report:\n\n"
        f"Arithmetic Execution Score: {scoreA}\n"
        f"Logic Execution Score: {scoreL}\n"
        f"Disk Transfer Speed Score: {scoreD}\n"
        f"RAM Transfer Speed Score: {scoreR}\n"
        f"Sieve Execution Time Score: {scoreS}\n\n"
        f"Final PC Performance Score: {final_score}"
    )
    image_path = f"{final_score}.png"

    popup = Toplevel()
    popup.title("PC Performance Report")
    popup.config(bg="black")
    popup.geometry("400x400")

    try:
        img = Image.open(image_path)
        img = img.resize((100, 100))  
        img_tk = ImageTk.PhotoImage(img) 
        
        img_label = tk.Label(popup, image=img_tk, background="black")
        img_label.image = img_tk  
        img_label.pack()

    except Exception as e:
        print(f"Error loading image: {e}")
        img = Image.open("default.png")
        img = img.resize((100, 100))  
        img_tk = ImageTk.PhotoImage(img)

        img_label = tk.Label(popup, image=img_tk, background="black")
        img_label.image = img_tk 
        img_label.pack()

    report_label = tk.Label(popup, text=report_message, foreground="white", background="black", font=("Arial", 12), justify="left")
    report_label.pack(padx=10, pady=10)

    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=5)

    popup.grab_set()
    popup.mainloop()




root = tk.Tk()
root.title("CPU-RAM-DISK Usage Monitor")
root.config(bg="black")
root.geometry("1500x750")

title = tk.Label(root, text="SYSTEM MONITOR", fg="white", bg="black", font=("Bell Gothic Std Black", 20))
title.pack(side="top", pady=20)

center_frame = tk.Frame(root, bg="black")
center_frame.pack(expand=True, fill="both", pady=10, padx=10)

progress_frame = tk.Frame(center_frame, bg="black")
progress_frame.pack(side="left", pady=10, expand=False)

cpu_bar = CircularProgressBar(progress_frame, radius=50, name="CPU", color=BLUE)
cpu_bar.pack(side="top", pady=5)

ram_bar = CircularProgressBar(progress_frame, radius=50, name="RAM", color='green')
ram_bar.pack(side="top", pady=5)

disk_bar = CircularProgressBar(progress_frame, radius=50, name="DISK", color='red')
disk_bar.pack(side="top", pady=5)

figure = plt.Figure(figsize=(15, 3), dpi=100)
figure.subplots_adjust(left=0.04, right=0.99, top=0.85, bottom=0.15)

figure_plot_cpu = figure.add_subplot(1, 3, 1)
figure_plot_ram = figure.add_subplot(1, 3, 2)
figure_plot_disk = figure.add_subplot(1, 3, 3)

figure_plot_cpu.set_ylabel("CPU Usage", rotation=0, labelpad=50, color="white", fontsize=12, ha='right')
figure_plot_ram.set_ylabel("RAM Usage", rotation=0, labelpad=50, color="white", fontsize=12, ha='right')
figure_plot_disk.set_ylabel("DISK Usage", rotation=0, labelpad=50, color="white", fontsize=12, ha='right')

figure_plot_cpu.set_title('')
figure_plot_ram.set_title('')
figure_plot_disk.set_title('')

line_graph = FigureCanvasTkAgg(figure, center_frame)
line_graph.get_tk_widget().pack(side="right", fill=tk.BOTH, expand=True)

bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(side="bottom", fill="x", pady=10)

canvas = tk.Canvas(bottom_frame, bg="black", width=700, height=120)
canvas.pack(side="left", fill="x", expand=True)

button_frame = tk.Frame(bottom_frame, bg="black")
button_frame.pack(side="right", padx=20)

button1 = tk.Button(button_frame, background=BLUE, foreground=WHITE, text="Run Benchmark", width=15, height=3, command=show_benchmark_options)
button1.pack(side="top", pady=5)

button2 = tk.Button(button_frame, background=GREY, foreground=WHITE, text="Generate Report", width=15, height=3, command=generate_report)
button2.pack(side="top", pady=5)

update_cpu_usage(cpu_bar)
update_ram_usage(ram_bar)
update_disk_usage(disk_bar)

logical_cores = psutil.cpu_count(logical=True)
physical_cores = psutil.cpu_count(logical=False)
architecture = platform.architecture()
processor = platform.processor()
machine_type = platform.machine()
info_expanded = False

canvas.create_text(675, 60, text="See PC Info...", font=("Fixedsys", 14), fill="white", tags="info")
canvas.bind("<Button-1>", lambda event: toggle_info(event))

root.mainloop()