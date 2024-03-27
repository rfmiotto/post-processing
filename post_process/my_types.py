from nptyping import Float, NDArray, Shape

Array1D = NDArray[Shape["*"], Float]
Array2D = NDArray[Shape["*, *"], Float]
