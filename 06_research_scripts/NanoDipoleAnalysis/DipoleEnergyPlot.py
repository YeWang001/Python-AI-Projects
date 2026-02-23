import pandas as pd
from matplotlib import pyplot as plt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    'font.family': 'DejaVu Sans',      
    'font.size': 14,
    'axes.linewidth': 1.2,
    'axes.labelweight': 'bold',
    'axes.titlesize': 16,
    'legend.frameon': True,
    'legend.framealpha': 0.9,
    'legend.edgecolor': 'gray',
    'legend.fontsize': 12,
    'grid.linestyle': '--',
    'grid.alpha': 0.5
})

data_files = {
    'a': os.path.join(script_dir, 'data', 'Cu_300_dipoles.xlsx'),
    'b': os.path.join(script_dir, 'data', 'Au_300_dipoles.xlsx'),
    'c': os.path.join(script_dir, 'data', 'Pd_300_dipoles.xlsx'),
    'd': os.path.join(script_dir, 'data', 'Cu_dipoles.xlsx'),
    'e': os.path.join(script_dir, 'data', 'Au_dipoles.xlsx'),
    'f': os.path.join(script_dir, 'data', 'Pd_dipoles.xlsx')
}

def plotFigures (caseLettersToPlot, figureFileName):
    
    # read data from Excel files
    df = pd.read_excel(data_files[caseLettersToPlot], usecols=['Index','Dipole moment', 'Potential energy'])
    # Series, no need to add (x.values, dipole.values, potential.values)

    # Extract data columns
    x = df['Index']
    dipole = df['Dipole moment']
    potential = df['Potential energy'] 

    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    # Left:(Dipole Moment)
    ax1.scatter(x, dipole, label='Dipole Moment', color = 'b')
    
    ax1.set_xlabel('Time (fs)', fontweight='bold')
    ax1.set_ylabel('Dipole Moments (eÅ)', color = 'b', fontweight='bold')
    
    ax1.tick_params(axis='x', labelbottom=False)
    ax1.grid(True)
    
    # Set left axis range based on maximum dipole value
    max_dipole = dipole.abs().max()
    ax1.set_ylim(-max_dipole-0.1, max_dipole+0.1)
    
    # Right:(Potential Energy)
    ax2 = ax1.twinx()
    ax2.scatter(x, potential, label='Potential Energy', color = 'g')
    
    ax2.set_ylabel('Potential Energy (eV)', color = 'g', fontweight='bold')
    
    # Extend right axis range
    min_energy, max_energy = potential.min(), potential.max()
    ax2.set_ylim(min_energy - 20, max_energy + 10)
    
    handles, labels = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles + handles2, labels + labels2)
    
    ax1.set_title('Time Evolution of Dipole Moments and Potential Energy', fontweight='bold')
        
    plt.savefig(figureFileName)
    plt.show()
    
for i in data_files.keys():
    plotFigures(i, f'Figure{i}.png')

        
