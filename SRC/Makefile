TREE_TYPE = TWO_LEVEL_TREE
# TREE_TYPE = THREE_LEVEL_TREE
# TREE_TYPE = ONE_LEVEL_TREE

# CC = gcc
IDIR = INCLUDE
ODIR = OBJ
CFLAGS = -O3 -Wall -I$(IDIR) -D$(TREE_TYPE) -g

_DEPS = GainType.h LKH.h

DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = SolveCTSP.o SolveTSP.o                                          \
       Distance.o Distance_SPECIAL.o eprintf.o fscanint.o GetTime.o    \
	   IsCandidate.o printff.o PrintParameters.o Random.o ReadLine.o   \
       ReadParameters.o ReadPenalties.o ReadProblem.o  Statistics.o    \
       WriteTour.o

_OBJ_CLKH = CLKHmain.o $(_OBJ)
_OBJ_CLKH_EXP = CLKH_EXPmain.o $(_OBJ)
_OBJ_CLKH_CHECK = CLKH_CHECKmain.o $(_OBJ)
             
OBJ_CLKH = $(patsubst %,$(ODIR)/%,$(_OBJ_CLKH))
OBJ_CLKH_EXP = $(patsubst %,$(ODIR)/%,$(_OBJ_CLKH_EXP))
OBJ_CLKH_CHECK= $(patsubst %,$(ODIR)/%,$(_OBJ_CLKH_CHECK))

$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

.PHONY: 
	all clean

all:
	$(MAKE) CLKH
	$(MAKE) CLKH_EXP
	$(MAKE) CLKH_CHECK

CLKH: $(OBJ_CLKH) $(DEPS)
	$(CC) -o ../CLKH $(OBJ_CLKH) $(CFLAGS) -lm
CLKH_EXP: $(OBJ_CLKH_EXP) $(DEPS)
	$(CC) -o ../CLKH_EXP $(OBJ_CLKH_EXP) $(CFLAGS) -lm
CLKH_CHECK: $(OBJ_CLKH_CHECK) $(DEPS)
	$(CC) -o ../CLKH_CHECK $(OBJ_CLKH_CHECK) $(CFLAGS) -lm
 
clean:
	/bin/rm -f $(ODIR)/*.o ../CLKH ../CLKH_EXP ../CLKH_CHECK *~ ._*\
   	           $(IDIR)/*~ $(IDIR)/._* 
