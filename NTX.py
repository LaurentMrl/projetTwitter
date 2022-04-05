import networkx as nx
import matplotlib.pyplot as plt

G = nx.petersen_graph()

# PART 1 --------------------------------------------------------------------------------------------------------------------------------

# subax1 = plt.subplot(121)

# nx.draw(G, with_labels=False, font_weight='bold')

# subax2 = plt.subplot(122)

# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

# plt.show()  

# PART 2 --------------------------------------------------------------------------------------------------------------------------------


options = {
    # Couleur des ronds
    'node_color': 'blue',
    # Taille des ronds
    'node_size': 100,
    # épeisseur des liens
    'width': 1,

}

# subplot : Positionne les graphs dans l'image, 2 fois le même subplot va supersoser les graphs
subax1 = plt.subplot(221)

nx.draw_random(G, **options)

# --------------------------------------------------------------------------------------------------------------------------------

subax2 = plt.subplot(222)

nx.draw_circular(G, **options)

# --------------------------------------------------------------------------------------------------------------------------------

subax3 = plt.subplot(223)

nx.draw_spectral(G, **options)

# --------------------------------------------------------------------------------------------------------------------------------

subax4 = plt.subplot(224)

nx.draw_shell(G, nlist=[range(5,10), range(5)], **options)

# --------------------------------------------------------------------------------------------------------------------------------

G = nx.dodecahedral_graph()

shells = [[2, 3, 4, 5, 6], [8, 1, 0, 19, 18, 17, 16, 15, 14, 7], [9, 10, 11, 12, 13]]

nx.draw_shell(G, nlist=shells, **options)

nx.draw(G)

plt.savefig("pathFalse.png")