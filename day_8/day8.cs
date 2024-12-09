namespace day_8
{
    using System;
    using System.Collections.Generic;

    public class Program
    {
        static List<string> ReadInputGrid(string filePath)
        {
            return [.. File.ReadAllLines(filePath)];
        }

        static Dictionary<char, List<(int x, int y)>> ParseAntennas(List<string> grid)
        {
            var antennas = new Dictionary<char, List<(int x, int y)>>();

            for (int y = 0; y < grid.Count; y++)
            {
                for (int x = 0; x < grid[y].Length; x++)
                {
                    char cell = grid[y][x];
                    if (char.IsLetterOrDigit(cell))
                    {
                        if (!antennas.ContainsKey(cell))
                        {
                            antennas[cell] = [];
                        }

                        antennas[cell].Add((x, y));
                    }
                }
            }

            return antennas;
        }

        static bool IsWithinBounds((int x, int y) position, int width, int height)
        {
            var (x, y) = position;
            return x >= 0 && x < width && y >= 0 && y < height;
        }

        static HashSet<(int x, int y)> FindAntinodes(
                Dictionary<char, List<(int x, int y)>> antennas,
                int mapWidth,
                int mapHeight)
        {
            var antinodePositions = new HashSet<(int x, int y)>();

            foreach (var entry in antennas)
            {
                char frequency = entry.Key;
                var positions = entry.Value;

                for (int i = 0; i < positions.Count; i++)
                {
                    for (int j = i + 1; j < positions.Count; j++)
                    {
                        var (x1, y1) = positions[i];
                        var (x2, y2) = positions[j];

                        int dx = x2 - x1;
                        int dy = y2 - y1;

                        var antinode1 = (x1 - dx, y1 - dy);
                        var antinode2 = (x2 + dx, y2 + dy);

                        if (IsWithinBounds(antinode1, mapWidth, mapHeight))
                        {
                            antinodePositions.Add(antinode1);
                        }

                        if (IsWithinBounds(antinode2, mapWidth, mapHeight))
                        {
                            antinodePositions.Add(antinode2);
                        }
                    }
                }
            }

            return antinodePositions;
        }

        static HashSet<(int x, int y)> FindAntinodesPartII(
            Dictionary<char, List<(int x, int y)>> antennas,
            int mapWidth,
            int mapHeight)
        {
            var antinodePositions = new HashSet<(int x, int y)>();

            foreach (var entry in antennas)
            {
                var points = entry.Value;

                for (int i = 0; i < points.Count; i++)
                {
                    for (int j = i + 1; j < points.Count; j++)
                    {
                        var (x1, y1) = points[i];
                        var (x2, y2) = points[j];

                        int vx = x2 - x1;
                        int vy = y2 - y1;

                        int n = 1;
                        while (true)
                        {
                            var p3 = (x2 + n * vx, y2 + n * vy);
                            var p4 = (x1 - n * vx, y1 - n * vy);

                            if (IsWithinBounds(p3, mapWidth, mapHeight))
                            {
                                antinodePositions.Add(p3);
                            }

                            if (IsWithinBounds(p4, mapWidth, mapHeight))
                            {
                                antinodePositions.Add(p4);
                            }

                            if (IsWithinBounds((x1, y1), mapWidth, mapHeight))
                            {
                                antinodePositions.Add((x1, y1));
                            }

                            if (IsWithinBounds((x2, y2), mapWidth, mapHeight))
                            {
                                antinodePositions.Add((x2, y2));
                            }

                            if (!IsWithinBounds(p3, mapWidth, mapHeight) && !IsWithinBounds(p4, mapWidth, mapHeight))
                            {
                                break;
                            }

                            n++;
                        }
                    }
                }
            }

            return antinodePositions;
        }

        static void Main()
        {
            var inputGrid = ReadInputGrid("input.txt");
            int mapWidth = inputGrid[0].Length;
            int mapHeight = inputGrid.Count;

            var antennas = ParseAntennas(inputGrid);
            var antinodePositions = FindAntinodes(antennas, mapWidth, mapHeight);
            Console.WriteLine($"Part I: {antinodePositions.Count}");

            antinodePositions = FindAntinodesPartII(antennas, mapWidth, mapHeight);
            Console.WriteLine($"Part II: {antinodePositions.Count}");
        }
    }
}
