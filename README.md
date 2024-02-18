# Image-Processing
Created some image processing functions, such as the sobel edge detector, embossing functions, gradient functions, and blurs. Used pillow for loading and convolving images  
## [Image Processing](https://github.com/202248SD/Image-Processing/blob/5f94cd9fb9e157dee51167872eff84cadd327d8f/ImageProcessing03.py)  
Convolve(img, kernel) --> convolves the input img with the kernel  
Grayscale(img) --> Converts input img into grayscale representation with formula: 0.299 x R + 0.587 x G + 0.114 x B  
## [Kernels](https://github.com/202248SD/Image-Processing/blob/5f94cd9fb9e157dee51167872eff84cadd327d8f/kernels.py)  
Has the kernels for image processing. Includes edge and ridge detection kernel, gaussian blur kernel and embossing kernels  
## [Sobel Operator](https://github.com/202248SD/Image-Processing/blob/5f94cd9fb9e157dee51167872eff84cadd327d8f/SobelOperator02.py)  
Created Sobel Operator from scratch  
Converts input img into grayscale  
Convolves grayscale img with kernels Gx and Gy, to approximate horiztonal and vertical gradients  
Resulting approximations are combined to find gradient magnitude  
Resulting approximations are used with tan function to find gradient direction, and edges are colored based on direction of gradient  
