import tkinter as tk

root = tk.Tk()
root.geometry("600x670")

# Crear canvas
canvas = tk.Canvas(root, width=600, height=670)
canvas.pack()

# Cargar imagen de la cancha
field_image = tk.PhotoImage(file="imagenes/canchita.png")
canvas.create_image(300, 335, image=field_image)

# Cargar imágenes de jugadores
player_images = {}
for i in range(1, 12):
    player_images[i] = tk.PhotoImage(file=f"imagenes/jugador{i}.png")

# Posiciones para formación 4-3-3
positions = {
    1: (300, 550),  # Portero
    2: (100, 400),  # Defensa 1
    3: (200, 400),  # Defensa 2
    4: (400, 400),  # Defensa 3
    5: (500, 400),  # Defensa 4
    6: (150, 250),  # Medio 1
    7: (300, 250),  # Medio 2
    8: (450, 250),  # Medio 3
    9: (150, 100),  # Delantero 1
    10: (300, 100), # Delantero 2
    11: (450, 100)  # Delantero 3
}

# Crear imágenes de jugadores en posiciones
player_ids = {}
for player, pos in positions.items():
    player_ids[player] = canvas.create_image(pos[0], pos[1], image=player_images[player])

# Variable para selección
selected_player = None

def on_click(event):
    global selected_player
    # Encontrar qué imagen fue clickeada
    clicked_id = canvas.find_closest(event.x, event.y)[0]
    if clicked_id in player_ids.values():
        # Encontrar el jugador correspondiente
        for player, pid in player_ids.items():
            if pid == clicked_id:
                clicked_player = player
                break
        if selected_player is None:
            selected_player = clicked_player
            # Resaltar (opcional: cambiar tamaño o algo)
            canvas.scale(clicked_id, event.x, event.y, 1.1, 1.1)
        elif selected_player == clicked_player:
            # Deseleccionar
            canvas.scale(clicked_id, event.x, event.y, 1/1.1, 1/1.1)
            selected_player = None
        else:
            # Intercambiar posiciones
            pos1 = positions[selected_player]
            pos2 = positions[clicked_player]
            # Mover imágenes
            canvas.coords(player_ids[selected_player], pos2[0], pos2[1])
            canvas.coords(player_ids[clicked_player], pos1[0], pos1[1])
            # Actualizar posiciones
            positions[selected_player], positions[clicked_player] = pos2, pos1
            # Deseleccionar
            canvas.scale(player_ids[selected_player], pos2[0], pos2[1], 1/1.1, 1/1.1)
            selected_player = None

# Bind click event
canvas.bind("<Button-1>", on_click)

root.mainloop()

