use std::io::Read;
use std::collections::{HashMap, HashSet};
use std::usize;

type PageOrder = (usize, usize);
type PageOrders = Vec<PageOrder>;
type Update = Vec<usize>;
type Updates = Vec<Update>;

type Graph = HashMap<usize, Vec<usize>>;

fn read_all(path: &str) -> String {
    let mut page_orders: PageOrders = PageOrders::new();
    let mut updates: Updates = Updates::new();
    let mut is_page_order = true;

    let mut file = std::fs::File::open(path).unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    contents
}

fn build_graph(page_orders: &PageOrders) -> Graph {
    let mut graph = Graph::new();

    for (a, b) in page_orders {
        graph.entry(*a).or_insert(Vec::new()).push(*b);
    }

    graph
}

fn topological_sort(graph: &Graph) -> Vec<usize> {
    let mut visited = HashSet::new();
    let mut stack = Vec::new();

    for &node in graph.keys() {
        if !visited.contains(&node) {
            dfs(node, graph, &mut visited, &mut stack);
        }
    }

    stack.reverse();
    stack
}

fn dfs(node: usize, graph: &Graph, visited: &mut HashSet<usize>, stack: &mut Vec<usize>) {
    if !visited.insert(node) {
        return;
    }

    if let Some(neighbors) = graph.get(&node) {
        for &neighbor in neighbors {
            if !visited.contains(&neighbor) {
                dfs(neighbor, graph, visited, stack);
            }
        }
    }

    stack.push(node);
}

fn main() {
    let path = "input.txt";
    let input = read_all(path);

    let (orders, queries) = input.split_once("\n\n").unwrap();

    let mut graph = Graph::new();
    for order in orders.lines() {
        let (page, dep_page) = order
            .split_once('|')
            .unwrap();

        graph
            .entry(dep_page.parse().unwrap())
            .or_default()
            .push(page.parse().unwrap());
    }

    for (vertices, edges) in &graph {
        println!("{}: {:?}", vertices, edges);
    }

    let pages = queries
        .lines()
        .map(|page| {
            page
                .split(',')
                .map(|num| num.parse::<usize>().unwrap())
                .collect::<Vec<usize>>()
    });

    let (mut part_i, mut part_ii) = (0, 0);
    for mut page in pages {
        if page.is_sorted_by(|a, b| graph[b].contains(a)) {
            part_i += page[page.len() / 2];
        } else {
            page.sort_by(|a, b| graph[b].contains(a).cmp(&true));
            part_ii += page[page.len() / 2];
        }
    }
    println!("{}, {}", part_i, part_ii);
}
