#include "LKH.h"

int main(int argc, char *argv[])
{
    GainType Cost;
    Cluster *Cl;
    Node *From;
    int *Tour, *Used, Clusters = 0, i;
    FILE *TourFile;
    char *TourFileName, *Line, *Keyword, Buf1[256], Buf2[256];
    char Delimiters[] = " :=\n\t\r\f\v\xef\xbb\xbf";

    /* Read the specification of the problem */

    sprintf(Buf1, "GTSPLIB/%s.gtsp", argv[1]);
    ProblemFileName = Buf1;
    sprintf(Buf2, "C-TOURS/%s.%s.tour", argv[1], argv[2]);
    TourFileName = Buf2;
    ReadProblem();
    for (Cl = FirstCluster; Cl; Cl = Cl->Next) {
        Clusters++;
        From = Cl->First;
        do
            From->V = Clusters;
        while ((From = From->Next) != Cl->First);
    }
    assert(TourFile = fopen(TourFileName, "r"));
    while ((Line = ReadLine(TourFile))) {
        if (!(Keyword = strtok(Line, Delimiters)))
            continue;
        for (i = 0; i < strlen(Keyword); i++)
            Keyword[i] = (char) toupper(Keyword[i]);
        if (!strcmp(Keyword, "TOUR_SECTION"))
             break;
        if (Optimum == 0 && !strcmp(Keyword, "COMMENT")) {
            Keyword = strtok(0, Delimiters);
            Keyword = strtok(0, Delimiters);
            Optimum = atoi(Keyword);
        } else {
            if (!strcmp(Keyword, "DIMENSION")) {
                int n;
                Keyword = strtok(0, Delimiters);
                n = atoi(Keyword);
                assert(n == DimensionSaved);
            }
        }
    }
    assert(Tour = (int *) malloc((DimensionSaved + 1) * sizeof(int)));
    for (i = 1; i <= DimensionSaved; i++)
        fscanf(TourFile, "%d", &Tour[i]);
    Tour[0] = Tour[DimensionSaved];
    assert(Used = (int *) calloc(DimensionSaved + 1, sizeof(int)));
    Cost = 0;
    for (i = 1; i <= DimensionSaved; i++) {
        Cost += ProblemType != ATSP ?
            Distance(&NodeSet[Tour[i - 1]], &NodeSet[Tour[i]]) :
            NodeSet[Tour[i - 1]].C[Tour[i]];
        if (Used[Tour[i]])
            eprintf("Cluster entered more than once");
        Used[Tour[i]] = 1;
    }
    for (i = 1; i <= Clusters; i++)
        if (!Used[i])
            eprintf("Unvisited cluster(s)");
    if (Cost != Optimum) 
        eprintf("Cost = %lld != Optimum = %lld\n", Cost, Optimum);
    printff("OK. Cost = %lld\n", Cost);
    return 0;
}
