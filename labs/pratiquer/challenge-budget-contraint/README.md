# Challenge 1: an architecture on a tight budget

This challenge closes the "Practise without an account" module. It tests the
skill **estimating the cost of an architecture** on an environment you did not
build: you have to **read** it, through the official CLI plugged into the
**feint** emulator, then **cost** it on a dated price grid. It is a challenge,
not a guided lab: no command is given.

Lesson of the site that carries this challenge:
<https://www.stephane-robert.info/en/docs/cloud/outils/feint/limites/>.

## What is tested

- Inventory an environment through the CLI, **all zones** included.
- Apply a dated grid **down to its rules**: what is billed, what is not.
- Conclude on the **budget**, and spot what costs without serving.

## Prerequisites

- Module 2 of the course (reading a bill, dated grids) and the lessons of
  module 2b: feint installed, and **`scw` plugged into feint**:
  <https://www.stephane-robert.info/en/docs/cloud/outils/feint/clients/>.
- **dsoxlab** and **Docker**: feint runs in a container, started by
  `dsoxlab run`. Port **4599** must be free.

## Duration

About 45 minutes.

## What the grade measures, and what it does not

The grade compares your `estimation.yaml` with a cost **recomputed** at check
time, from feint's real state and the grid provided. The environment is
**drawn at random** at every `dsoxlab run`: another learner's answer is worth
nothing to you.

feint emulates **no price**: the grid is an exercise grid, dated, whose amounts
are set for this challenge. A real bill is checked against the prices recorded
at the provider, at their date, and against the monthly invoice, which alone is
binding.

```bash
dsoxlab run pratiquer-challenge-budget-contraint
dsoxlab challenge pratiquer-challenge-budget-contraint
```
