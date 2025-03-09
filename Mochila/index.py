from textual.app import App, ComposeResult
from textual.widgets import Input, Label, Button, ListView, ListItem, Static, Digits
from textual.containers import Vertical, Horizontal


class InputWithLabel(Horizontal):
    """Componente reutilizable para un input con etiqueta."""

    def __init__(self, label_text: str, placeholder: str = "") -> None:
        super().__init__()
        self.label_text = label_text
        self.placeholder = placeholder

    def compose(self) -> ComposeResult:
        yield Label(self.label_text, classes="input-label")
        yield Input(placeholder=self.placeholder, classes="input-field")

    def get_value(self) -> str:
        """Obtiene el valor del input."""
        return self.query(Input).first().value


class GroupCard(Vertical):
    """Tarjeta contenedora de un grupo de Beneficio/Peso con botón de eliminación."""

    def __init__(self, knapsack_app, group_id: int):  # Renombrar "app" para evitar conflicto
        super().__init__()
        self.knapsack_app = knapsack_app  # Cambio aquí
        self.group_id = group_id
        self.benefit_input = InputWithLabel("Beneficio", "Ej: 25")
        self.weight_input = InputWithLabel("Peso", "Ej: 18")
        self.delete_button = Button("Eliminar", id=f"delete_{group_id}")
        self.update_visibility()

    def compose(self) -> ComposeResult:
        yield Horizontal(
            self.benefit_input,
            self.weight_input,
            self.delete_button
        )

    def get_values(self) -> tuple:
        """Obtiene los valores de beneficio y peso."""
        return (
            self.benefit_input.get_value().strip(),
            self.weight_input.get_value().strip(),
        )

    def update_visibility(self):
        """Oculta el botón de eliminar si solo queda un grupo."""
        self.delete_button.visible = len(self.knapsack_app.groups) > 1  


class KnapsackApp(App):
    """Aplicación interactiva del problema de la mochila."""

    CSS = """
    Screen {
        align: center middle;
    }
    .input-label {
        width: 12;
        text-align: right;
        padding: 1;
    }
    .input-field {
        width: 1fr;
    }
    ListView {
        height: 10;
        width: 50%;
        margin: 1;
    }
    Button {
        margin: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.groups = []  # Lista de grupos de Beneficio/Peso
        self.next_group_id = 1  # ID único para cada grupo

    def compose(self) -> ComposeResult:
        self.capacity_input = InputWithLabel("Capacidad Mochila", "Ej: 20")
        self.add_group_button = Button("Añadir Grupo", id="add_group")
        self.add_button = Button("Calcular", id="add_objects")

        self.object_list = ListView()
        self.group_container = Vertical()

        yield Vertical(
            self.capacity_input,
            self.add_group_button,
            self.group_container,  # Contenedor dinámico de grupos
            self.add_button,
            Static("Resultados:", classes="title"),
            self.object_list,
        )

    def on_mount(self):
        """Se ejecuta cuando la aplicación ya ha montado todos los elementos."""
        self.add_group()  # Ahora es seguro agregar el primer grupo

    def add_group(self):
        """Añade un nuevo grupo de Beneficio/Peso."""
        group = GroupCard(self, self.next_group_id)
        self.groups.append(group)
        self.group_container.mount(group)
        self.next_group_id += 1
        self.update_group_buttons()

    def remove_group(self, group_id: int):
        """Elimina solo el grupo específico."""
        group_to_remove = None

        # Buscar el grupo a eliminar
        for group in self.groups:
            if group.group_id == group_id:
                group_to_remove = group
                break

        if group_to_remove:
            self.groups.remove(group_to_remove)  # Eliminar de la lista
            group_to_remove.remove()  # Eliminar del UI

        self.update_group_buttons()  # Actualizar visibilidad del botón "Eliminar"

    def update_group_buttons(self):
        """Actualiza la visibilidad del botón de eliminar en los grupos."""
        for group in self.groups:
            group.update_visibility()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja los eventos de botones."""
        if event.button.id == "add_group":
            self.add_group()

        elif event.button.id.startswith("delete_"):
            group_id = int(event.button.id.split("_")[1])
            self.remove_group(group_id)

        elif event.button.id == "add_objects":
            capacidad = float(self.capacity_input.get_value().strip())

            # Recoger los valores y pesos de cada grupo
            objetos = []
            for group in self.groups:  # Cambié de .values() a simplemente recorrer self.groups
                value, weight = group.get_values()
                try:
                    value = float(value)
                    weight = float(weight)
                    objetos.append((value, weight))
                except ValueError:
                    pass  # Ignorar si no son números válidos

            beneficio, seleccionados = mochila_fracionaria(capacidad, objetos)

            self.object_list.clear()  # Limpiar la lista de objetos
            self.object_list.append(ListItem(Label(f"Maximo Beneficio : {beneficio}")))

            for valor, peso, fraccion in seleccionados:
                item_text = f"\n Beneficio: {valor}, Peso: {peso}, Fracción: {fraccion:.2f}"
                self.object_list.append(ListItem(Label(item_text)))


def mochila_fracionaria(capacidad, valores):
    """    
    :parametro capacidad: Capacidad máxima de la mochila
    :parametro valores: Lista de tuplas (valor, peso) de cada objeto
    :devuelve: Máximo beneficio y los objetos seleccionados con sus fracciones
    """
    # Ordenar los objetos en base a la mejor relación valor/peso (descendente)
    valores.sort(key=lambda x: x[0] / x[1], reverse=True)

    print(valores)
    
    total_beneficio = 0  
    contenido_mochila = [] 
    
    for beneficio, peso in valores:
        if capacidad >= peso:  
            # Si el objeto cabe completo, lo tomamos
            contenido_mochila.append((beneficio, peso, 1))  # Se toma el 100% (1)
            total_beneficio += beneficio
            capacidad -= peso
        else:
            # Si no cabe completo, tomamos la fracción que cabe
            fraccion = capacidad / peso
            contenido_mochila.append((beneficio, peso, fraccion))  
            total_beneficio += beneficio * fraccion
            break 
    
    return total_beneficio, contenido_mochila


if __name__ == "__main__":
    app = KnapsackApp()
    app.run()
