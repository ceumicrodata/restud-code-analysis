# Automated analysis of code submitted to the Review of Economic Studies
Each accapted manuscript at Restud contains a replication package: a ZIP file with data and code in some folder structure. The structure and naming of these files is up to the author. There are about 200 ZIP files of accepted manuscripts that have not yet been published.

- Reading the filenames in these ZIP files with a script (bash or python), flag each package based on what software they use: Stata, Matlab, R, Python, C, Fortran, bash. 
- Use common file extensions for each software. 
- (Advanced) Beware, some ZIP files contain other ZIP files inside. Treat these as folders.
- Create a table (.csv file) with manuscript number and an indicator for which language(s) the authors used. Packages often use multiple software.
- For a random sample of packages, review and score README files for content. Does it have enough information?
  - manifest: what the package contains
  - what the package does
  - what environment it needs
  - how to run it
  - data access and licensing
- (Advanced) Instead of indicator, report a count of the files consistent that language. I might have 30 .do files, for example, and 1 .sh script. This is `{'stata': 30, 'bash': 1, 'matlab': 0}` etc.
- Create beautiful charts of the software usage distribution. 
