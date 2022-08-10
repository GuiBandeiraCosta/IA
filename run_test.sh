#!/bin/bash

for i in {1..10}; do echo -n "Running test $i"; diff tests_final_public/output$i.txt <(time python3 numbrix.py tests_final_public/input$i.txt $1); echo; done
