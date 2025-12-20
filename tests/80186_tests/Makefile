
# build all .asm that starts with a number
# use nasm to generate .bin, then append `ea 00 00 00 f0` to FFF0 as
# reset vector and `ff` to FFFF

SRCS := 01.xor_after_add.asm
BINS := $(SRCS:.asm=.bin)

all: $(BINS)

%.bin0: %.asm
	nasm -f bin -o $@ -l $*.lst $<

%.bin: %.bin0
	python prepare_test.py $*

clean:
	rm -f $(BINS)
