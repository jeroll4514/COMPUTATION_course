import numpy as np

class PercolationSimulation:
    """
    A simulation of a 2D directed percolation problem. Given a 2D lattice, blocked sites
    are denoted by 0s, and open sites are denoted by 1s. During a simulation, water is
    poured into the top of the grid, and allowed to percolate to the bottom. If water
    fills a lattice site, it is marked with a 2 in the grid. Water only reaches a site
    if it reaches an open site directly above, or to the immediate left or right 
    of an open site.

    I've included the API for my solution below. You can use this as a starting point, 
    or you can re-factor the code to your own style. Your final solution must have a 
    method called percolate that creates a random lattice and runs a percolation 
    simulation and
    1. returns True if the system percolates
    2. stores the original lattice in self.grid
    3. stores the water filled lattice in self.grid_filled

    + For simplicity, use the first dimension of the array as the percolation direction
    + For boundary conditions, assume that any site out of bounds is a 0 (blocked)
    + You should use numpy for this problem, although it is possible to use lists 



    Attributes:
        grid (np.array): the original lattice of blocked (0) and open (1) sites
        grid_filled (np.array): the lattice after water has been poured in
        n (int): number of rows and columns in the lattice
        p (float): probability of a site being blocked in the randomly-sampled lattice
            random_state (int): random seed for the random number generator
        random_state (int): random seed for numpy's random number generator. Used to 
            ensure reproducibility across random simulations. The default value of None
            will use the current state of the random number generator without resetting
            it.
    """

    def __init__(self, n=100, p=0.5, grid=None, random_state=None):
        """
        Initialize a PercolationSimulation object.

        Args:
            n (int): number of rows and columns in the lattice
            p (float): probability of a site being blocked in the randomly-sampled lattice
            random_state (int): random seed for numpy's random number generator. Used to
                ensure reproducibility across random simulations. The default value of None
                will use the current state of the random number generator without resetting
                it.
        """

        self.random_state = random_state #for storage
        np.random.seed(self.random_state) #the random seed

        # Initialize a random grid if one is not provided. Otherwise, use the provided
        # grid.
        if grid is None:
            self.n = n
            self.p = p
            self.grid = np.zeros((n, n))
            self._initialize_grid()
        else:
            assert len(np.unique(np.ravel(grid))) <= 2, "Grid must only contain 0s and 1s"
            self.grid = grid.astype(int)
            # override numbers if grid is provided
            self.n = grid.shape[0]
            self.p = 1 - np.mean(grid)

        # The filled grid used in the percolation calculation. Initialize to the original
        # grid. We technically don't need to copy the original grid if we want to save
        # memory, but it makes the code easier to debug if this is a separate variable 
        # from self.grid.
        self.grid_filled = np.copy(self.grid)

    def _initialize_grid(self):
        """
        Sample a random lattice for the percolation simulation. This method should
        write new values to the self.grid and self.grid_filled attributes. Make sure
        to set the random seed inside this method.

        This is a helper function for the percolation algorithm, and so we denote it 
        with an underscore in order to indicate that it is not a public method (it is 
        used internally by the class, but end users should not call it). In other 
        languages like Java, private methods are not accessible outside the class, but
        in Python, they are accessible but external usage is discouraged by convention.

        Private methods are useful for functions that are necessary to support the 
        public methods (here, our percolate() method), but which we expect we might need
        to alter in the future. If we released our code as a library, others might 
        build software that accesses percolate(), and so we should not alter the 
        input/outputs because it's a public method
        """

        for rind in range(self.n): #iterates over grid rows (slow)
            for cind in range(self.n): #iterates over grid cols (fast)
                #randomly assigns percolation walls according to probability p
                if np.random.random() > self.p:
                    self.grid[rind][cind] = 1 #0 is blocked, 1 is open
        

    def _poll_neighbors(self, i, j):
        """
        Check whether there is a filled site adjacent to a site at coordinates i, j in 
        self.grid_filled. Respects boundary conditions.

        Returns True/False if the following cell is filled/blocked [Left,Right,Up,Down]
        """

        output = [False,False,False,False] #whether the water can travel left, right, up, or down

        if j != 0: #not on the left boundary
            if self.grid_filled[i][j-1] == 1: #Left
                output[0] = True
        if j != self.n-1: #not on right boundary
            if self.grid_filled[i][j+1] == 1: #Right
                output[1] = True
        if i != 0: #not on upper boundary
            if self.grid_filled[i-1][j] == 1: #Up
                output[2] = True
        if i != self.n-1: #not on lower boundary
            if self.grid_filled[i+1][j] == 1: #Down
                output[3] = True

        return output

    
    def _flow_recursive(self, i, j):
        """
        Only used if we opt for a recursive solution.

        The recursive portion of the flow simulation. Notice how grid and grid_filled
        are used to keep track of the global state, even as our recursive calls nest
        deeper and deeper
        """

        movement = self._poll_neighbors(i,j) #has valid directions water can move (left,right,up,down)

        if movement[0] == True: #Water can move left
            self.grid_filled[i][j-1] = 2
            self._flow_recursive(i,j-1)
        if movement[1] == True: #Water can move right
            self.grid_filled[i][j+1] = 2
            self._flow_recursive(i,j+1)
        if movement[2] == True: #Water can move up
            self.grid_filled[i-1][j] = 2
            self._flow_recursive(i-1,j)
        if movement[3] == True: #Water can move down
            self.grid_filled[i+1][j] = 2
            self._flow_recursive(i+1,j)


    def percolate(self):
        """
        Initialize a random lattice and then run a percolation simulation. Report results
        """

        for cind in range(self.n): #iterates over columns within top row
            if self.grid[0][cind] == 1: #if starting cell is open
                self.grid_filled[0][cind] = 2 #puts water in starting cell
                self._flow_recursive(0,cind) #water flows
        
        #outputs if percolation completes or not
        return 2 in self.grid_filled[-1]