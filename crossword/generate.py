import copy
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var, words in self.domains.items():
            old_words = words.copy()
            for word in old_words:
                if var.length != len(word):
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False  # Indicates if x's domain was changed
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:  # If there's no overlap btw variables, consistency is assured
            return False
        old_words = self.domains[x].copy()
        for word in old_words:
            valid = False  # Indicates there's a consistent option for this word in y's domain
            for word_y in self.domains[y]:
                if word[overlap[0]] == word_y[overlap[1]]:
                    valid = True
                    break
            if not valid:
                self.domains[x].remove(word)
                revision = True

        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Find all arcs for initial queue.
        if arcs is None:
            arcs = [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]

        while len(arcs) > 0:
            arc = arcs.pop(0)  # First in, first out
            if self.revise(*arc):  # If x's domain was modified during arc consistency check...
                if len(self.domains[arc[0]]) == 0:  # If domain is empty
                    return False
                new_arcs = [(arc[0], y) for y in self.crossword.neighbors(arc[0]) if y != arc[1]]
                arcs.extend(new_arcs)  # ... need to re-check all of x's arcs

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if len(assignment.values()) != len(set(assignment.values())):  # Check all answers are unique
            return False

        for var, answer in assignment.items():
            if len(answer) != var.length:  # Check length match
                return False
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment.keys():  # Only check neighbors that have been assigned
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap is not None:
                        # Check that overlaps are correct
                        if assignment[var][overlap[0]] != assignment[neighbor][overlap[1]]:
                            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = self.crossword.neighbors(var)
        counts = {word: 0 for word in self.domains[var]}  # Initialize count of ruled-out words

        for value in self.domains[var]:
            for neighbor in neighbors:
                if neighbor not in assignment.keys():  # Ignore vars that are already assigned
                    overlap = self.crossword.overlaps[var, neighbor]
                    for n_value in self.domains[neighbor]:
                        # Ignore values already assigned
                        if n_value not in assignment.values() and value[overlap[0]] == n_value[overlap[1]]:
                            counts[value] += 1  # Restrains one more

        return sorted(self.domains[var], key=lambda value: counts[value])  # Sort using counts

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        remaining = set(self.crossword.variables) - set(assignment.keys())
        min_remaining_count = min(len(self.domains[var]) for var in remaining)  # Get smallest domain size
        # Only keep vars with smallest domain size
        ordered_remaining = [var for var in remaining if len(self.domains[var]) == min_remaining_count]
        if len(ordered_remaining) > 1:  # If tied, sort by degree
            ordered_remaining = sorted(ordered_remaining, key=lambda x: len(self.crossword.neighbors(x)))

        return ordered_remaining[-1]  # Return highest degree

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment  # Already finished

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            test_assignment = assignment.copy()
            test_assignment[var] = value
            if self.consistent(test_assignment):
                result = self.backtrack(test_assignment)
                if result is not None:
                    return result

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
