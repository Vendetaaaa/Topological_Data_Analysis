# Topological Data Analysis:
This project builds an engine to compute $H_0$ (connected components) and $H_1$ (loops/holes) persistence intervals for arbitrary metric spaces using Vietoris–Rips filtration.

## Dependencies
```
pip install numpy scipy matplotlib
```

## Quick-Start
```
cd tda-engine - Go to the engine
python main.py - This will run the script to compute topological invariants on a noisy 2D manifold
```
## File Tree
```
tda-engine/
├── requirements.txt
├── main.py
└── tda/
    ├── __init__.py
    ├── union_find.py
    ├── homology.py
    └── utils.py
```

# Enjoy!
