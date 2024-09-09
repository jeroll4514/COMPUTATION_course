class AbelianSandpile:
    """
    An Abelian sandpile model simulation. The sandpile is initialized with a random
    number of grains at each lattice site. Then, a single grain is dropped at a random
    location. The sandpile is then allowed to evolve until it is stable. This process
    is repeated n_step times.

    A single step of the simulation consists of two stages: a random sand grain is 
    dropped onto the lattice at a random location. Then, a set of avalanches occurs
    causing sandgrains to get redistributed to their neighboring locations.
    
    Parameters:
    n (int): The size of the grid
    grid (np.ndarray): The grid of the sandpile
    history (list): A list of the sandpile grids at each timestep
    """

    def __init__(self, n, random_state):
        self.n = n
        np.random.seed(random_state) # Set the random seed
        self.grid = np.random.choice([0, 1, 2, 3], size=(n, n))
        self.history =[self.grid.copy()]


    def step(self):
        """
        Perform a single step of the sandpile model. Step corresponds a single sandgrain 
        addition and the consequent toppling it causes. 
        """
        sand_drop = np.random.choice(self.n,2) #picks random x,y coordinate to add grain

        self.grid[sand_drop[0]][sand_drop[1]] += 1 #adds sand to sand_drop

        ind_store = [sand_drop.copy()] #will store indices for tracking avalanche
        while True:
            start_len = len(ind_store) #number of points to check
            if start_len == 0:
                break

            for coord in ind_store:
                rind,cind = coord #defines row index and column index

                if self.grid[rind][cind] < 4:
                    continue #skip to next coordinate if no avalanche
                    
                self.grid[rind][cind] -= 4 #OH NO AN AVALEANCHE

                #if-statements enforce boundary conditions
                if rind != 0:
                    self.grid[rind-1][cind] += 1
                    ind_store.append([rind-1,cind])
                if rind != self.n-1:
                    self.grid[rind+1][cind] += 1
                    ind_store.append([rind+1,cind])
                if cind != 0:
                    self.grid[rind][cind-1] += 1
                    ind_store.append([rind,cind-1])
                if cind != self.n-1:
                    self.grid[rind][cind+1] += 1
                    ind_store.append([rind,cind+1])
                
            del ind_store[:start_len] #only keeps new lattice sites to test

        '''
        #This will work, but is way too slow to reasonably perforn the n=100 test
        while True: #runs through grid until the sand is stable
            for rind in range(self.n): #iterates through lower rows originating at grain dropsite (slow)
                for cind in range(self.n): #iterates through each column (fast)

                    if self.grid[rind][cind] > 3: #finds event

                        #Avalanche event
                        self.grid[rind][cind] -= 4

                        #if statements enforce boundary conditions
                        if rind != 0:
                            self.grid[rind-1][cind] += 1
                        if rind != self.n-1:
                            self.grid[rind+1][cind] += 1
                        if cind != 0:
                            self.grid[rind][cind-1] += 1
                        if cind != self.n-1:
                            self.grid[rind][cind+1] += 1

            #Now finds maximum sand height.  If >3 then repeat process.  If <= 3 then complete.
            row_max = [max(row) for row in self.grid[:]] #list of max values for each row
            if max(row_max) <= 3:
                break #exits while loop
        '''

    # we use this decorator for class methods that don't require any of the attributes 
    # stored in self. Notice how we don't pass self to the method
    @staticmethod
    def check_difference(grid1, grid2):
        """Check the total number of different sites between two grids"""
        return np.sum(grid1 != grid2)

    
    def simulate(self, n_step):
        """
        Simulate the sandpile model for n_step steps.
        """
        for ii in range(n_step):
            self.step()
            self.history.append(self.grid.copy())