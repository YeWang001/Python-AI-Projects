import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mb
from matplotlib import cm
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data")

colors = cm.get_cmap('tab10', 10).colors

font = 12
#mb.rcParams["text.usetex"] = True
mb.rcParams["font.size"] = font
mb.rcParams["font.family"] = "Times New Roman"
mb.rcParams["axes.labelsize"] = font
mb.rcParams["xtick.labelsize"] = font
mb.rcParams["ytick.labelsize"] = font
mb.rcParams["legend.fontsize"] = font
mb.rcParams["lines.linewidth"] = 1.5
# colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

energyFiles = {
    "a": os.path.join(data_dir, "case0.txt"),
    "b": os.path.join(data_dir, "case1.txt"),
    "f": os.path.join(data_dir, "case2.txt"),
    "c": os.path.join(data_dir, "case3.txt"),
    "g": os.path.join(data_dir, "case4.txt"),
    "e": os.path.join(data_dir, "case5.txt"),
    "d": os.path.join(data_dir, "case7.txt"),
    "h": os.path.join(data_dir, "case8.txt")
}

dipoleFiles = {
    "a": os.path.join(data_dir, "case0_dipole.txt"),
    "b": os.path.join(data_dir, "case1_dipole.txt"),
    "f": os.path.join(data_dir, "case2_dipole.txt"),
    "c": os.path.join(data_dir, "case3_dipole.txt"),
    "g": os.path.join(data_dir, "case4_dipole.txt"),
    "e": os.path.join(data_dir, "case5_dipole.txt"),
    "d": os.path.join(data_dir, "case7_dipole.txt"),
    "h": os.path.join(data_dir, "case8_dipole.txt")
}

def plotParabolas(caseLettersToPlot, figureFileName):
    """makes the whole plot for a given list of caseletters that should fit together"""
    plt.figure()
    i = 0
    for caseLetter in caseLettersToPlot:
        #read data from files
        fieldGauss, energyGauss = np.loadtxt(energyFiles[caseLetter], unpack=True, usecols=(0,1))
        fieldVasp, dipoleVasp = np.loadtxt(dipoleFiles[caseLetter], unpack=True)
        fieldVasp *= -1
        dipoleVasp*=-1
        fieldGauss *= -1.
        #get dipole fittings
        fittedPolyVasp, cov = np.polyfit(fieldVasp, dipoleVasp, 1, cov=True)
        alphaVasp = fittedPolyVasp[0]
        muVasp = fittedPolyVasp[1]
        deltaAlphaVasp = np.sqrt(cov[0,0])
        deltaMuVasp = np.sqrt(cov[1,1])
        parabolaPolyVasp = np.array([-0.5 * alphaVasp, -muVasp, 0.])
        parabolaPolyVaspUpperBound = np.array([-0.5 * (alphaVasp - deltaAlphaVasp), -muVasp + deltaMuVasp, 0.])
        parabolaPolyVaspLowBound = np.array([-0.5 * (alphaVasp + deltaAlphaVasp), -muVasp - deltaMuVasp, 0.])
        plottingField = np.linspace(0,1.5,128)
        vaspCurve = np.polyval(parabolaPolyVasp, plottingField)
        vaspUpBound = np.polyval(parabolaPolyVaspUpperBound, plottingField)
        vaspLowBound = np.polyval(parabolaPolyVaspLowBound, plottingField)
        print("\n\n case Letter : ", caseLetter)
        print("mu from VASP: %g +- %g"%(muVasp, deltaMuVasp))
        print("alpha from VASP: %g +- %g"%(alphaVasp, deltaAlphaVasp))
        # plt.fill_between(10 * plottingField, vaspUpBound, vaspLowBound, color="gray")
        # plt.plot(10 * plottingField, vaspCurve,color = colors[i], label = r'(%s) Eq.(2), $\mu, \alpha$ by VASP'%caseLetter)
        # plt.plot(10 * fieldGauss, energyGauss,"o", color = colors[i], label = '(%s) Direct (GAUSSIAN)'%caseLetter)
        # Energy fit
        fittedPolynomial, cov = np.polyfit(fieldGauss, energyGauss, 2, cov = True)
        alphaGauss = -2 * fittedPolynomial[0]
        muGauss = fittedPolynomial[1]
        deltaAlphaGauss = 2*np.sqrt(cov[0,0])
        deltaMuGauss = np.sqrt(cov[1,1])
        parabolaGauss = np.polyval(fittedPolynomial, plottingField)
        # plt.plot(10 * plottingField, parabolaGauss, "--", label = r'(%s) Eq.(2), $\mu, \alpha$ by Gaussian'%caseLetter)

        plt.plot(fieldVasp, dipoleVasp, ".", color=colors[i], label=f'{caseLetter} data')
        plt.plot(fieldVasp, muVasp + alphaVasp * fieldVasp, color=colors[i], label=f'{caseLetter} fit')

        print("mu from GAUSS: %g +- %g"%(muGauss, deltaMuGauss))
        print("alpha from GAUSS: %g +- %g"%(alphaGauss, deltaAlphaGauss))
        i += 1

    plt.legend()
    plt.xlabel('Applied Field [GV/m]')
    plt.ylabel('Field-induced energy [eV]')
    plt.savefig(figureFileName)
    plt.show()

plotParabolas("abcd", "parabola1.png")
plotParabolas("efgh", "parabolas2.png")
