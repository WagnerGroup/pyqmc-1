# This must be done BEFORE importing numpy or anything else.
# Therefore it must be in your main script.
import os

os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
import pandas as pd
from pyscf import lib, gto, scf
from pyqmc import slater_jastrow, line_minimization, initial_guess, gradient_generator


def test():
    """ Optimize a Helium atom's wave function and check that it's 
    better than Hartree-Fock"""

    mol = gto.M(atom="He 0. 0. 0.", basis="bfd_vdz", ecp="bfd", unit="bohr")
    mf = scf.RHF(mol).run()
    wf = slater_jastrow(mol, mf)
    nconf = 500
    wf, dfgrad, dfline = line_minimization(
        wf, initial_guess(mol, nconf), gradient_generator(mol, wf)
    )
    dfgrad = pd.DataFrame(dfgrad)
    mfen = mf.energy_tot()
    enfinal = dfgrad["en"].values[-1]
    enfinal_err = dfgrad["en_err"].values[-1]
    assert mfen > enfinal


if __name__ == "__main__":
    test()
