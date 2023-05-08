# ECC
The Economic Cycle Clock aka Business Cycle Clock shows the economic growth cycle for a country or region. Usually the GDP is used, but several underlying statistics correlate with this but with various lags (positive or negative).

Currently it just runs a GitHub Action every Monday to fetch data from SCB (Sweden), transform it, and save to file that is committed to the data-directory.

TODO:  
[ ] Create action for incorporating new data into a plotlyt graph and output to html + commit.  
[ ] Create Github Pages for project and serve the generated HTML file.  
