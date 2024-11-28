
class Graph:
    def __init__(self):
        self.vertices = []  # Список вершин
        self.edges = {}     # Словарь смежности для рёбер

def test_simple_graph():
    graph = Graph()
    graph.vertices = [0, 1, 2, 3]
    graph.edges = {
        0: [1, 2],
        1: [0, 3],
        2: [0],
        3: [1]
    }
    
    # Ожидаем, что остовное дерево будет содержать рёбра [(0, 1), (0, 2), (1, 3)]
    spanning_tree = graph.get_spanning_tree_dfs()
    
    print("Тест 1: Простой граф")
    print("Остовное дерево:")
    print(spanning_tree)
    # Ожидаемый результат: [(0, 1), (0, 2), (1, 3)]
    graph.visualize_graph(spanning_tree)
