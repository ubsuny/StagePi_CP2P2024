# StagePi_CP2P2024
Studying Second Harmonic Generation (SHG) of Europium Oxide Potassium Tantalate (EuO/KTO) compound as a part of "CP2 Spring 2024" project work.

## Data types involved in code
There are several data types involved in the Python annotations which I will be using in the upcoming project. Some of them are listed below:
- **int:** This data type represents integers or whole numbers such as 1, 2, 3, etc. For example, the variables in the code `px_trig_pin`, `ln_trig_pin`, `fr_trig_pin`, and `volt_threshold` are all integers.
- **float:** This data type represents floating-point numbers, or numbers with a decimal point, such as 1.5, 3.14, 0.01, etc. For example, in the code, the variables such as `self.volt_max`, `self.volt_min`, and `self.volt_offs` are all floats.
- **bool:** This data type represents Boolean values, or logical values, that can be either True or False. For example in the code, the variable `self.vthreshold` is a bool.
- **str:** This data type represents strings, or sequences of characters, such as “Hello”, “Python”, etc. For example in the code, the variables `port` and `cmd` are both strings.
- **list:** This data type represents lists, or ordered collections of values, that can be of any type. For example in the code, the variable `self.channel` is a list of integers.
- **dict:** This data type represents dictionaries or unordered collections of key-value pairs, that can be of any type. For example in the code, the variables `self.volt_max`, `self.volt_min`, and `self.volt_offs` are all dictionaries of floats.
- **NoneType:** This data type represents the absence of a value, and is denoted by the keyword None. For example in the code, the methods `set_pos`, `set_channel`, etc do not return any value.
- **Exception:** This data type represents an error or abnormal condition that occurs during the execution of a program. For example, the `raise Exception`.
- **ValueError:** This data type represents an error that occurs when a function or operation receives an argument that has the right type but an inappropriate value. For example, the `raise ValueError`.

## Random Number generated to simulate SHG results
For any hypothetical sample: 
- random SHG intensities are created using `np.random.rand(len(positions))np.random.rand(len(positions))` based on distance when piezo stage moves along x and z axis.
- random SHG intensities `shg_intensities = electric_fields**2 * d_effs**2` are made based on random photon energies `np.random.uniform(1.5, 3.0, 100)`. The electric fields are also generated randomly `np.random.normal(1.0, 0.1, 100)` and randomly chosen effective non-linear coefficients `d_effs = np.random.normal(1.0, 0.1, 100)`.

For more details, the outputs have been generated in the file `simulated_SHG.ipynb`.

## Physics and Literature Review
Second Harmonic Generation (SHG) is a fascinating nonlinear optical process where two photons of the same frequency interact within a nonlinear material to create a new photon with twice the energy, and therefore, twice the frequency and half the wavelength of the original photons.

$$P  = \chi E = \chi^{(1)} E + \chi^{(2)} E^2 + \chi^{(3)} E^3$$
$\chi^{(2)}$ and $\chi^{(3)}$ are degree of non-linearity known as non-linear susceptibility or polarizability.

An experimental work (by T. Santhanakrishnan et al. 2019) performing SHG on a sample LAO/STO interfaces and its results are shown below:
![Screenshot 2024-03-24 105036](https://github.com/s4il3sh/StagePi_CP2P2024/assets/144289804/400bd371-24af-44f5-98f7-7b1dd1d08043)
More details can be obtained from `SHG.ipynb` file.

## Tensorflow in the code
Tensorflow is used in the code helping to move StagePi. The code and the output of the code is shown in the file `stage_pi.ipynb`. The use of tensorflow would be more effective in machine learning and deep learning by feeding some data to extrapolate. The code I used in moving the StagePi using tensorflow simply replace the similar work of the numpy. Hence I do not see it is being used as its true potential in the code.
