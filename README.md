# Introduction to Artificial Intelligence (WSI)
### MENG-PW-S1-WSI – Warsaw University of Technology

Repository for coursework in the **Introduction to Artificial Intelligence** course 
at **Warsaw University of Technology**.

The repository contains implementations of algorithms, experimental studies, and reports prepared as part of laboratory assignments.


## Course Objective

The goal of the course is to implement selected artificial intelligence algorithms and perform experimental evaluation of their behavior.

Each assignment requires:

1. Implementing the specified algorithm from scratch.
2. Performing systematic experiments on the implementation.
3. Analyzing the results and drawing justified conclusions.
4. Preparing clear documentation describing the conducted experiments.

The focus is not only on correct implementation but also on **proper experimental methodology and analysis of results**.



## Assignment Evaluation Criteria

Assignments are evaluated based on the following components:

### Implementation Correctness — 72%
- Correct implementation of the algorithm described during lectures.
- Incorrect implementation that affects experimental results is penalized.
- Implementations that contradict lecture descriptions receive significant penalties.

### Experimental Study — 14%
Evaluation of:
- scope of conducted experiments,
- correctness of methodology,
- relevance of tested parameters and datasets,
- clarity of presented results.

### Conclusions — 14%
Evaluation of:
- correctness of conclusions,
- whether conclusions are supported by experimental results,
- whether conclusions are sufficiently precise and justified.



## General Requirements

Each assignment must include:

- **Source code**
- **Experimental results**
- **Documentation describing the experiments**

The documentation should clearly explain:

- what parameters were tested,
- what datasets were used,
- what results were obtained,
- what conclusions can be drawn from the experiments.



## Experimental Methodology

When conducting experiments:

- Only **one parameter should be changed at a time** when evaluating its influence.
- Results should be presented primarily in **tables**, optionally supported by **plots**.
- Tables should contain aggregated statistics such as:

  - mean value
  - standard deviation
  - minimum result
  - maximum result

Example:

| Parameter | min | mean | std | max |
|-----------|-----|------|-----|-----|
| μ = 20 | 1.23 | 2.34 | 0.11 | 3.45 |
| μ = 40 | 1.03 | 2.49 | 0.91 | 3.51 |

After each table:

1. Describe what can be observed in the results.
2. Explain what parameter values produce the best results.
3. Provide conclusions based on the observed trends.

Final conclusions should summarize the entire experiment.



## Randomized Algorithms

For algorithms that use randomness:

- Results **must not be based on a single run**.
- Experiments should be repeated **at least 25 times**.
- Report aggregated statistics:
  - mean
  - standard deviation
  - best result
  - worst result



## Code Requirements

The implemented algorithm must be:

- **general-purpose**, not tied to a specific dataset
- **readable and maintainable**
- **stable and reusable**

Code should follow these principles:

- clear structure
- descriptive variable and function names
- modular design

Each source file should contain a header specifying the **author**.



## Documentation Requirements

Documentation quality is also evaluated. It should:

- use correct terminology,
- avoid spelling errors,
- clearly describe experimental procedures,
- present results in a readable way.

Numerical results should typically be presented with **two decimal places**.



## Repository Structure
```
.
├── README.md
├── requirements.txt
│
├── src/
│ ├── assignment_01/
│ ├── assignment_02/
│ └── project/
│
├── notebooks/
├── data/
│ ├── raw/
│ └── processed/
│
├── reports/
├── docs/
└── tests/
```

### Directory Description

**src/**  
Implementation of algorithms and assignment code.

**data/**  
Datasets used during experiments.

- `raw/` – original datasets
- `processed/` – transformed or prepared datasets

**notebooks/**  
Optional experimental notebooks.

**reports/**  
Assignment reports and experiment summaries.

**docs/**  
Additional documentation.

**tests/**  
Unit tests for algorithm implementations.



## Development Environment

Recommended environment:

- Python 3.10+
- Git
- Visual Studio Code

Dependencies are listed in:
`requirements.txt`


Install them using:

```bash
pip install -r requirements.txt
```

## Academic Integrity

All submitted work must be **original**.

Submitting code written by another person or copied from the Internet results in a grade of **0** and may lead to further disciplinary consequences.

The course instructors maintain a database of known implementations from previous years and publicly available sources.



## Author

Student of **Warsaw University of Technology**



## How to Run the Code

Clone the repository:

```bash
git clone https://github.com/soswi/MENG-PW-S1-WSI.git
cd MENG-PW-S1-WSI
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
.venv\Scripts\activate
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

Run an assignment example:

```bash
python src/assignment_01/main.py
```
