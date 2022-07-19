# Practical Course: Process Minining - Transformative Business Knowledge 

## Description

This is a project made as part of the Bachelor Parctical Course: "Process Minining - Transformative Business Knowledge" at the Technical University of Munich.
It implements a simple [Alpha Miner](https://en.wikipedia.org/wiki/Alpha_algorithm) for Process Discovery and a small web appllication to visualize the results. 
You can upload an XES-file on the web application or choose from already given XES-files and let the Alpha Miner generate the respective petri-net and some statistics. 

The implementation of the Alpha algorithm mostly follows the steps introduces in [this book](https://www.academia.edu/40551325/Process_Mining_Wil_van_der_Aalst_Data_Science_in_Action_Second_Edition). The only difference is the implementation of step 4, for which you can find a more detailled desciption in the powerpoint presentation. 


## Installation

Please run the following commands from the root directory (/praktikum_process_mining)

Download all requirements:
```bash
pip install -r requirements.txt
```

Activate the virtual environment:
```bash
source venv/bin/activate
```

Run on localhost:
```bash
bash run_local.sh
```

Run on server:
```bash
bash run_server.sh
```
Then open the URL "https://lehre.bpm.in.tum.de/ports/8006"


## Project status
finished