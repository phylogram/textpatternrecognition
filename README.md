# It is just a riddle

Explanation is found in the jupypter notebook: ./Usage Presentation.ipynb or if you do not want to use jupyter see Usage_Presentation.py

## Installation

Use python 3.6 or venv. Nothing more needed for the core, only the usage examples are in a jupyter notebook, but also available as User_Presentation.py


## TO DO:

- Add any kind of logging / remember functionality. For example store positions of found occurrences in memory for …
- adding a replacement functionality,
- adding alternative search functions instead of regex. RegEx may perform badly in some cases, see: https://flashtext.readthedocs.io/en/latest/  
  - which is not build in the parent class for inheriting. That could cause some troubles later.
    - also sister class expects also regex match. Changing this in brother class would break brother class functionality. Since sister class is in hierarchical relationship to brother class, it would make sense to reflect this in OO.

## Questions

I would like to pass functions from pattern.PatternParser to pattern.PossiblePattern, resulting in an unique responsibility. Lambda does not work, because child classes should be able to overwrite it. 

Just inheriting pattern.PossiblePattern from pattern.PatternParser makes no sense, since it in semantics not a real child class. Everything in __init__ would be done again.
