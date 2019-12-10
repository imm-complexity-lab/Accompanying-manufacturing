#include "LKH.h"
#include <unistd.h>
#include <sys/time.h>
#include <sys/resource.h>

GainType SolveCTSP(int *Tour);
static double GetTimeUsage(int who);

/*
 * This file contains the main function of the CLKH program.
 */

int main(int argc, char *argv[])
{
    GainType Cost;
    int *Tour;

    /* Read the specification of the problem */
    if (argc >= 2)
        ParameterFileName = argv[1];
    ReadParameters();
    ReadProblem();
    assert(Tour = (int *) malloc((DimensionSaved + 1) * sizeof(int)));
    Cost = SolveCTSP(Tour);
    TraceLevel = 1;
    if (OutputTourFileName)
        WriteTour(OutputTourFileName, Tour, Cost);
    if (TourFileName && (Optimum == MINUS_INFINITY || Cost < Optimum))
        WriteTour(TourFileName, Tour, Cost);
    printff("Value = " GainFormat, Cost);
    if (Optimum != MINUS_INFINITY && Optimum != 0)
        printff(", Error = %0.2f%%", 100.0 * (Cost - Optimum) / Optimum);
    printff(", Time = %0.1f sec.\n\n",
            GetTimeUsage(RUSAGE_SELF) + GetTimeUsage(RUSAGE_CHILDREN));
    return 0;
}

static double GetTimeUsage(int who)
{
    struct rusage ru;
    getrusage(who, &ru);
    return ru.ru_utime.tv_sec + ru.ru_utime.tv_usec / 1000000.0;
}
 
