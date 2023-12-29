# Simulator Readme

## 1. Working/Usage

The simulator executes 4 types of instructions: LS, LM, PUT, and ADD. It reads instructions line by line from the `instruction_file.txt` file. Each instruction follows the format 'corex LM address,' where x is the core number ([1-4]).

Inside the code, the IDs assigned to the cores and cache controllers are actual (core/cache number) - 1. The sharer list for each directory entry is a list of size four where the value at each index indicates whether the ith cache has the cache block in shared/owned state or not (1 implies present, and 0 implies not present as shared).

## 2. Command for Building Random Instruction

To build random instructions, use the following command:

```bash
python .\test\TestInstruction.py <NumberOfInst>
```

## 2. Command for Running the Project

To run the project, use the following command:

```bash
python .\test\main.py
```
