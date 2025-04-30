"""
Task4
Description:
This program tests geometric classes. It prompts the user to input parameters for a Rhombus,
creates the object, prints its details, draws the figure (fills it in the chosen color and annotates it
with user-entered text), and saves the drawing to a file.
"""
import matplotlib
import matplotlib.pyplot as plt
from geometry import Rhombus
from inputs_check import input_float_with_condition, input_color_matplotlib


def draw_rhombus(rhombus: Rhombus, label_text: str, save_filename: str) -> None:
    """
    Draws the rhombus using matplotlib with one horizontal diagonal,
    fills it with the chosen color, annotates it with label_text,
    and saves the plot to a file.

    Args:
        rhombus (Rhombus): The Rhombus object.
        label_text (str): Text to label the figure.
        save_filename (str): File name for saving the plot.
    """
    a = rhombus.a
    b = rhombus.b
    # Vertices of a rhombus with horizontal diagonal:
    vertices = [
        (a / 2, 0),
        (0, b / 2),
        (-a / 2, 0),
        (0, -b / 2)
    ]
    # Close the polygon:
    vertices.append(vertices[0])
    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]

    plt.figure(figsize=(6, 6))
    plt.fill(x_coords, y_coords, color=rhombus.figure_color, alpha=0.5, label='Ромб')
    plt.plot(x_coords, y_coords, color='black')
    plt.title("Геометрическая фигура: Ромб")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis('equal')

    plt.text(0, 0, label_text, fontsize=12, ha='center', va='center')
    plt.legend()
    plt.savefig(save_filename)
    plt.show()


def task4():
    print("Построение ромба с заданными диагоналями.")
    a = input_float_with_condition("Введите значение диагонали a (горизонтальная): ", lambda x: x > 0)
    b = input_float_with_condition("Введите значение диагонали b (вертикальная): ", lambda x: x > 0)
    color = input_color_matplotlib('Введите цвет фигуры (например, blue, red, green): ')

    label_text = input("Введите текст для подписи фигуры: ").strip()

    rhombus = Rhombus(a, b, color)
    print("\nИнформация о ромбе:")
    print(rhombus)

    save_filename = "files/rhombus.png"
    draw_rhombus(rhombus, label_text, save_filename)
    print(f"Рисунок фигуры сохранён в файл: {save_filename}")


if __name__ == "__main__":
    task4()
