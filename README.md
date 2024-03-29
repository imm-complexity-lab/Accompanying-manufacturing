# Paper Abstract
The paper is devoted to the problem of optimization of accompanying manufacturing in flexible or reconfigurable manufacturing systems. Using a set of obligatory products as an input, the initial problem is reduced to two interrelated subproblems: 1) for each product from the set of obligatory products, form a group of additional (accompanying) products that can be manufactured without changing the state of production, and 2) determine the order of manufacturing changeovers between the groups of additional products, as well as the ``points of entry and exit'' for each group. The subproblems are considered sequentially: the first subproblem is reduced to the maximum weight clique problem, the second -- to the cluster traveling salesman problem. Large-scale computational experiments were conducted to reveal the benefits of applying effective modern methods for solving both subproblems in comparison with the greedy solution (which models the rational actions of a human operator solving large accompanying manufacturing problems in short time).


# Auxiliary software



GLKH is a program for solving the Clustered Traveling Salesman Problem (CTSP).

The code is distributed for research use. The author reserves all rights to the
code.

INSTRUCTIONS FOR INSTALLATION: (Version 1.0 - December 2013)

The software is available in gzipped tar format:

    CLKH-1.0.tgz        (approximately 10 MB)

Download the software and execute the following UNIX commands:

    tar xvfz CLKH-1.0.tgz
    cd CLKH-1.0 
    make

Four executable files called CLKH, CLKH_EXP, CLKH_CHECK, and LKH will now be
available in the directory CLKH-1.0.

CLKH is used for solving a given instance once, whereas GLKH_EXP is used
for solving an instance using a specified number of independent runs, 
default is 10. CLKH_CHECK may be used to check that a solution is feasible 
(i.e., it visits each cluster exactly once and has a correct length). 
LKH is an executable of LKH-2.0.7. 

To ease the running of CLKH and CLKH_EXP, two scripts, runCLKH and runCLKH_EXP,
are provided. They create suitable parameter files and execute CLKH and 
CLKH_EXP, respectively.

The scripts runSmall, runLarge and runVeryLarge can be used for solving the
GTSPLIB instances. It is recommended to run the script runSmall in order to
test the installation:

    ./runSmall

The runCLKH script may be used for solving other instances. Just change 
the value of PROBLEM_FILE in the script. 

The CLKH-1.0 directory contains the following subdirectories:

  GTSPLIB:   library of benchmark instances. A description of the format can
             be found at http://www.cs.rhul.ac.uk/home/zvero/GTSPLIB/.

  C-TOURS:   optimal or current best tours for the GTSPLIB instances. 

  PI-FILES:  pi-files generated by the Held-Karp ascent.

  SRC:       source code of CLKH

  LKH-2.0.7: source code for the current version of LKH.

  TMP:       temporary files used during the solution process.
