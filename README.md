## Practical Course: Process Minining - Transformative Business Knowledge 

## Description

This is a project made as part of the Bachelor Parctical Course: "Process Minining - Transformative Business Knowledge" at the Technical University of Munich.
It implements a simple [Alpha Miner](https://en.wikipedia.org/wiki/Alpha_algorithm) for Process Discovery and a small web appllication to visualize the results. 
You can upload an XES-file on the web application or choose from already given XES-files and let the Alpha Miner generate the respective petri-net and some statistics. 

The implementation of the Alpha algorithm mostly follows the steps introduces in [this book](https://www.academia.edu/40551325/Process_Mining_Wil_van_der_Aalst_Data_Science_in_Action_Second_Edition). The only difference is the implementation of step 4, of which you can find a more detailled desciption in the powerpoint presentation. 


## Installation

Please run the following commands from the root directory (/praktikum_process_mining)

Download all requirements:
```bash
pip install -r requirements.txt
```

Run on localhost:
```bash
bash run_local.sh
```

Run on server:
```bash
bash run_server.sh
```

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.


## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.


## License
For open source projects, say how it is licensed.

## Project status
finished