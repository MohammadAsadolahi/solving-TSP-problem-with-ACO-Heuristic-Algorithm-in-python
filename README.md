# Solving-TSP-with-ACO-python
solving tsp with ACO (ant colony optimization) in python
using heuristic algorithm to solve high dimensional tsp problem  
  cities are included in "Cities List.txt" in repo to add or remove cities you've got to include or exclude cities in every line like:  "1 909 649"  
    first number is city index and next two numbers are city euclidean coordinates: x,y which are set to 0 to 1000 but you can change the range to any range
    the distance between cities are calculated by Euclidean Distance which is:  
    ![Euclidean Distance](https://wikimedia.org/api/rest_v1/media/math/render/svg/2e0c9ce1b3455cb9e92c6bad6684dbda02f69c82)
    
  
# a random solution:
![random solution](https://github.com/mohammadAsadolahi/Solving-TSP-with-ACO-python/blob/main/random%20solution%20for%2020%20cities.png)
# route found by algorithm at iteration of 160(feeding algorithm with list of 20 city euclidean coordinates: x,y from 0 to 1000 ):
![iteration 160 solution](https://github.com/mohammadAsadolahi/Solving-TSP-with-ACO-python/blob/main/Best%20solution%20found%20at%20160%20iterations%20by%20colony.png) 
