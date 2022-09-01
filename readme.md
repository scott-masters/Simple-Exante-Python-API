### Simple Python Exante API.

## Overview

This simple python script was written to allow python programs to interact with
the Exante trading platform. The Exante team has already created a python API, 
but that is a comprehensive and pretty complex project. I found it quite 
overwhelming when I was starting out.

By contrast this project contains only the functions that I use most often and I
have kept the code as short and simple as I could. The API sends HTTP commands
that are explained [here](https://api-live.exante.eu/api-docs/). The hope is 
that this basic API will be able to get you started and when you need functions 
that I have not included you will be able to grasp the pattern from what I have 
provided and add them in yourself.

## Setup

To use this API there are 9 steps:

1. Become an Exante customer by registering for an account (https://exante.eu/).
2. Login to the Client Area.
3. Under `Trading` select `HTTP API`.
4. Request access to the API.
5. Select the `Applications` tab and create a new application.
6. Download this GitHub project onto your machine.
7. Open the `checks.py` file and fill out your personal information.
    - Your account is visable is you select `Summary` under `Account`.
    - The `app_id` and `shared_key` can be found in the `Applications` tab.
    - Your `client_id` is in the `Access` tab.
    - The `end_point` is either https://api-demo.exante.eu/ for demo accounts or 
    https://api-live.exante.eu/ for live accounts.
8. Run the `checks.py` script (ideally with python 3.10) to make sure everything 
is working correctly.
9. Begin integrating the Exante client into your own project.

## License and Disclaimers

Anyone is free to use this code however they wish and do not need to acknowledge
this project as a source.

I have endeavored to make this code work on a best efforts basis only and 
disclaim all legal responsibility if it does not work as intended.

I am not associated with Exante in any way, other than being one of their
clients.

I am happy to try to answer questions and resolve bugs.
I am happy to try to answer questions and resolve bugs, you can email me at 
scott.masters@protonmail.com.