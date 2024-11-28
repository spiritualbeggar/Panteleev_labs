import random
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.vertices = []  # Список вершин
        self.edges = {}     # Словарь смежности для рёбер

    def generate_random_graph(self):
        """Генерация случайного графа."""
        num_vertices = random.randint(3, 10)  # Случайное количество вершин от 3 до 10
        self.vertices = [i for i in range(num_vertices)]
        
        # Случайное создание рёбер
        for v in self.vertices:
            self.edges[v] = []
            num_edges = random.randint(1, min(3, num_vertices - 1))  # Ограничиваем количество рёбер
            connections = random.sample(self.vertices, num_edges)
            for c in connections:
                if c != v and c not in self.edges[v]:
                    self.edges[v].append(c)
                    self.edges.setdefault(c, []).append(v)  # Обратное ребро для неориентированного графа

    def dfs(self, start, visited, spanning_tree_edges):
        """Рекурсивный поиск в глубину (DFS) для построения остовного дерева."""
        visited.add(start)
        for neighbor in self.edges[start]:
            if neighbor not in visited:
                # Добавляем ребро в остовное дерево
                spanning_tree_edges.append((start, neighbor))
                self.dfs(neighbor, visited, spanning_tree_edges)

    def get_spanning_tree_dfs(self):
        """Построение остовного дерева методом поиска в глубину (DFS)."""
        visited = set()
        spanning_tree_edges = []
        # Запуск DFS из первой вершины, если она существует
        if self.vertices:
            self.dfs(self.vertices[0], visited, spanning_tree_edges)
        return spanning_tree_edges

    def print_graph(self):
        """Вывод графа и остовного дерева в консоль."""
        print("Сгенерированный граф:")
        for v in self.vertices:
            print(f"{v}: {self.edges[v]}")
        
        spanning_tree = self.get_spanning_tree_dfs()
        print("\nОстовное дерево (DFS):")
        for edge in spanning_tree:
            print(edge)
        
        self.visualize_graph(spanning_tree)

    def visualize_graph(self, spanning_tree_edges):
        """Визуализация графа и его остовного дерева."""
        G = nx.Graph()
        G.add_nodes_from(self.vertices)
        G.add_edges_from([(u, v) for u in self.edges for v in self.edges[u]])

        # Отображаем граф
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)  # Расположение вершин
        nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=12, font_weight="bold")
        nx.draw_networkx_edges(G, pos, edgelist=spanning_tree_edges, edge_color="red", width=2)
        plt.title("Граф и его остовное дерево")
        plt.show()

# Пример использования
graph = Graph()
graph.generate_random_graph()
graph.print_graph()
