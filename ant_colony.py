import numpy as np




class CVPR:
    def __init__(self,graph:np.array,demande:list[int],n_vehicules:int,capacity:int):
        self.graph = graph
        self.demande = demande
        self.n_vehicules = n_vehicules
        self.n_points = len(self.graph)
        self.capacity = capacity
        self.pheromone = np.ones((self.n_points, self.n_points))

    def ant_colony_optimization(self,n_ants:int=50, n_iterations:int=1000, alpha:float=1, beta:float=1, evaporation_rate:float=0.9, Q:float=1):

        best_solution_length = float('inf')
        best_solution=None
        for iteration in range(n_iterations):
            # here we keep track of the paths of each ant in a given iteration
            solutions = []
            solution_lengths = []


            for ant in range(n_ants):
                
                # Initialize the ant's path
                depot=0
                visited = [False]*self.n_points
                # randomly select the starting point
                car_current_points = [depot for i in range(self.n_vehicules)]
                # set current point as visited
                visited[depot] = True
                # include the current point in the path
                car_paths = [[depot]for i in range(self.n_vehicules)]
                
                car_capacities=[self.capacity for i in range(self.n_vehicules)]
                # initialize the path length (cost)
                path_length = 0            
           
                probabilities = np.zeros((self.n_vehicules,self.n_points))
                for i in range(self.n_vehicules):                    
                        # initialize the probabilities of moving to each unvisited node
                    while False in visited:  # while not all nodes are visited
                        # calculate the probabilities of visiting each node
                        has_unvisited=False
                        for candidate in range(self.n_points):
                            if (car_capacities[i]-self.demande[candidate]>=0) and candidate!=car_current_points[i] and not visited[candidate]:
                                has_unvisited=True
                                probabilities[i][candidate] = self.pheromone[car_current_points[i], candidate]**alpha / self.graph[car_current_points[i], candidate]**beta
                            else:
                                probabilities[i][candidate]=0
                        probabilities[i]=np.nan_to_num(probabilities[i])
                        if np.sum(probabilities[i])==0 or not has_unvisited:  
                            break
            
                        probabilities[i] /= np.sum(probabilities[i])
                       
                        car_i_next_point = np.random.choice(self.n_points, p=probabilities[i])   
                        probabilities[:,car_i_next_point]=0
                        visited[car_i_next_point] = True
                        car_paths[i].append(car_i_next_point)

                        path_length += self.graph[car_current_points[i], car_i_next_point]
                        car_current_points[i]=car_i_next_point
                        car_capacities[i]-=self.demande[car_i_next_point]

                        #print(car_i_next_point)
                        
                
                # the current ant has completed its path (visited all nodes)
                # so we append the path and its cost to the paths and path_lengths lists
                solutions.append([car_paths])
                solution_lengths.append(path_length)
                # we update the global best progress
                
                if path_length < best_solution_length:
                    best_solution = car_paths
                    best_solution_length = path_length
                print(f'Iteration {iteration+1}/{n_iterations} - Best path length: {best_solution_length} - current path length: {path_length}')
                    

            # update the pheromone matrix after all ants have completed their paths
            self.pheromone *= evaporation_rate
            
            for solution, solution_length in zip(solutions, solution_lengths):
                for sub_path in solution[0] :
                    for i in range(len(sub_path)-1):
                        self.pheromone[sub_path[i], sub_path[i+1]] += Q/solution_length
                    self.pheromone[sub_path[-1], sub_path[0]] += Q/solution_length

            
        return best_solution, best_solution_length
