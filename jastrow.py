import numpy as np



class Jastrow2B:
    """A simple Jastrow factor that is written as 
    :math:`\ln \Psi_J  = \sum_{i<j} c(r_{ij}) + \sum_k c_k \sum_{i<j} b(r_{ij})`
    c is the cusp and b are Gaussians for this implementation
    """
    def __init__(self,nconfig,mol):
        self.parameters={}
        nexpand=4
        self._nelec=np.sum(mol.nelec)
        self._mol=mol
        self.parameters['cusp']=np.array([1.,1.])
        self.parameters['exponents']=np.array([0.2*2**n for n in range(1,nexpand)])
        self.parameters['coeff']=np.zeros(nexpand)
        self._bvalues=np.zeros((nconfig,nexpand))
        self._eposcurrent=np.zeros((nconfig,self._nelec,3))

    def recompute(self,epos):
        """ """
        u=0.0
        self._eposcurrent=epos.copy()
        #Evaluate b's and c's 
        #We will save the b sums over i,j in _bvalues



        return (1,u)

    def updateinternals(self,e,epos,mask=None):
        """  """
        #update b and c sums. This overlaps with testvalue()
        if mask is None:
            mask=[True]*self._eposcurrent.shape[0]
        self._eposcurrent[mask,e,:]=epos[mask,e,:]

    def value(self): 
        """  """

    def gradient(self,e,epos):
        """We compute the gradient for electron e as 
        :math:`\grad_e \ln \Psi_J = \sum_k c_k \sum_{j > e} \grad_e b_k(r_{ej})  + \sum_{i < e} \grad_e b_k(r_{ie}) `
        So we need to compute the gradient of the b's for these indices. 
        Note that we need to compute distances between electron position given and the current electron distances.
        We will need this for laplacian() as well"""

    def laplacian(self,e,epos):
        """ """
        

    def testvalue(self,e,epos):
        """
        here we will evaluate the b's for a given electron (both the old and new) 
        and work out the updated value. This allows us to save a lot of memory
        """

    def pgradient(self):
        """Given the b sums, this is pretty trivial for the coefficient derivatives.
        For the exponent derivatives, we will have to compute the derivative of all the b's 
        and redo the sums, similar to recompute() """



def test(): 
    from pyscf import lib, gto, scf
    
    mol = gto.M(atom='Li 0. 0. 0.; H 0. 0. 1.5', basis='cc-pvtz',unit='bohr')
    epos=np.random.randn(10,4,3)
    
    jastrow=Jastrow2B(10,mol)
    baseval=jastrow.recompute(epos)
    e=3
    grad=jastrow.gradient(e,epos[:,e,:])
    print(grad)

    delta=1e-9
    for d in range(0,3):
        eposnew=epos.copy()
        eposnew[:,e,d]+=delta
        baseval=jastrow.recompute(epos)
        testval=jastrow.testvalue(e,eposnew[:,e,:])
        valnew=jastrow.recompute(eposnew)
        print("updated value",testval-np.exp(valnew[1]-baseval[1]))
        print('derivative',d,'analytic',grad[d,:],'numerical',(valnew[1]-baseval[1])/delta)
    
if __name__=="__main__":
    test()
