SOURCES  = $(wildcard *.c)
CC       = gcc
OBJECTS  = $(SOURCES:.c=.o)
INCLUDES = $(wildcard *.h)

all: tuntox

.c.o: $(INCLUDES)
	$(CC) $(CFLAGS) $(USER_CFLAGS) $< -c -o $@

tuntox: $(OBJECTS) $(INCLUDES)
	$(CC) -o $@ $(OBJECTS) $(LDFLAGS) $(USER_LDFLAGS) -ltoxcore -lsodium -pthread -lm -lrt

clean:
	rm -rf *.o tuntox
