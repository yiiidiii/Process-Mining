# Practical Course: Process Mining - Transformative Business Knowledge 

## Description

This is a project made as part of the Bachelor Practical Course: "Process Mining - Transformative Business Knowledge" at the Technical University of Munich.
It implements a simple [Alpha Miner](https://en.wikipedia.org/wiki/Alpha_algorithm) for Process Discovery and a small web application to visualize the results. 
You can upload an XES-file on the web application or choose from already given XES-files and let the Alpha Miner generate the respective petri-net and some statistics. 

The implementation of the Alpha algorithm mostly follows the steps introduced in [this book](https://www.academia.edu/40551325/Process_Mining_Wil_van_der_Aalst_Data_Science_in_Action_Second_Edition). 
The only difference is the implementation of step 4. An overview for step 4 and more information on this project (such as improvable aspects and the difficulties encountered during this project)
can be found in the PowerPoint presentation(s). 


## Installation

Please run the following commands from the root directory (/praktikum_process_mining).

Create a virtual environment and activate it:
```bash
source venv/bin/activate
```

Download all requirements:
```bash
pip install -r requirements.txt
```

Run on localhost:
```bash
python app.py
```

Run on server:
```bash
bash run_server.sh
```
Then open the URL "https://lehre.bpm.in.tum.de/ports/8006"

Run the tests:
```bash
python -m unittest test/static_tests.py
```

## Project status
finished