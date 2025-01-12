# Discrete Algebraic Reconstruction Technique (DART)
DART is an iterative reconstruction algorithm for discrete tomography. The original publication in <a href="#original_publication">[1]</a> was used as reference to create this library.
What this repository consists of, is an implementation of the DART algorithm together with a framework to generate phantoms and measurements, to test the algorithm itself.<br/>
The DART algorithm alternates between continuous and discrete reconstruction steps. For the continuous step, many reconstruction algorithms were implemented with **astra-toolbox**. Publications relevant to this library can be found in <a href="#astra_1">[2]</a>, <a href="#astra_2">[3]</a> and <a href="#astra_3">[4]</a>. For the original publication of SART, which is the main reconstruction algorithm presented in the original DART publication, you can refer to <a href="#SART">[5]</a>.

This project was created as a practical assignment of the *Computational Imaging and Tomography* course at Leiden University 2021/22. The submitted report of our experiments can be found <a href="https://github.com/OhGreat/DART_python/blob/main/DART_experimentation_report.pdf">here</a>.<br/>


<!-- TABLE OF CONTENTS -->
<details id="test">
  <summary>Table of Contents</summary>
  <ul>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#usage">Usage</a></li>
    <ul>
        <li><a href="#generating-phantoms">Generationg phantoms</a></li>
        <li><a href="#generating-projections">Generating projections</a></li>
        <li><a href="#dart-and-substeps">DART & substeps</a></li>
        <li><a href="#algebraic-reconstruction-algorithms">Algebraic Reconstruction Algorithms</a></li>
    </ul>
    <li><a href="#examples-and-results">Examples & Results</a></li>
    <li><a href="#issues">Issues</a></li>
    <li><a href="#references">References</a></li>
  </ul>
</details>


## Prerequisites
An environment with `Python 3` >= 3.6 is required to use this library with the `astra-toolbox` installed.
Astra-toolbox can be installed with anaconda with the following command:
```python
conda install -c astra-toolbox astra-toolbox
```
Or you can follow the instructions available <a href="https://www.astra-toolbox.com/">here</a>.

To install the DART pip package run the following command:
```python
pip install DART-OhGreat
```

## Usage
To run DART, data *(in the form of phantoms)* and measurements *(in the form of projections)* need to be artificially constructed. 
Therefore, three main wrappers have been created around the code to solve the following tasks:
- phantom creation
- projection and measurements acquisition
- running DART reconstruction algorithm

Usage of the package for each of this tasks is described in detail in the following sections. 

If instead of using the pip package you chose to clone the repository, you need to add `src.` before every import as such:
```python
from src.phantoms.creator import create_phantoms
```

### Generating phantoms

#### Semilunar phantoms
To generate semilunar like phantoms you can use the `create_phantoms` function. It can be imported from `phantoms.creator.py` and used as below:
```python
from phantoms.creator import create_phantoms
phantom_list = create_phantoms(phantoms="semilunars",img_size=512, gray_values=[255, 200, 150], n=3, overlap=False, seed=None, img_name="dir/to/save/filename")
``` 
Parameters:
- `phantoms`: (string), name of the phantom family. Shoud be one between "semilunars", "aliens", "clouds", "paws".
- `img_size`: should be an integer of value 256 or 512 and represents the size of the phantoms to generate.
- `gray_values`: list of three integers between 0 and 255 representing the intensities to use for the various phantom layers.
- `n`: integer representing the number of phantoms to generate.
- `overlap`: defines wether the shape layers should overlap between them.
- `seed`: integer to be passed to have reproducible results.
- `img_name`: string defining the path and filename to use.
                The filename should not have the extension, 
                it will be created as a png by default.

Output:
- python list of phantoms.

### Generating projections

#### From 2D phantoms
To generate measurements in the form of 1D projections, the function `project_from_2D` has been created. You can import it and use it with the following commands:

```python
from projections.project import project_from_2D
proj_id, sino_id, sinogram = project_from_2D(phantom_id, vol_geom, n_projections, detector_spacing, apply_noise=False, save_dir=None, use_gpu=False)
```
Parameters:
- `phantom_id`: Phantom as astra-toolbox object.
- `vol_geom`: geometry of the output image. Used to define the number of detectors as the first dimension of the vol_geom.
- `n_projections`: is an integer value representing the number of projections as the number of angles to make measurements from.
- `detector_spacing`: defines the size of the pixel.
- `angles`: angles to use for the measurements. (np.array, should be created as a np.linspace of values)
- `noise_factor`: factor that adds Poisson distributed noise to the image, when defined. 
- `save_dir`: string representing the directory to save png images that represent the measurements. Images won't be saved if this parameter is not set.
- `use_gpu`: creates a projector that can use GPU  

Output:
- The function will return `proj_id`, `sino_id` and `sinogram`. The first is a reference to the astra toolbox projector object, the second is a reference to the astra toolkit sinogram object and the former is the sinograms' actual measurements.

#### From 3D phantoms
***to be added***


### DART and substeps
All the steps required to run the DART algorithm have been broken down and can be used separately. A detailed desctiption for the usage of all the functions  available in the library will follow in this section.
 
#### DART algorithm
DART can be used in the following way:
```python
from algorithms.DART import *
# create DART instance
dart = DART(gray_levels=[0, 40, 150], p=0.85, rec_shape=img.shape,
            proj_geom=proj_geom, projector_id=projector_id,
            sinogram=sinogram)
# run DART algorithm
rec = dart.run(iters=10, rec_alg="SART_CUDA", rec_iter= 1000)

```
Instance parameters:
- `gray_levels`: gray levels known *a priori* used in the segmentation step. (list)
- `p`: probability of a pixel to not be sampled as a free pixel. (float)
- `rec_shape`: shape of the volume to create as output. (tuple)
- `proj_geom`: astra-toolbox projection geometry used for the measurements.
- `projector_id`: reference to the astra toolbox projector used to make the projections. (Can be created with the **project_from_2D** fucntion described above)
- `sinogram`: sinorgam of measurements. (np.array) (Can be created with the **project_from_2D** fucntion described above)

Run parameters:
- `iters`: number of DART iteration to perform. (int)
- `p`: as above, can be used to run multiple experiments without reistanciating DART.
- `gray_levels`:same as above.
- `rec_alg`: algebraic reconstruction algorithm to use: can be 'SART', 'SIRT' or 'FBP'. To run the GPU implementations just add '_CUDA' to the algorithn name (e.g. 'SART_CUDA').
- `rec_iter`: number of reconstruction subrutine iterations to run.

Output:
- (np.array), returns the reconstructed image.

### Segmentation
The method `segment` can be used to segment an image at the defined gray values, once DART has been instanced as defined above.
```python
new_gray_vals = [0, 130, 240]
dart.gray_values = new_gray_vals
# function to update gray values thresholds
dart.update_gray_thresholds()
segmented_img = dart.segment(img)
```
Parameters:
- `img`: is the grayscale input phantom to segment as a 2D numpy matrix.
- `gray_levels` : array of gray levels to compute the thresholds for the segmentation from.

Output:
- returns the segmented image. (np.array)

### Pixel neighborhood
To calculate the indexes of neighbours of a specific pixel, you can use the method `pixel_neighborhood` as below:
```python
neighbours = dart.pixel_neighborhood(img_shape, x, y)
```
Parameters:
- `img_shape` : is the shape of the reconstructed image.
- `x,y`: are the coordinates of the pixel to calculate the neighbours for.

Output:
- The method returns a list with all the indexes of the neighbours.

### Boundary pixels
To calculate the boundary pixels of the phantom image, the method `boundary_pixels` takes as input the reconstructed image and calculates the boundary pixels with the help of the `pixel_neighborhood` method described above. You can use it as follows, after having created a DART instance:
```python
b_pixels = dart.boundary_pixels(img):
```
Parameters:
- `img`: (2D np.array), image to calculate boundary pixels for.

Output:
- (np.array), mask of boundary pixels.

### Free pixels
To calculate the free pixels, the following method is available:
```python
free_pixels = dart.free_pixels()
```
The method takes into consideration the **p** value defined in the DART instance to calculate the free pixels.

Output:
- The output `free_pixels` is a binary 2D np.array, where the True values represent the free pixels.

## Algebraic Reconstruction Algorithms
For the continous reconstruction step of DART, various algorithms have been implemented with the ASTRA-toolbox. Specifically, **SART**, **SIRT** and **FBP** are available for experimentation. You can call the functions detatched from DART as below:

The following example demostrates how to use SART:
```python
from algorithms.SART import *
sart_res_id, sart_res = SART(vol_geom, vol_data, projector_id, sino_id, iters, use_gpu=True)
```
SIRT and FBP can be used similarly to the SART example above. 

Parameters:
- `vol_geom`: represents the volume geometry for the output.
- `vol_data`: starting values to use for the reconstructed image.
- `projector_id`: specifies the projector to use for the measurements.
- `sino_id`: is the sinogram id of the projections.
- `iters`: number of dart iterations to run.
- `use_gpu`: set to True to run Astra on GPU. You also need to use a gpu capable projector.

Output:
- The algorithm will return `sart_res_id` which is the astra-toolbox reference to the reconstructed phantom, and `sart_res`, a numpy array with the actual values of the reconstructed phantom.  

## Examples and Results
Examples on how to use the repository are available in the notebook examples under the `notebook_examples` directory. To run experiments on various algorithms and measurement configurations you can check the examples in the `experiment_scripts` directory.

The following reconstruction is a sample of the experiments carried out to in the report attached in the repository. The experiment consisted in comparing the performance of DART, SART and SIRT algorithms for 12 projections and an angular range of 120 degrees. For a fair comparison, all algorithms were run for the same number of reconstruction steps. Specifically, DART was run for 50 iterations and 1000 SART subrutines for each iteration, while SART and SIRT were run for 50.000 iterations. As we can see from the images, DART achieves a better reconstruction than the compared algorithms both in their raw output and the segmented one.

<img src="https://github.com/OhGreat/DART_python/blob/main/report_images/alien_rec_low_proj.png" />

The following experiment was made under the assumption of limited number of projections. In total 8 projections were used with an angle range of 180 degrees. The same number of iterations as above was used for this experiment. The results again show that DART achieves superior reconstructions.

<img src="https://github.com/OhGreat/DART_python/blob/main/report_images/paw_low_proj.png" />

## Issues
If you encounter any problems while using the framework you can notify us by opening an issue here: https://github.com/OhGreat/DART_python/issues

## References
<div id="original_publication">
[1].<br/>
Batenburg, Kees & Sijbers, Jan. (2011). DART: A Practical Reconstruction Algorithm for Discrete Tomography. IEEE transactions on image processing : a publication of the IEEE Signal Processing Society. 20. 2542-53. 10.1109/TIP.2011.2131661, <a href="https://ieeexplore.ieee.org/document/5738333">https://ieeexplore.ieee.org/document/5738333</a>
</div>

<br/>
<div id="astra_1">
[2].<br/>
W. van Aarle, W. J. Palenstijn, J. Cant, E. Janssens, F. Bleichrodt, A. Dabravolski, J. De Beenhouwer, K. J. Batenburg, and J. Sijbers, “Fast and Flexible X-ray Tomography Using the ASTRA Toolbox”, Optics Express, 24(22), 25129-25147, (2016),
 <a href="http://dx.doi.org/10.1364/OE.24.025129">http://dx.doi.org/10.1364/OE.24.025129</a>
</div>

<br/>
<div id="astra_2">
[3].<br/>
W. van Aarle, W. J. Palenstijn, J. De Beenhouwer, T. Altantzis, S. Bals, K. J. Batenburg, and J. Sijbers, “The ASTRA Toolbox: A platform for advanced algorithm development in electron tomography”, Ultramicroscopy, 157, 35–47, (2015), <a href="http://dx.doi.org/10.1016/j.ultramic.2015.05.002">http://dx.doi.org/10.1016/j.ultramic.2015.05.002</a>
</div>

<br/>
<div id="astra_3">
[4].<br/>
W. J. Palenstijn, K. J. Batenburg, and J. Sijbers, “Performance improvements for iterative electron tomography reconstruction using graphics processing units (GPUs)”, Journal of Structural Biology, vol. 176, issue 2, pp. 250-253, 2011, <a href="http://dx.doi.org/10.1016/j.jsb.2011.07.017">http://dx.doi.org/10.1016/j.jsb.2011.07.017</a>
</div>

<br/>
<div id="SART">
[5].<br/>
Yu, Hengyong & Wang, Ge. (2010). SART-Type Image Reconstruction from a Limited Number of Projections with the Sparsity Constraint. International journal of biomedical imaging. 2010. 934847. 10.1155/2010/934847. <a href="https://www.hindawi.com/journals/ijbi/2010/934847/">https://www.hindawi.com/journals/ijbi/2010/934847/</a>
 </div>
