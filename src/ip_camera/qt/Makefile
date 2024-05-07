# Name of your executable 
EXECUTABLE = gui

# Compiler and flags
CXX = g++
CXXFLAGS = -Wall -g

# Required libraries (obtained from pkg-config)
GSTREAMER_LIBS = `pkg-config --libs gstreamer-1.0 gstreamer-video-1.0`
QT_LIBS = `pkg-config --libs QtCore QtGui QtWidgets`

# Include directories (if needed, obtained from pkg-config)
GSTREAMER_INCDIRS = `pkg-config --cflags gstreamer-1.0 gstreamer-video-1.0`
QT_INCDIRS = `pkg-config --cflags QtCore QtGui QtWidgets`

# All the object files from your sources 
OBJECTS = main.o

# Main rule to build the executable 
all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
		$(CXX) $(CXXFLAGS) $(OBJECTS) -o $@ $(QT_LIBS) $(GSTREAMER_LIBS) 

# Rule to create object files 
main.o: gui.cpp
		$(CXX) $(CXXFLAGS) $(QT_INCDIRS) $(GSTREAMER_INCDIRS) -c $< -o $@

# Cleaning up
clean:
		rm -f $(OBJECTS) $(EXECUTABLE)