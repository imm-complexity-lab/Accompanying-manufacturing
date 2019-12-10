CC = gcc
CFLAGS = -O3 -DMaxSAT
target = tsm-mwc
all : $(target)

$(target) : TSM-Release1.0.3.c
	$(CC) $(CFLAGS) TSM-Release1.0.3.c -o $(target) -mcmodel=medium

clean :
	-rm $(target)
