# Mohr’s Circle Plotter (Python)

This repository contains a Python script that reads **3×3 stress tensors** (MPa) from multiple material-point `.dat` files, computes the **principal stresses** (eigenvalues), and generates **Mohr’s Circle** plots for:

- Each individual material point
- Average stress tensor (unweighted)
- Volume-weighted average stress tensor

All plots are saved as PNG files.

## Repository Structure

```text
├── README.md
├── requirements.txt
├── src/
│   └── MohrCircle.py
├── input/
│   ├── Gr10_MatPt1.dat
│   ├── Gr10_MatPt2.dat
│   ├── ...
│   └── Gr10_MatPt10.dat
└── results/
    ├── MohrCirc_Gr10_MatPt1.PNG
    ├── ...
    ├── MohrCirc_Gr10_MatPt10.PNG
    ├── MohrCirc_Gr10_Avg.PNG
    └── MohrCirc_Gr10_VolAvg.PNG

```
### Installation
```bash
pip install -r requirements.txt
```

### Run
```bash
python src/MohrCircle.py Gr10 MatPt dat 10
```

### Arguments
1. **FilePrefixStr**: Prefix of the input file names (e.g., `Gr10`).
2. **MatPtStr**: Material point identifier string (e.g., `MatPt`).
3. **FileExtension**: File extension of the input files (e.g., `dat`).
4. **NumMaterialPoints**: Number of material points (an integer, e.g., `10`).

## Input File Format
```text
# AtomicVolume: 16.890729999999998
-1.1061717529e+03 -9.9840942380e+02  2.4667868040e+02
-9.9840942380e+02  1.7068065186e+03  5.1543750000e+02
 2.4667868040e+02  5.1543750000e+02 -1.4615225220e+02
```
## Output
The script generates PNG files:
- Individual material points: `MohrCirc_<FilePrefixStr>_<MatPtStr><n>.PNG` (e.g., `MohrCirc_Gr10_MatPt1.PNG`).
- Simple average: `MohrCirc_<FilePrefixStr>_Avg.PNG` (e.g., `MohrCirc_Gr10_Avg.PNG`).
- Volume-weighted average: `MohrCirc_<FilePrefixStr>_VolAvg.PNG` (e.g., `MohrCirc_Gr10_VolAvg.PNG`).
