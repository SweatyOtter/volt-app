import tkinter as tk                                                                                                                                          │
│  from tkinter import ttk, messagebox, scrolledtext, simpledialog                                                                                               │
│  import boto3                                                                                                                                                  │
│  import json                                                                                                                                                   │
│  from datetime import datetime                                                                                                                                 │
│                                                                                                                                                                │
│  class VoltApp:                                                                                                                                                │
│      def __init__(self, root):                                                                                                                                 │
│          self.root = root                                                                                                                                      │
│          self.root.title("Volt - Electronics Repair Assistant")                                                                                                │
│          self.root.geometry("1200x800")                                                                                                                        │
│                                                                                                                                                                │
│          try:                                                                                                                                                  │
│              self.lambda_client = boto3.client('lambda', region_name='us-west-2')                                                                              │
│              self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2')                                                                               │
│              self.table = self.dynamodb.Table('RepairSessions')                                                                                                │
│          except Exception as e:                                                                                                                                │
│              messagebox.showerror("AWS Error", f"Failed to connect to AWS: {str(e)}")                                                                          │
│              return                                                                                                                                            │
│                                                                                                                                                                │
│          self.current_session_id = None                                                                                                                        │
│          self.create_ui()                                                                                                                                      │
│                                                                                                                                                                │
│      def create_ui(self):                                                                                                                                      │
│          self.root.columnconfigure(0, weight=1)                                                                                                                │
│          self.root.rowconfigure(1, weight=1)                                                                                                                   │
│                                                                                                                                                                │
│          header = ttk.Frame(self.root)                                                                                                                         │
│          header.pack(fill=tk.X, padx=10, pady=10)                                                                                                              │
│          ttk.Label(header, text="VOLT - Electronics Repair Assistant", font=("Arial", 18, "bold")).pack()                                                      │
│          ttk.Label(header, text="WT330/WT405 Power Amplifier Troubleshooting").pack()                                                                          │
│                                                                                                                                                                │
│          self.notebook = ttk.Notebook(self.root)                                                                                                               │
│          self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)                                                                                       │
│                                                                                                                                                                │
│          self.session_tab = ttk.Frame(self.notebook)                                                                                                           │
│          self.notebook.add(self.session_tab, text="Session")                                                                                                   │
│          self.create_session_tab()                                                                                                                             │
│                                                                                                                                                                │
│          self.measurements_tab = ttk.Frame(self.notebook)                                                                                                      │
│          self.notebook.add(self.measurements_tab, text="Measurements")                                                                                         │
│          self.create_measurements_tab()                                                                                                                        │
│                                                                                                                                                                │
│          self.analysis_tab = ttk.Frame(self.notebook)                                                                                                          │
│          self.notebook.add(self.analysis_tab, text="Analysis")                                                                                                 │
│          self.create_analysis_tab()                                                                                                                            │
│                                                                                                                                                                │
│          self.troubleshooting_tab = ttk.Frame(self.notebook)                                                                                                   │
│          self.notebook.add(self.troubleshooting_tab, text="Troubleshooting")                                                                                   │
│          self.create_troubleshooting_tab()                                                                                                                     │
│                                                                                                                                                                │
│          self.schematic_tab = ttk.Frame(self.notebook)                                                                                                         │
│          self.notebook.add(self.schematic_tab, text="Schematics")                                                                                              │
│          self.create_schematic_tab()                                                                                                                           │
│                                                                                                                                                                │
│      def create_session_tab(self):                                                                                                                             │
│          frame = ttk.LabelFrame(self.session_tab, text="Create New Repair Session", padding=15)                                                                │
│          frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)                                                                                               │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Device Model:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=10)                                        │
│          self.device_var = tk.StringVar(value="WT405")                                                                                                         │
│          ttk.Combobox(frame, textvariable=self.device_var, values=["WT330", "WT405"], state="readonly", width=20).grid(row=0, column=1, sticky=tk.W, pady=10)  │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Serial Number:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=10)                                       │
│          self.serial_var = tk.StringVar()                                                                                                                      │
│          ttk.Entry(frame, textvariable=self.serial_var, width=25).grid(row=1, column=1, sticky=tk.W, pady=10)                                                  │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Symptom Description:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.NW, pady=10)                                │
│          self.symptom_text = tk.Text(frame, height=5, width=40, wrap=tk.WORD)                                                                                  │
│          self.symptom_text.grid(row=2, column=1, sticky=tk.EW, pady=10)                                                                                        │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Technician Name:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=10)                                     │
│          self.tech_var = tk.StringVar(value="jaymc")                                                                                                           │
│          ttk.Entry(frame, textvariable=self.tech_var, width=25).grid(row=3, column=1, sticky=tk.W, pady=10)                                                    │
│                                                                                                                                                                │
│          button_frame = ttk.Frame(frame)                                                                                                                       │
│          button_frame.grid(row=4, column=0, columnspan=2, pady=20)                                                                                             │
│          ttk.Button(button_frame, text="Create Session", command=self.create_session, width=20).pack(side=tk.LEFT, padx=5)                                     │
│          ttk.Button(button_frame, text="Load Session", command=self.load_session, width=20).pack(side=tk.LEFT, padx=5)                                         │
│                                                                                                                                                                │
│          ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)                                                  │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Current Session:", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky=tk.W, pady=10)                                     │
│          self.session_status = tk.StringVar(value="No active session")                                                                                         │
│          ttk.Label(frame, textvariable=self.session_status, foreground="blue", font=("Arial", 10)).grid(row=6, column=1, sticky=tk.W, pady=10)                 │
│                                                                                                                                                                │
│          frame.columnconfigure(1, weight=1)                                                                                                                    │
│                                                                                                                                                                │
│      def create_measurements_tab(self):                                                                                                                        │
│          frame = ttk.LabelFrame(self.measurements_tab, text="Log Circuit Measurements", padding=15)                                                            │
│          frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)                                                                                               │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Test Point:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)                                            │
│          self.test_point_var = tk.StringVar()                                                                                                                  │
│          test_points = ["power_supply_rail_pos", "power_supply_rail_neg", "preamp_input", "preamp_output", "power_amp_output", "Q1_base", "Q1_collector",      │
│  "bias_voltage"]                                                                                                                                               │
│          ttk.Combobox(frame, textvariable=self.test_point_var, values=test_points, state="readonly", width=25).grid(row=0, column=1, sticky=tk.W, pady=5)      │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Measured Value:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)                                        │
│          self.value_var = tk.StringVar()                                                                                                                       │
│          ttk.Entry(frame, textvariable=self.value_var, width=25).grid(row=1, column=1, sticky=tk.W, pady=5)                                                    │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Unit:", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)                                                  │
│          self.unit_var = tk.StringVar(value="V")                                                                                                               │
│          ttk.Entry(frame, textvariable=self.unit_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=5)                                                     │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Expected Value:", font=("Arial", 9, "bold")).grid(row=3, column=0, sticky=tk.W, pady=5)                                        │
│          self.expected_var = tk.StringVar()                                                                                                                    │
│          ttk.Entry(frame, textvariable=self.expected_var, width=25).grid(row=3, column=1, sticky=tk.W, pady=5)                                                 │
│                                                                                                                                                                │
│          ttk.Button(frame, text="Log Measurement", command=self.log_measurement, width=20).grid(row=4, column=0, columnspan=2, pady=15)                        │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Recent Measurements:", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))              │
│          self.measurements_text = scrolledtext.ScrolledText(frame, height=10, width=80)                                                                        │
│          self.measurements_text.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW, pady=5)                                                                    │
│                                                                                                                                                                │
│          frame.columnconfigure(1, weight=1)                                                                                                                    │
│          frame.rowconfigure(6, weight=1)                                                                                                                       │
│                                                                                                                                                                │
│      def create_analysis_tab(self):                                                                                                                            │
│          frame = ttk.LabelFrame(self.analysis_tab, text="Circuit Analysis", padding=15)                                                                        │
│          frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)                                                                                               │
│                                                                                                                                                                │
│          button_frame = ttk.Frame(frame)                                                                                                                       │
│          button_frame.pack(fill=tk.X, pady=10)                                                                                                                 │
│          ttk.Button(button_frame, text="Run Fault Correlation", command=self.run_fault_analysis, width=20).pack(side=tk.LEFT, padx=5)                          │
│          ttk.Button(button_frame, text="Run Circuit Reasoning", command=self.run_circuit_reasoning, width=20).pack(side=tk.LEFT, padx=5)                       │
│          ttk.Button(button_frame, text="Clear", command=lambda: self.analysis_text.delete("1.0", tk.END), width=10).pack(side=tk.LEFT, padx=5)                 │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Analysis Results:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))                                                │
│          self.analysis_text = scrolledtext.ScrolledText(frame, height=20, width=100, wrap=tk.WORD)                                                             │
│          self.analysis_text.pack(fill=tk.BOTH, expand=True, pady=5)                                                                                            │
│                                                                                                                                                                │
│      def create_troubleshooting_tab(self):                                                                                                                     │
│          frame = ttk.LabelFrame(self.troubleshooting_tab, text="Troubleshooting Guide", padding=15)                                                            │
│          frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)                                                                                               │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Symptom:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)                                              │
│          self.symptom_combo_var = tk.StringVar()                                                                                                               │
│          ttk.Combobox(frame, textvariable=self.symptom_combo_var, values=["no_output", "distortion", "low_gain", "hum"], state="readonly",                     │
│  width=20).grid(row=0, column=1, sticky=tk.W, pady=5)                                                                                                          │
│                                                                                                                                                                │
│          ttk.Button(frame, text="Get Troubleshooting Steps", command=self.get_troubleshooting_steps, width=25).grid(row=1, column=0, columnspan=2, pady=15)    │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Recommended Steps:", font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))                │
│          self.troubleshooting_text = scrolledtext.ScrolledText(frame, height=15, width=100, wrap=tk.WORD)                                                      │
│          self.troubleshooting_text.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, pady=5)                                                                 │
│                                                                                                                                                                │
│          frame.columnconfigure(1, weight=1)                                                                                                                    │
│          frame.rowconfigure(3, weight=1)                                                                                                                       │
│                                                                                                                                                                │
│      def create_schematic_tab(self):                                                                                                                           │
│          frame = ttk.LabelFrame(self.schematic_tab, text="Schematic Retrieval", padding=15)                                                                    │
│          frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)                                                                                               │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Device:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=10)                                              │
│          self.schem_device_var = tk.StringVar(value="Eden-Electronics")                                                                                        │
│          ttk.Entry(frame, textvariable=self.schem_device_var, width=25).grid(row=0, column=1, sticky=tk.W, pady=10)                                            │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Schematic:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=10)                                           │
│          self.schem_name_var = tk.StringVar(value="WT330-Schematic-2003")                                                                                      │
│          ttk.Combobox(frame, textvariable=self.schem_name_var, values=["WT330-Schematic-2003", "WT405-Schematic"], state="readonly", width=25).grid(row=1,     │
│  column=1, sticky=tk.W, pady=10)                                                                                                                               │
│                                                                                                                                                                │
│          ttk.Button(frame, text="Retrieve Schematic", command=self.retrieve_schematic, width=20).grid(row=2, column=0, columnspan=2, pady=15)                  │
│                                                                                                                                                                │
│          ttk.Label(frame, text="Schematic Info:", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))                   │
│          self.schematic_text = scrolledtext.ScrolledText(frame, height=12, width=100, wrap=tk.WORD)                                                            │
│          self.schematic_text.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW, pady=5)                                                                       │
│                                                                                                                                                                │
│          frame.columnconfigure(1, weight=1)                                                                                                                    │
│          frame.rowconfigure(4, weight=1)                                                                                                                       │
│                                                                                                                                                                │
│      def create_session(self):                                                                                                                                 │
│          if self.current_session_id:                                                                                                                           │
│              messagebox.showinfo("Info", f"Session active: {self.current_session_id}")                                                                         │
│              return                                                                                                                                            │
│                                                                                                                                                                │
│          device = self.device_var.get()                                                                                                                        │
│          symptom = self.symptom_text.get("1.0", tk.END).strip()                                                                                                │
│          tech = self.tech_var.get()                                                                                                                            │
│                                                                                                                                                                │
│          if not device or not symptom or not tech:                                                                                                             │
│              messagebox.showerror("Error", "Fill in Device, Symptom, Technician")                                                                              │
│              return                                                                                                                                            │
│                                                                                                                                                                │
│          try:                                                                                                                                                  │
│              payload = {                                                                                                                                       │
│                  "operation": "create",                                                                                                                        │
│                  "session_data": {                                                                                                                             │
│                      "device_model": device,                                                                                                                   │
│                      "symptom_description": symptom,                                                                                                           │
│                      "technician_name": tech                                                                                                                   │
│                  }                                                                                                                                             │
│              }                                                                                                                                                 │
│                                                                                                                                                                │
│              response = self.lambda_client.invoke(                                                                                                             │
│                  FunctionName='volt-repair-session-crud',                                                                                                      │
│                  InvocationType='RequestResponse',                                                                                                             │
│                  Payload=json.dumps(payload)                                                                                                                   │
│              )                                                                                                                                                 │
│                                                                                                                                                                │
│              result = json.loads(response['Payload'].read().decode())                                                                                          │
│              body = json.loads(result['body'])                                                                                                                 │
│                                                                                                                                                                │
│              self.current_session_id = body['session_id']                                                                                                      │
│              self.session_status.set(f"Active: {self.current_session_id}")                                                                                     │
│              messagebox.showinfo("Success", f"Session: {self.current_session_id}")                                                                             │
│          except Exception as e:                                                                                                                                │
│              messagebox.showerror("Error", str(e))                                                                                                             │
│                                                                                                                                                                │
│      def load_session(self):                                                                                                                                   │
│          sid = simpledialog.askstring("Load", "Session ID:")                                                                                                   │
│          if sid:                                                                                                                                               │
│              self.current_session_id = sid                                                                                                                     │
│              self.session_status.set(f"Loaded: {sid}")                                                                                                         │
│                                                                                                                                                                │
│      def log_measurement(self):                                                                                                                                │
│          if not self.current_session_id:                                                                                                                       │
│              messagebox.showerror("Error", "No active session")                                                                                                │
│              return                                                                                                                                            │
│                                                                                                                                                                │
│          tp = self.test_point_var.get()                                                                                                                        │
│          val = self.value_var.get()                                                                                                                            │
│          unit = self.unit_var.get()                                                                                                                            │
│          exp = self.expected_var.get()                                                                                                                         │
│                                                                                                                                                                │
│          if not all([tp, val, unit]):                                                                                                                          │
│              messagebox.showerror("Error", "Fill all fields")                                                                                                  │
│              return                                                                                                                                            │
│                                                                                                                                                                │
│          try:                                                                                                                                                  │
│              payload = {                                                                                                                                       │
│                  "session_id": self.current_session_id,                                                                                                        │
│                  "test_point": tp,                                                                                                                             │
│                  "measurement_type": "voltage_DC",                                                                                                             │
│                  "measured_value": float(val),                                                                                                                 │
│                  "unit": unit,                                                                                                                                 │
│                  "expected_value": exp                                                                                                                         │
│              }                                                                                                                                                 │
│                                                                                                                                                                │
│              self.lambda_client.invoke(                                                                                                                        │
│                  FunctionName='volt-measurement-logger',                                                                                                       │
│                  InvocationType='RequestResponse',                                                                                                             │
│                  Payload=json.dumps(payload)                                                                                                                   │
│              )                                                                                                                                                 │
│                                                                                                                                                                │
│              ts = datetime.now().strftime("%H:%M:%S")                                                                                                          │
│              self.measurements_text.insert(tk.END, f"[{ts}] {tp}: {val}{unit} (exp: {exp})\n")                                                                 │
│              self.measurements_text.see(tk.END)                                                                                                                │
│              self.test_point_var.set("")                                                                                                                       │
│              self.value_var.set("")                                                                                                                            │
│              messagebox.showinfo("Success", "Measurement logged")                                                                                              │
│          except Exception as e:                                                                                                                                │
│              messagebox.showerror("Error", str(e))                                                                                                             │
│                                                                                                                                                                │
│      def run_fault_analysis(self):                                                                                                                             │
│          if not self.current_session_id:                                                                                                                       │
│              messagebox.showerror("Error", "No active session")                                                                                                │
│              return                                                                                                                                            │
│                                                                                                                                                                │
│          try:                                                                                                                                                  │
│              payload = {                                                                                                                                       │
│                  "session_id": self.current_session_id,                                                                                                        │
│                  "device_model": self.device_var.get()                                                                                                         │
│              }                                                                                                                                                 │
│                                                                                                                                                                │
│              response = self.lambda_client.invoke(                                                                                                             │
│                  FunctionName='volt-fault-correlation',                                                                                                        │
│                  InvocationType='RequestResponse',                                                                                                             │
│                  Payload=json.dumps(payload)                                                                                                                   │
│              )                                                                                                                                                 │
│                                                                                                                                                                │
│              result = json.loads(response['Payload'].read().decode())                                                                                          │
│              body = json.loads(result['body'])                                                                                                                 │
│                                                                                                                                                                │
│              self.analysis_text.delete("1.0", tk.END)                                                                                                          │
│              self.analysis_text.insert(tk.END, "FAULT CORRELATION ANALYSIS\n")                                                                                 │
│              self.analysis_text.insert(tk.END, "="*80 + "\n\n")                                                                                                │
│              self.analysis_text.insert(tk.END, f"Measurements: {body.get('measurements_analyzed', 0)}\n\n")                                                    │
│                                                                                                                                                                │
│              for i, cand in enumerate(body.get('root_cause_candidates', []), 1):                                                                               │
│                  self.analysis_text.insert(tk.END, f"Candidate {i}:\n")                                                                                        │
│                  self.analysis_text.insert(tk.END, f"  Cause: {cand.get('cause')}\n")                                                                          │
│                  self.analysis_text.insert(tk.END, f"  Confidence: {cand.get('confidence', 0)*100:.0f}%\n\n")                                                  │
│          except Exception as e:                                                                                                                                │
│              self.analysis_text.delete("1.0", tk.END)                                                                                                          │
│              self.analysis_text.insert(tk.END, f"Error: {str(e)}")                                                                                             │
│                                                                                                                                                                │
│      def run_circuit_reasoning(self):                                                                                                                          │
│          if not self.current_session_id:                                                                                                                       │
│              messagebox.showerror("Error", "No active session")                                                                                                │
│              return                                                                                                                                            │
│                                                                                                                                                                │
│          try:                                                                                                                                                  │
│              self.analysis_text.delete("1.0", tk.END)                                                                                                          │
│              self.analysis_text.insert(tk.END, "Running Claude Analysis...\n")                                                                                 │
│              self.root.update()                                                                                                                                │
│                                                                                                                                                                │
│              payload = {                                                                                                                                       │
│                  "session_id": self.current_session_id,                                                                                                        │
│                  "device_model": self.device_var.get()                                                                                                         │
│              }                                                                                                                                                 │
│                                                                                                                                                                │
│              response = self.lambda_client.invoke(                                                                                                             │
│                  FunctionName='volt-circuit-reasoning',                                                                                                        │
│                  InvocationType='RequestResponse',                                                                                                             │
│                  Payload=json.dumps(payload)                                                                                                                   │
│              )                                                                                                                                                 │
│                                                                                                                                                                │
│              result = json.loads(response['Payload'].read().decode())                                                                                          │
│              body = json.loads(result['body'])                                                                                                                 │
│                                                                                                                                                                │
│              self.analysis_text.delete("1.0", tk.END)                                                                                                          │
│              self.analysis_text.insert(tk.END, "CLAUDE CIRCUIT ANALYSIS\n")                                                                                    │
│              self.analysis_text.insert(tk.END, "="*80 + "\n\n")                                                                                                │
│              self.analysis_text.insert(tk.END, f"Root Cause: {body.get('root_cause', 'TBD')}\n\n")                                                             │
│                                                                                                                                                                │
│              self.analysis_text.insert(tk.END, "Components:\n")                                                                                                │
│              for c in body.get('probable_failed_components', []):                                                                                              │
│                  self.analysis_text.insert(tk.END, f"  - {c}\n")                                                                                               │
│                                                                                                                                                                │
│              self.analysis_text.insert(tk.END, "\nRepairs:\n")                                                                                                 │
│              for r in body.get('recommended_repairs', []):                                                                                                     │
│                  self.analysis_text.insert(tk.END, f"  - {r}\n")                                                                                               │
│                                                                                                                                                                │
│              self.analysis_text.insert(tk.END, "\nWarnings:\n")                                                                                                │
│              for w in body.get('safety_warnings', []):                                                                                                         │
│                  self.analysis_text.insert(tk.END, f"  WARNING: {w}\n")                                                                                        │
│          except Exception as e:                                                                                                                                │
│              self.analysis_text.delete("1.0", tk.END)                                                                                                          │
│              self.analysis_text.insert(tk.END, f"Error: {str(e)}")                                                                                             │
│                                                                                                                                                                │
│      def get_troubleshooting_steps(self):                                                                                                                      │
│          sym = self.symptom_combo_var.get()                                                                                                                    │
│          dev = self.device_var.get()                                                                                                                           │
│                                                                                                                                                                │
│          if not sym or not dev:                                                                                                                                │
│              messagebox.showerror("Error", "Select device and symptom")                                                                                        │
│              return                                                                                                                                            │
│                                                                                                                                                                │
│          try:                                                                                                                                                  │
│              payload = {"device_model": dev, "symptom": sym}                                                                                                   │
│                                                                                                                                                                │
│              response = self.lambda_client.invoke(                                                                                                             │
│                  FunctionName='volt-troubleshooting-workflow',                                                                                                 │
│                  InvocationType='RequestResponse',                                                                                                             │
│                  Payload=json.dumps(payload)                                                                                                                   │
│              )                                                                                                                                                 │
│                                                                                                                                                                │
│              result = json.loads(response['Payload'].read().decode())                                                                                          │
│              body = json.loads(result['body'])                                                                                                                 │
│                                                                                                                                                                │
│              self.troubleshooting_text.delete("1.0", tk.END)                                                                                                   │
│              self.troubleshooting_text.insert(tk.END, f"TROUBLESHOOTING: {body.get('description')}\n")                                                         │
│              self.troubleshooting_text.insert(tk.END, "="*80 + "\n\n")                                                                                         │
│                                                                                                                                                                │
│              for step in body.get('steps', []):                                                                                                                │
│                  self.troubleshooting_text.insert(tk.END, f"Step {step.get('step')}: {step.get('description')}\n")                                             │
│                  self.troubleshooting_text.insert(tk.END, f"  Test: {step.get('test_point')}\n\n")                                                             │
│          except Exception as e:                                                                                                                                │
│              self.troubleshooting_text.delete("1.0", tk.END)                                                                                                   │
│              self.troubleshooting_text.insert(tk.END, f"Error: {str(e)}")                                                                                      │
│                                                                                                                                                                │
│      def retrieve_schematic(self):                                                                                                                             │
│          dev = self.schem_device_var.get()                                                                                                                     │
│          sch = self.schem_name_var.get()                                                                                                                       │
│                                                                                                                                                                │
│          if not dev or not sch:                                                                                                                                │
│              messagebox.showerror("Error", "Fill device and schematic")                                                                                        │
│              return                                                                                                                                            │
│                                                                                                                                                                │
│          try:                                                                                                                                                  │
│              payload = {"device_model": dev, "sheet_name": sch}                                                                                                │
│                                                                                                                                                                │
│              response = self.lambda_client.invoke(                                                                                                             │
│                  FunctionName='volt-retrieve-schematic',                                                                                                       │
│                  InvocationType='RequestResponse',                                                                                                             │
│                  Payload=json.dumps(payload)                                                                                                                   │
│              )                                                                                                                                                 │
│                                                                                                                                                                │
│              result = json.loads(response['Payload'].read().decode())                                                                                          │
│              body = json.loads(result['body'])                                                                                                                 │
│                                                                                                                                                                │
│              self.schematic_text.delete("1.0", tk.END)                                                                                                         │
│              self.schematic_text.insert(tk.END, "SCHEMATIC RETRIEVED\n")                                                                                       │
│              self.schematic_text.insert(tk.END, "="*80 + "\n\n")                                                                                               │
│              self.schematic_text.insert(tk.END, f"Device: {body.get('device_model')}\n")                                                                       │
│              self.schematic_text.insert(tk.END, f"Sheet: {body.get('sheet_name')}\n")                                                                          │
│              self.schematic_text.insert(tk.END, f"Size: {body.get('size_bytes')} bytes\n\n")                                                                   │
│              self.schematic_text.insert(tk.END, f"URL: {body.get('presigned_url')}\n")                                                                         │
│              messagebox.showinfo("Success", "Schematic retrieved")                                                                                             │
│          except Exception as e:                                                                                                                                │
│              self.schematic_text.insert(tk.END, f"Error: {str(e)}")                                                                                            │
│                                                                                                                                                                │
│  if __name__ == "__main__":                                                                                                                                    │
│      root = tk.Tk()                                                                                                                                            │
│      app = VoltApp(root)                                                                                                                                       │
│      root.mainloop()   
