# algorithmic_trading

This project has been realized in coorperation with the student Hugo BESSON. It consists on the automatic detection of divergences, which occur between an asset and an oscillator. In the world of technical analysis, such project is relevant as the divergence asset indicates, with high probability, the direction in which the asset is likely to evolve. 

The present project allows to perform detection of the 4 types of divergences, which are the regular Bullish and Bearish divergences, and the hidden Bullish and Bearish divergences.

This detection occurs provided that the user provides the following inputs :

- The type of asset on which the detection is performed. 
- The time interval and time resolution associated with the test.
- The type of oscillator to be used (here, the RSI).
- The type of divergence to evaluate (among the four possible)

The result of the algorithm will be a list of two dimensionnals vectors, whose components correspond to the begginings and the ends of the divergences signals. 

The next Figure summarizes the process ;

![](Process.png)
*Inputs and outputs of the algorithm*
