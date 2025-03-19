# WinSim-CEID

WinSim is a proprietary simulator for an in-house microcontrollable board developed in 1997 at CEID, UPatras by Professor Dimitrios Nikolos. The simulator has basic copy protection which this repo aims to bypass by patching out the relevant calls. Obviously, we are not providing you with the executable, as this would violate national copyright law.

Tested with Python 3.11 and 3.12

## Installation

There is no installation required, this is just a simple script.

You can either clone the repository with git:
```sh
git clone https://github.com/LinkBoi00/WinSim-CEID.git WinSim-CEID
```
or download the repository as a .ZIP file from GitHub itself.

## Instructions

For Linux:
```sh
python3 winsim-patch.py --file "path\to\WinSim.exe"
```

For Windows:
```sh
python winsim-patch.py --file "C:\path\to\WinSim.exe"
```

## Explanation

Since we have a life and cannot spend our entire day on 1997s software, the info provided below may not be entirely correct. You are welcome to submit feedback from the Issues tab.

### Part 1 - License check window
-   Upon bootup the program calls a function to show the license validation window.
-   This function tries to read and validate a file called Memory.ico which is a hardware-locked license key generated below.
-   If that file is not found or is not valid for the computer it is running at, the program will show the user a randomly generated code (License Code 1) and prompt the user to enter the correct License Code 2 based on that
-   If License Code 2 matches with the provided License Code 1, the program generates Memory.ico for the user's computer, so that the verification doesn't have to be done each time.

### Part 2 - License Code 2 pattern
-   The copy protection in this program follows the classic 1990s approach where based on a set of (randomly generated) parameters, the user has to respond accordingly following an algorithm only known to them if the software had been purchased legally.
-   This challenge-based approach is obviously archaic by today's standards.
-   We can see that 'License Code 2' has 3 text boxes. The expected user inputs for each text box in that section (from now on called b1, b2, b3 respectively) is a mathematical function of the randomly generated parameters in License Code 1 (henceforth a1, a2, a3 respectively).
-   We can easily find out that the algorithm for License Code 2 is:
-   b1 = (4 * (a2 % a3 % 1522) + 3 * (a2 % a1 * (a2 % a1) % 2527) + (2 * (a1 % a3 * (a1 % a3) % 3128))) % 5000;
-   b2 = (5 * (a1 % a3 % 1128) + (3 * ((a3 + a2) % a1 * ((a3 + a2) % a1) % 2382))) % 5000;
-   b3 = (3 * (a1 + a3 + a2) % 4572 * ((a1 + a3 + a2) % 4572) + (4 * ((a2 + a1) % (a1 + a3)))) % 5000;

Due to the lack of sophistication, instead of messing with license generation, we can easily patch out license verification entirely. This repo replaces the calls made to the function that spawns the license window and checks for license verification with NOP calls. Specifically, we are patching the byte pattern "E8 03 E0 02 00 EB 0A" with "90 90 90 90 90 90 90".
