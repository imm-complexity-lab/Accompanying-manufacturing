#include "LKH.h"
#include <unistd.h>
#include <sys/time.h>
#include <sys/resource.h>

GainType SolveTSP(int Dimension, char *ParFileName,
                  char *TourFileName, int *Tour, GainType Optimum,
                  GainType Displacement);

GainType SolveCTSP(int *Tour)
{
    int i, j, Dist, Clusters = 0;
    Cluster *Cl;
    Node *From, *To;
    FILE *ParFile, *ProblemFile;
    char ParFileName[256], ProblemFileName[256],
        NewTourFileName[256], Prefix[256];
    GainType M, Cost;
    int *Used;

    for (Cl = FirstCluster; Cl; Cl = Cl->Next) {
        Clusters++;
        From = Cl->First;
        do
            From->V = Clusters;
        while ((From = From->Next) != Cl->First);
    }

    M = Clusters < 2 ? 0 : INT_MAX / 2 / Precision;

    sprintf(Prefix, "%s.pid%d", Name, getpid());

    /* Create the problem file */
    sprintf(ProblemFileName, "TMP/%s.ctsp", Prefix);
    assert(ProblemFile = fopen(ProblemFileName, "w"));
    fprintf(ProblemFile, "NAME : %s.ctsp\n", Prefix);
    if (Type)
        fprintf(ProblemFile, "TYPE : %s\n", Type);
    if (ProblemType != ATSP)
        fprintf(ProblemFile, "DIMENSION : %d\n", Dimension);
    else
        fprintf(ProblemFile, "DIMENSION : %d\n", DimensionSaved);
    fprintf(ProblemFile, "EDGE_WEIGHT_TYPE : EXPLICIT\n");
    if (ProblemType != ATSP)
        fprintf(ProblemFile, "EDGE_WEIGHT_FORMAT : UPPER_ROW\n");
    else
        fprintf(ProblemFile, "EDGE_WEIGHT_FORMAT : FULL_MATRIX\n");
    fprintf(ProblemFile, "EDGE_WEIGHT_SECTION\n");
    for (i = 1; i <= DimensionSaved; i++) {
        From = &NodeSet[i];
        for (j = ProblemType != ATSP ? i + 1 : 1; j <= DimensionSaved; j++) {
            if (i == j)
                fprintf(ProblemFile, "9999999 ");
            else {
                To = &NodeSet[j];
                Dist = (ProblemType != ATSP ?
                        Distance(From, To) : From->C[j]) +
                    (From->V != To->V ? M : 0);
                fprintf(ProblemFile, "%d ", Dist);
                while (Dist * Precision / Precision != Dist) {
                    printff("*** PRECISION (= %d) is too large. ",
                            Precision);
                    if ((Precision /= 10) < 1)
                        Precision = 1;
                    printff("Changed to %d.\n", Precision);
                }
            }
        }
    }
    fprintf(ProblemFile, "EOF\n");
    fclose(ProblemFile);

    /* Create the parameter file */
    sprintf(ParFileName, "TMP/%s.par", Prefix);
    assert(ParFile = fopen(ParFileName, "w"));
    fprintf(ParFile, "PROBLEM_FILE = TMP/%s.ctsp\n", Prefix);
    fprintf(ParFile, "ASCENT_CANDIDATES = %d\n", AscentCandidates);
    fprintf(ParFile, "BACKBONE_TRIALS = %d\n", BackboneTrials);
    if (Backtracking)
        fprintf(ParFile, "BACKTRACKING  = YES\n");
    for (i = 0; i < CandidateFiles; i++)
        fprintf(ParFile, "CANDIDATE_FILE = %s\n", CandidateFileName[i]);
    fprintf(ParFile, "CANDIDATE_SET_TYPE = ALPHA\n");
    if (Excess > 0)
        fprintf(ParFile, "EXCESS = %g\n", Excess);
    if (!Gain23Used)
        fprintf(ParFile, "GAIN23 = NO\n");
    if (!GainCriterionUsed)
        fprintf(ParFile, "GAIN_CRITERION = NO\n");
    fprintf(ParFile, "INITIAL_PERIOD = %d\n", InitialPeriod);
    if (InitialTourAlgorithm != WALK)
        fprintf(ParFile, "INITIAL_TOUR_ALGORITHM = %s\n",
                InitialTourAlgorithm ==
                NEAREST_NEIGHBOR ? "NEAREST-NEIGHBOR" :
                InitialTourAlgorithm == GREEDY ? "GREEDY" : "");
    fprintf(ParFile, "INITIAL_STEP_SIZE = %d\n", InitialStepSize);
    if (InitialTourFileName)
        fprintf(ParFile, "INITIAL_TOUR_FILE = %s\n", InitialTourFileName);
    fprintf(ParFile, "INITIAL_TOUR_FRACTION = %0.3f\n",
            InitialTourFraction);
    if (InputTourFileName)
        fprintf(ParFile, "INPUT_TOUR_FILE = %s\n", InputTourFileName);
    fprintf(ParFile, "KICK_TYPE = %d\n", KickType);
    fprintf(ParFile, "MAX_BREADTH = %d\n", MaxBreadth);
    fprintf(ParFile, "MAX_CANDIDATES = %d%s\n", MaxCandidates,
            CandidateSetSymmetric ? " SYMMETRIC" : "");
    fprintf(ParFile, "MAX_SWAPS = %d\n", MaxSwaps);
    fprintf(ParFile, "MAX_TRIALS = %d\n", MaxTrials);
    for (i = 0; i < MergeTourFiles; i++)
        fprintf(ParFile, "MERGE_TOUR_FILE = %s\n", MergeTourFileName[i]);
    fprintf(ParFile, "MOVE_TYPE = %d\n", MoveType);
    if (NonsequentialMoveType >= 4)
        fprintf(ParFile, "NONSEQUENTIAL_MOVE_TYPE = %d\n",
                NonsequentialMoveType);
    if (Optimum != MINUS_INFINITY)
        fprintf(ParFile, "OPTIMUM = " GainFormat "\n",
                Optimum + Clusters * M);
    fprintf(ParFile, "PATCHING_A = %d %s\n", PatchingA,
            PatchingARestricted ? "RESTRICTED" :
            PatchingAExtended ? "EXTENDED" : "");
    fprintf(ParFile, "PATCHING_C = %d %s\n", PatchingC,
            PatchingCRestricted ? "RESTRICTED" :
            PatchingCExtended ? "EXTENDED" : "");
    if (PiFileName)
        fprintf(ParFile, "PI_FILE = %s\n", PiFileName);
    fprintf(ParFile, "POPULATION_SIZE = %d\n", MaxPopulationSize);
    fprintf(ParFile, "PRECISION = %d\n", Precision);
    if (!RestrictedSearch)
        fprintf(ParFile, "RESTRICTED_SEARCH = NO\n");
    fprintf(ParFile, "RUNS = %d\n", Runs);
    fprintf(ParFile, "SEED = %d\n", Seed);
    if (!StopAtOptimum)
        fprintf(ParFile, "STOP_AT_OPTIMUM = NO\n");
    if (!Subgradient)
        fprintf(ParFile, "SUBGRADIENT = NO\n");
    if (SubproblemSize > 0)
        fprintf(ParFile, "SUBPROBLEM_SIZE = %d\n", SubproblemSize);
    if (SubproblemTourFileName)
        fprintf(ParFile, "SUBPROBLEM_TOUR_FILE = %s\n",
                SubproblemTourFileName);
    fprintf(ParFile, "SUBSEQUENT_MOVE_TYPE = %d\n", SubsequentMoveType);
    if (!SubsequentPatching)
        fprintf(ParFile, "SUBSEQUENT_PATCHING = NO\n");
    if (TimeLimit != DBL_MAX)
        fprintf(ParFile, "TIME_LIMIT = %0.1f\n", TimeLimit);
    sprintf(NewTourFileName, "TMP/%s.temp.tour", Prefix);
    fprintf(ParFile, "TOUR_FILE = %s\n", NewTourFileName);
    fprintf(ParFile, "TRACE_LEVEL = %d\n",
            TraceLevel == 0 ? 1 : TraceLevel);
    fclose(ParFile);

    /* Transform the CTSP into a TSP/ATSP */
    /* Solve the TSP/ATSP */
    Cost =
        SolveTSP(DimensionSaved, ParFileName, NewTourFileName,
                 Tour, Optimum, M * Clusters);
    unlink(ParFileName);
    unlink(ProblemFileName);

    /* Check the tour */
    for (i = 1; i <= DimensionSaved; i++)
        NodeSet[Tour[i - 1]].Suc = &NodeSet[Tour[i]];
    From = FirstNode;
    i = From->V;
    do
        FirstNode = From = From->Suc;
    while (From->V == i);
    assert(Used = (int *) calloc(Clusters + 1, sizeof(int)));
    do {
        j = From->V;
        if (Used[j])
            eprintf("Illegal tour: cluster entered more than once");
        Used[j] = 1;
        while (From->V == j)
            From = From->Suc;
    } while (From != FirstNode);
    for (i = 1; i <= Clusters; i++)
        if (!Used[i])
            eprintf("Illegal tour: unvisited cluster(s)");
    free(Used);
    return Cost;
}
