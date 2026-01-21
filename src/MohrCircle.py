import sys
import re
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

_FLOAT_RE = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


def readData(fname: str):
    path = Path(fname)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {fname}")

    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    lines = [ln.strip() for ln in lines if ln.strip()]

    if len(lines) < 4:
        raise ValueError(f"{fname} has too few lines. Expected 1 volume line + 3 tensor lines.")

    # Parse volume (first float on first line)
    m = _FLOAT_RE.findall(lines[0])
    if not m:
        raise ValueError(f"Could not parse volume from first line in {fname}: {lines[0]!r}")
    V = float(m[0])

    # Parse 3x3 stress tensor
    tensor = []
    for i in range(1, 4):
        parts = lines[i].split()
        if len(parts) != 3:
            raise ValueError(f"{fname} line {i+1} must have 3 numbers: {lines[i]!r}")
        tensor.append([float(x) for x in parts])

    Sigma = np.array(tensor, dtype=float)
    if Sigma.shape != (3, 3):
        raise ValueError(f"{fname}: stress tensor is not 3x3. Got {Sigma.shape}")

    return Sigma, V


def AvgStress(SigArr, VolumeArr):
    """
    Volume-weighted average stress tensor:
      sum(Sigma_i * V_i) / sum(V_i)

    For unweighted average, pass VolumeArr = [1,1,...,1]
    """
    SigArr = np.asarray(SigArr, dtype=float)          # (N,3,3)
    VolumeArr = np.asarray(VolumeArr, dtype=float)    # (N,)

    denom = np.sum(VolumeArr)
    if denom == 0:
        raise ValueError("Sum of volumes is 0; cannot compute weighted average.")

    return np.sum(SigArr * VolumeArr[:, None, None], axis=0) / denom


def EigVal(Sigma):
    """
    Principal stresses = eigenvalues of symmetric stress tensor.
    Returns eigenvalues sorted: sigma1 >= sigma2 >= sigma3 (MPa)
    """
    vals = np.linalg.eigvalsh(Sigma)
    return np.sort(vals)[::-1]


def plotMohrsCircle(SigmaEigval, foutNamePNG):
    """
    Plot style:
      - Largest circle (sigma1-sigma3) filled blue
      - Two smaller circles drawn as white holes
      - No arrows
      - Axes lines through origin
    """
    SigmaEigval = np.asarray(SigmaEigval, dtype=float)
    if SigmaEigval.shape != (3,):
        raise ValueError("SigmaEigval must be length-3 (sigma1,sigma2,sigma3).")

    # MPa -> GPa
    s1, s2, s3 = SigmaEigval / 1e3

    # Centers + radii
    c13, r13 = (s1 + s3) / 2.0, (s1 - s3) / 2.0  # Big circle (1-3)
    c12, r12 = (s1 + s2) / 2.0, (s1 - s2) / 2.0  # Small
    c23, r23 = (s2 + s3) / 2.0, (s2 - s3) / 2.0  # Small

    fig, ax = plt.subplots(figsize=(6.4, 6.4))

    # Big filled circle
    big = plt.Circle((c13, 0.0), r13, facecolor="#135198", edgecolor="black", linewidth=1.2)
    ax.add_patch(big)

    # White holes
    hole1 = plt.Circle((c12, 0.0), r12, facecolor="white", edgecolor="black", linewidth=1.2)
    hole2 = plt.Circle((c23, 0.0), r23, facecolor="white", edgecolor="black", linewidth=1.2)
    ax.add_patch(hole1)
    ax.add_patch(hole2)

    # Axis lines through origin
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)

    ax.set_xlabel(r'$\sigma$ [GPa]')
    ax.set_ylabel(r'$\tau$ [GPa]')
    ax.set_aspect("equal", adjustable="box")

    # Limits based on largest circle
    pad = 0.15 * r13 if r13 > 0 else 1.0
    ax.set_xlim(c13 - r13 - pad, c13 + r13 + pad)
    ax.set_ylim(-r13 - pad, r13 + pad)

    out_path = Path(foutNamePNG)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main(FilePrefixStr, MatPtStr, FileExtension, NumMaterialPoints):
    input_dir = Path("input")
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    SigmaArr = []
    VolumeArr = []

    for n in range(1, NumMaterialPoints + 1):
        fname = input_dir / f"{FilePrefixStr}_{MatPtStr}{n}.{FileExtension}"
        Sigma, V = readData(str(fname))
        SigmaArr.append(Sigma)
        VolumeArr.append(V)

    AvgSigma = AvgStress(SigmaArr, [1.0] * NumMaterialPoints)
    VolAvgSigma = AvgStress(SigmaArr, VolumeArr)

    for n in range(1, NumMaterialPoints + 1):
        SigmaEigval = EigVal(SigmaArr[n - 1])
        plotMohrsCircle(
            SigmaEigval,
            str(output_dir / f"MohrCirc_{FilePrefixStr}_{MatPtStr}{n}.PNG"),
        )

    plotMohrsCircle(EigVal(AvgSigma), str(output_dir / f"MohrCirc_{FilePrefixStr}_Avg.PNG"))
    plotMohrsCircle(EigVal(VolAvgSigma), str(output_dir / f"MohrCirc_{FilePrefixStr}_VolAvg.PNG"))

    print(f"Done. Plots saved in: {output_dir.resolve()}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python src/MohrCircle.py <FilePrefixStr> <MatPtStr> <FileExtension> <NumMaterialPoints>")
        print("Example: python src/MohrCircle.py Gr10 MatPt dat 10")
        sys.exit(1)

    FilePrefixStr = sys.argv[1]
    MatPtStr = sys.argv[2]
    FileExtension = sys.argv[3]
    NumMaterialPoints = int(sys.argv[4])

    main(FilePrefixStr, MatPtStr, FileExtension, NumMaterialPoints)
