from grid import Grid 
from blocks import IBlock, JBlock, OBlock, SBlock, TBlock
import random



class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), OBlock(), SBlock(), TBlock()]
        self.next_block = self.get_random_block()
        self.current_block = self.get_random_block()
        self.game_over = False
        self.score = 0

    def update_score(self, line_cleared, moved_down_points):
        if line_cleared == 1:
            self.score += 100
        elif line_cleared == 2:
            self.score += 300
        elif line_cleared == 3:
            self.score += 500
        self.score += moved_down_points


    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), OBlock(), SBlock(), TBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
       

        block.row_offset = 0
        block.column_offset = 3
        return block


    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if tile.row < 0 or tile.row >= self.grid.num_rows or tile.column < 0 or tile.column >= self.grid.num_cols:
                return False
        return True

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if tile.row >= 0:  
                if (tile.row >= self.grid.num_rows or 
                    tile.column >= self.grid.num_cols or 
                    tile.column < 0 or 
                    self.grid.grid[tile.row][tile.column] != 0):
                    return False
        return True

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            if (position.row >= 0 and position.row < self.grid.num_rows and 
                position.column >= 0 and position.column < self.grid.num_cols):
                self.grid.grid[position.row][position.column] = self.current_block.id
        rows_cleared = self.grid.clean_full_rows()
        self.update_score(rows_cleared, 0)
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        if self.block_fits() == False:
            self.game_over = True


    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), OBlock(), SBlock(), TBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0


        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        self.grid.clean_full_rows()
        

        if not self.block_fits():
            self.game_over = True


    def move_left(self):
        if not self.game_over:
            self.current_block.move(0, -1)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move(0, 1)


    def move_right(self):
        if not self.game_over:
            self.current_block.move(0, 1)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move(0, -1)


    def move_down(self):
        if not self.game_over:
            self.current_block.move(1, 0)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move(-1, 0)
                self.lock_block()
                return False
            return True
        return False


    def rotate(self):
        if not self.game_over:
            self.current_block.rotate()
            if not self.block_inside() or not self.block_fits():
                self.current_block.undo_rotation()



    def draw(self, screen):
        self.grid.draw(screen)
        if not self.game_over:
            self.current_block.draw(screen, 11, 11)
            if self.next_block.id == 3:
                self.next_block.draw(screen, 255, 290)
            elif self.next_block.id == 4:
                self.next_block.draw(screen, 255, 280)
            else:
                self.next_block.draw(screen, 270, 270)