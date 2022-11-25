# compilateur
CPP := g++
# options de compilation
CFLAGS := -std=c++98 -Wall -Wextra -pedantic -Wno-unused-variable -Wno-unused-parameter
# les options -Wno-unused-variable -Wno-unused-parameter
# sont recommandées mais non obligatoires
# all est la cible par défaut choisie par la commande make
# elle dépend de la règle executable, qui va être réalisée
# en fonction de la description donnée dans la suite
all : executable
TARGET := target/
SRC := src/
HPP := $(wildcard src/*.hpp)

EXEC := executable 
run : all	
	for exec in $(EXEC); do ./$$exec; done 

clean :
	rm -f $(TARGET)*


executable :   $(TARGET)main.o $(TARGET)Point.o  $(TARGET)exercice3.o
			$(CPP) $(CFLAGS) -o $@ $^ -lm


memoire : all
		valgrind  --leak-check=full  ./$(EXEC) 



$(TARGET)%.o : $(SRC)%.cpp $(HPP)
				$(CPP) $(CFLAGS) -o $@ -c $<




