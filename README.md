# Mohr’s Circle Plotter (Python)

This repository contains a Python script that reads **3×3 stress tensors** (MPa) from multiple material-point `.dat` files, computes the **principal stresses** (eigenvalues), and generates **Mohr’s Circle** plots for:

- Each individual material point
- Average stress tensor (unweighted)
- Volume-weighted average stress tensor

All plots are saved as PNG files.

## Repository Structure

```text

## Repository Structure

```text
.
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


Input File Format

Each `.dat` file must follow this format:

Line 1: Volume (comment line)
Example:
# AtomicVolume: 16.890729999999998

Lines 2–4: Stress tensor (3×3) in MPa

Example:
-1.1061717529e+03 -9.9840942380e+02  2.4667868040e+02
-9.9840942380e+02  1.7068065186e+03  5.1543750000e+02
 2.4667868040e+02  5.1543750000e+02 -1.4615225220e+02

##Installation

Install required Python libraries:

pip install -r requirements.txt

How to Run

Run the script from the repository root:
python src/MohrCircle.py Gr10 MatPt dat 10

Arguments

FilePrefixStr → Prefix of the input files (example: Gr10)

MatPtStr → Material point naming string (example: MatPt)

FileExtension → Input file extension (example: dat)

NumMaterialPoints → Number of material point files (example: 10)

The script will read:

input/Gr10_MatPt1.dat

input/Gr10_MatPt2.dat

...

input/Gr10_MatPt10.dat

and save outputs to results/.

Output Files
1) Individual material point plots

Saved as:

results/MohrCirc_Gr10_MatPt1.PNG

...

results/MohrCirc_Gr10_MatPt10.PNG

2) Average stress tensor plot (unweighted)

Saved as:

results/MohrCirc_Gr10_Avg.PNG

3) Volume-weighted average stress tensor plot

Saved as:

results/MohrCirc_Gr10_VolAvg.PNG



