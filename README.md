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
