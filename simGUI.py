#!/usr/bin/python

import Tkinter as tk

import battleSim as bs
import aa1941

RESULTS = """Attacker Wins Prop. {}, Avg. Rounds {}, Avg. Attacker Units Remaining {}, Avg. Defensive Units Remaining {}
Most Common Remaining Attacking Army:
{}
Most Common Remaining Defending Army:
{}
"""

class SimWindow(object):
	"""
	The GUI for the A&A 1941 sim
	"""
	
	def __init__(self):

		#keep a dictionary of fields for the unit counts
		self.fields = {}

		#build the gui
		self.rows = 2
		self.root = tk.Tk()
		self.frame = tk.Frame(self.root)
		self.simLabel = tk.Label(self.frame, text="Number of Simulations")
		self.simField = tk.Entry(self.frame)
		self.attackLabel = tk.Label(self.frame, text="Attacker")
		self.defenseLabel = tk.Label(self.frame, text="Defender")
		self.start = tk.Button(self.frame, text="Start", command=self.startSim)
		self.scroll = tk.Scrollbar(self.frame)
		self.results = tk.Text(self.frame, yscrollcommand=self.scroll.set)

		#setup the scrollbar
		self.scroll.config(command=self.results.yview)

		#do some layout
		self.frame.pack(expand=tk.YES, fill=tk.BOTH)

		self.simLabel.grid(row=0)
		self.simField.grid(row=0, column=1)
		self.attackLabel.grid(row=1, column=1)
		self.defenseLabel.grid(row=1, column=2)

		#add fields for each of the unit types
		self.buildFields(aa1941.UNITS)
		self.root.title("A&A 1941 Battle Simulator")

		#add start button and results area
		self.results.grid(row=self.rows, columnspan=3, pady=5, sticky=tk.N+tk.S+tk.W+tk.E)
		self.scroll.grid(row=self.rows, column=3, sticky=tk.N+tk.S)
		self.start.grid(row=self.rows+1, column=2, sticky=tk.E)

		#set the resize options
		#self.frame.columnconfigure(0, weight=1)
		self.frame.columnconfigure(1, weight=1)
		#self.frame.columnconfigure(2, weight=1)
		self.frame.rowconfigure(self.rows, weight=1)

		tk.mainloop()

	def startSim(self):
		"""
		Start the simulation
		"""
		#extract the unit counts from the fields
		aArmy = self.buildArmy(True)
		dArmy = self.buildArmy(False)
	
		try:
			runs = int(self.simField.get())
		except:
			runs = None

		if aArmy is not None and dArmy is not None and runs is not None:
			self.results.insert(tk.END, RESULTS.format(*bs.runSim(aArmy, dArmy, runs)))

	def buildArmy(self, attack):
		"""
		Builds an army from the data inputted in the fields
		"""
		units = []
		error = False

		#get the units
		for (name, isAttacking), field in self.fields.items():
			if attack == isAttacking:
				try:
					if len(field.get()):
						count = int(field.get())
					else:
						count = 0
				except:
					count = None
					error = True
				
				#add a unit for each of the count
				if not error:
					for i in range(count):
						units.append(bs.buildUnit(name))

		return bs.Army(units) if not error else None

	def buildFields(self, units):
		"""
		Adds fields for each of the unit types
		"""
		#add a attack and defense fields for each unit type
		for name in units:
			label = tk.Label(self.frame, text=name)
			afield = tk.Entry(self.frame)
			dfield = tk.Entry(self.frame)

			#display the components
			label.grid(row=self.rows)
			afield.grid(row=self.rows, column=1)
			dfield.grid(row=self.rows, column=2)
		
			self.rows += 1
			self.fields[(name, True)] = afield
			self.fields[(name, False)] = dfield

if __name__ == "__main__":
	SimWindow()
