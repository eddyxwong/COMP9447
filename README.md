<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />




<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


Project developed by Frank Su, Eddy Wong, Zachary Ngooi and Alex Sanders for [COMP9447](https://www.handbook.unsw.edu.au/postgraduate/courses/2022/COMP9447?year=2022) during 22T2. Project name undecided. 

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org/doc/)
* [Python AST](https://docs.python.org/3/library/ast.html)

### Tests written using 
* [Pytest](https://docs.pytest.org/en/7.1.x/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

The file [requirements.txt](requirements.txt) contains a updated list of dependencies used in this project that can be installed using pip. This project was developed and tested on Python3 3.8.10 64-bit.

This project also uses existing CLI tooling for the feature to convert a json IAM policy to a Terraform template. Installation instructions 
can be found [here](https://github.com/flosell/iam-policy-json-to-terraform#installation). The 1.8.0 release is the version used in this 
project.

### Installation

1. Clone the repo
   ```sh
   $ git clone https://github.com/eddyxwong/COMP9447
   ```
2. Install dependencies
   ```sh
   $ pip install -r requirements.txt
   ```
3. Install any other dependencies. Refer to prerequisites.
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
1. cd into astStaticAnalysis directory
   ```sh
   $ cd astStaticAnalysis
   ```
2. Run program by adding -h flag to print a help message.
    ```sh
   $ python3 astBoto3.py -h
   ```
3. Files can be parse with no flags
    ```sh
   $ python3 astBoto3.py ./testDir/astTest.py ./testDir1/astTest1.py
4. Directorys can be parsed using the dir flag
    ```sh
   $ python3 astBoto3.py --dir ./testDir
   ```
5. IAC templates can be generated using either the tf or cfn flag
    ```sh
   $ python3 astBoto3.py --dir ./testDir --tf --cfn
   ```
6. Policy difference checker can you accessed by adding a diff flag
    ```sh
   $ python3 astBoto3.py --dir ./testDir --tf --cfn --diff
   ```

## Comparing Policies
1. cd into the astStaticAnalysis directory
   ```sh
   $ cd astStaticAnalysis
   ```
2. Run the program by moving the policies to be compared into the comparePolicies directory and parse the python scipt as command-line argumnet into [policyDiffChecker.py](./astStaticAnalysis/policyDiffChecker.py) and subsequently the name of the directory, comparePolicies.
   ```sh
   $ python3 policyDiffChecker.py comparePolicies
   ```

## Github Actions
1. Github Actions has been set-up to automate your policy generation workflow. The default branch that it runs on is when a push/pull is made on "main".
Follow the steps below to specify a different branch for github actions to run on
   ```sh
   $ cd .github/workflows/
   ```
2. Open the main.yml in an editing program. Change "main" in "branches: ["main"]" to the name of the branch you would like github actions to run on
   ```sh
   branches: ["Name Of Branch Here"]
   ```
3. The current workflow for github actions is 
[Scan for all .py Files] -> [Run policy generation tool on them] -> [Compare policy created with existing policies in the astStaticAnalysis\comparePolicies folder]

4. A summary of all automated actions is available in the "actions" tab in the repository under the corresponding worflow run. 
Either navigate to the job named:
   ```sh
   "Create The Master Analysis"
   ```
   locate the log named:
   ```sh
   "Displaying The Master Analysis" 
   ```
   or simply download the artifact named:
   ```sh
   "masterAnalysis"
   ```
   in the summary page for github actions 

## Tests
1. cd into tests directory
  ```sh
   $ cd tests
   ```
2. Run tests(Some tests fail to due testing of error handling which has not been implemented)
  ```sh
   $ pytest
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap
- [X] Decide on project name
- [X] IAM policy generator
- [X] Github Action integration
- [X] Policy 'git diff' checker
- [ ] Rules engine to account for policies granting permissions not used in codebase
See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE.txt](./LICENSE) for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* C.C
* F.P

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
