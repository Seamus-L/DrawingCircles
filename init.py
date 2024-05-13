import pygame
import sys
import math
import pygame.gfxdraw

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Nodes and Edges")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Node:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.dragging = False
        self.resizing = False

    def draw(self):
        # pygame.gfxdraw.filled_circle(screen, self.x, self.y, self.size, WHITE)
        pygame.gfxdraw.aacircle(screen, self.x, self.y, self.size, WHITE)

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def update_size(self, new_size):
        self.size = new_size

# Calculate tangent points between two circles
def calculate_tangent_points(node1, node2, pinch): #Takes arguments for each node, and whether or not it is a top tangent
    dist = math.hypot(node2.x - node1.x, node2.y - node1.y)
    if dist == 0:
        return (node1.x, node1.y), (node1.x, node1.y)  # Nodes are coincident, no tangents
    radius_sum = node1.size + node2.size
    if dist <= radius_sum:
        return (node1.x, node1.y), (node2.x, node2.y)  # Circles are overlapping, no tangents
    theta = math.atan2(node2.y - node1.y, node2.x - node1.x) #Theta captures the orientation of the circles in a plane - center to center
    theta += math.pi / 2  # Rotate 90 degrees to find tangent

    phi = math.asin(abs(node1.size-node2.size)/dist)  #Phi captures the adjustments in tangent angle due to the differences in radii of the circles

    if node1.size > node2.size:
        x1 = node1.x + node1.size * math.cos(theta-phi)
        y1 = node1.y + node1.size * math.sin(theta-phi)
        x2 = node2.x + node2.size * math.cos(theta-phi)
        y2 = node2.y + node2.size * math.sin(theta-phi)
        return (x1, y1), (x2, y2)
    else:
        x1 = node1.x + node1.size * math.cos(theta+phi)
        y1 = node1.y + node1.size * math.sin(theta+phi)
        x2 = node2.x + node2.size * math.cos(theta+phi)
        y2 = node2.y + node2.size * math.sin(theta+phi)
        return (x1, y1), (x2, y2)


# Create a list to store nodes
nodes = [
    Node(250, 300, 20),
    Node(550, 300, 20),
    Node(400, 100, 20)
]

# Main event loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for node in nodes:
                if node.x - node.size <= mouse_x <= node.x + node.size and \
                   node.y - node.size <= mouse_y <= node.y + node.size:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        node.resizing = True
                    else:
                        node.dragging = True
                    offset_x = node.x - mouse_x
                    offset_y = node.y - mouse_y
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            for node in nodes:
                node.dragging = False
                node.resizing = False
        elif event.type == pygame.MOUSEMOTION:
            for node in nodes:
                if node.dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    node.update_position(mouse_x + offset_x, mouse_y + offset_y)
                elif node.resizing:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_size = max(abs(mouse_x - node.x), abs(mouse_y - node.y))
                    node.update_size(new_size)

    # Fill the background with black
    screen.fill((0, 0, 0))

#Draw edges between nodes
    for i in range(len(nodes)):      
        if i < len(nodes)-1:
            tangent_point1, tangent_point2 = calculate_tangent_points(nodes[i], nodes[i+1], 0)
            pygame.gfxdraw.line(screen, int(tangent_point1[0]), int(tangent_point1[1]), 
                    int(tangent_point2[0]), int(tangent_point2[1]), RED)
        else: 
            tangent_point1, tangent_point2 = calculate_tangent_points(nodes[len(nodes)-1], nodes[0], 0)
            pygame.gfxdraw.line(screen, int(tangent_point1[0]), int(tangent_point1[1]), 
                    int(tangent_point2[0]), int(tangent_point2[1]), RED)
            

    # TO DO:
        #Create array/list of tangent points to draw polygon
        #Add functionality to add additional circles along tangents
            #Must index them in node array properly
        #Add functionality to add subtractive circles as well (tangent drawn on other side pinch = 1)
            #Make subtractive (Pinching) circles fill BLACK to create illusion of filling.
        #Add restrictions to moving circles to violating tangency and pushing through tangent lines (THIS IS REALLY HARD)
        #Add alignment
        #Add reset
            #Hard reset entire canvas
            #Soft reset (double click) circle to reset size to 20
        #Add preset/save?
            #Should also add way to export as png? Can upscale as well due to vector nature.



            # pygame.gfxdraw.line(screen, int(tangent_point3[0]), int(tangent_point3[1]),
            #                     int(tangent_point4[0]), int(tangent_point4[1]), RED)
            # # Fill the area bounded by the tangent lines with solid white
            # pygame.draw.polygon(screen, WHITE, [tangent_point1, tangent_point2, tangent_point4, tangent_point3])


    # Draw all nodes
    for node in nodes:
        node.draw()

    # Update display
    pygame.display.flip()
