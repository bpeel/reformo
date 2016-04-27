PROGS = maketiming
SDL_CFLAGS = `pkg-config sdl2 SDL2_image --cflags`
SDL_LIBS = `pkg-config sdl2 SDL2_image --libs`
CFLAGS = -g -Wall -O0 $(SDL_CFLAGS)

all : $(PROGS)

.c.o :
	gcc $(CFLAGS) -c -o $@ $<

maketiming : maketiming.o
	gcc -o $@ $^ $(SDL_LIBS)

clean :
	rm -f $(PROGS) *.o

.PHONY : clean all
